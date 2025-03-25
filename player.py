# player.py
"""Player module: Where the tunes and flicks come to life."""

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget, QListWidgetItem, QMenu, QAction
from PyQt5.QtCore import QUrl, QThread, pyqtSignal, Qt, QSize  # Added QSize
from PyQt5.QtGui import QPainter, QColor, QIcon
import logging
import os
import random
import numpy as np
import json
import requests
import yt_dlp

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Replace with your YouTube API key
YOUTUBE_API_KEY = "AIzaSyDSEGZTR-Aa17Y5jIJ-jyinl18l97bhYp4"

class FetchWorker(QThread):
    """Worker thread for fetching YouTube content and downloading."""
    tracks_fetched = pyqtSignal(list)  # [(title, video_id, thumbnail_url), ...]
    track_downloaded = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    progress_updated = pyqtSignal(int)  # For download progress

    def __init__(self, cache_dir, query="music"):
        super().__init__()
        self.cache_dir = cache_dir
        self.query = query
        self._running = True

    def run(self):
        """Fetch YouTube videos using the API."""
        if not self._running:
            return
        try:
            url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                "part": "snippet",
                "q": self.query,
                "type": "video",
                "maxResults": 20,
                "key": YOUTUBE_API_KEY,
                "videoCategoryId": "10"  # Music category
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            tracks = [
                (
                    item["snippet"]["title"],
                    item["id"]["videoId"],
                    item["snippet"]["thumbnails"]["default"]["url"]
                ) for item in data["items"]
            ]
            self.tracks_fetched.emit(tracks)
            if tracks and self._running:
                title, video_id, _ = random.choice(tracks)
                self.download_track(title, video_id)
        except requests.exceptions.RequestException as e:
            if self._running:
                self.error_occurred.emit(f"Network error while fetching YouTube content: {str(e)}")
        except Exception as e:
            if self._running:
                self.error_occurred.emit(f"Failed to fetch YouTube content: {str(e)}")

    def download_track(self, title, video_id):
        """Download a YouTube video as audio with progress."""
        if not self._running:
            return
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"

            def progress_hook(d):
                if d["status"] == "downloading":
                    total = d.get("total_bytes", 0)
                    downloaded = d.get("downloaded_bytes", 0)
                    if total > 0:
                        progress = int((downloaded / total) * 100)
                        self.progress_updated.emit(progress)

            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": os.path.join(self.cache_dir, f"{title}.%(ext)s"),
                "quiet": True,
                "progress_hooks": [progress_hook],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                self.track_downloaded.emit(file_path)
        except requests.exceptions.RequestException as e:
            if self._running:
                self.error_occurred.emit(f"Network error while downloading: {str(e)}")
        except Exception as e:
            if self._running:
                self.error_occurred.emit(f"Failed to download: {str(e)}")

    def stop(self):
        """Stop the thread safely."""
        self._running = False
        self.quit()
        self.wait()

class VisualizerWidget(QWidget):
    """Enhanced audio visualizer widget with dynamic colors."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.audio_data = []
        self.color_phase = 0

    def set_audio_data(self, data):
        """Update visualizer with audio data."""
        self.audio_data = data
        self.update()

    def paintEvent(self, event):
        """Draw the visualizer bars with dynamic colors."""
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.black)
        if not self.audio_data:
            return
        bar_width = self.width() // len(self.audio_data)
        self.color_phase = (self.color_phase + 1) % 360
        for i, value in enumerate(self.audio_data):
            height = int(value * self.height() / 255)
            hue = (self.color_phase + i * 10) % 360
            color = QColor.fromHsv(hue, 255, 255)
            painter.setBrush(color)
            painter.drawRect(i * bar_width, self.height() - height, bar_width - 2, height)

class TuneBlasterPlayer:
    """Playback engine: The DJ spinning the tracks."""
    def __init__(self, parent):
        self.parent = parent
        self.media_player = QMediaPlayer(parent)
        self.playlist = []
        self.queue = []  # New queue for tracks to be played
        self.web_tracks = []  # [(title, video_id, thumbnail_url), ...]
        self.cache_dir = os.path.expanduser("~/TuneBlaster_Cache")
        self.config_dir = os.path.expanduser("~/TuneBlaster_Config")
        os.makedirs(self.cache_dir, exist_ok=True)
        os.makedirs(self.config_dir, exist_ok=True)
        self.chunk_size = 10 * 1024 * 1024  # 10MB chunks
        self.playlist_file = os.path.join(self.config_dir, "playlist.json")
        self.current_track = None
        self.current_playlist_index = -1
        self.workers = []

        # Connect signals
        self.media_player.durationChanged.connect(self.update_duration)
        self.media_player.positionChanged.connect(self.update_position)
        self.media_player.error.connect(self.handle_error)
        self.media_player.mediaStatusChanged.connect(self.on_media_status_changed)  # For auto-playing queue

    def toggle_playback(self):
        """Play or pause the media, like a musical yo-yo."""
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.parent.ui.play_button.setText("Play")
        else:
            if self.media_player.media().isNull():
                self.fetch_youtube()
            else:
                self.media_player.play()
                self.parent.ui.play_button.setText("Pause")

    def play_next_track(self):
        """Play the next track in the playlist."""
        if not self.playlist:
            QMessageBox.warning(self.parent, "Oops!", "No tracks in the playlist!")
            return
        self.current_playlist_index = (self.current_playlist_index + 1) % len(self.playlist)
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.playlist[self.current_playlist_index])))
        self.current_track = os.path.basename(self.playlist[self.current_playlist_index])
        self.update_now_playing()
        self.media_player.play()
        self.parent.ui.play_button.setText("Pause")
        fake_audio = np.random.randint(0, 255, 50).tolist()
        self.parent.ui.visualizer.set_audio_data(fake_audio)
        logging.info(f"Playing next track: {self.current_track}")

    def play_prev_track(self):
        """Play the previous track in the playlist."""
        if not self.playlist:
            QMessageBox.warning(self.parent, "Oops!", "No tracks in the playlist!")
            return
        self.current_playlist_index = (self.current_playlist_index - 1) % len(self.playlist)
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.playlist[self.current_playlist_index])))
        self.current_track = os.path.basename(self.playlist[self.current_playlist_index])
        self.update_now_playing()
        self.media_player.play()
        self.parent.ui.play_button.setText("Pause")
        fake_audio = np.random.randint(0, 255, 50).tolist()
        self.parent.ui.visualizer.set_audio_data(fake_audio)
        logging.info(f"Playing previous track: {self.current_track}")

    def shuffle_playlist(self):
        """Shuffle the playlist and start playing from the first track."""
        if not self.playlist:
            QMessageBox.warning(self.parent, "Oops!", "No tracks in the playlist to shuffle!")
            return
        shuffled_playlist = self.playlist.copy()
        random.shuffle(shuffled_playlist)
        self.playlist = shuffled_playlist
        self.current_playlist_index = 0
        self.update_playlist_ui()
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.playlist[0])))
        self.current_track = os.path.basename(self.playlist[0])
        self.update_now_playing()
        self.media_player.play()
        self.parent.ui.play_button.setText("Pause")
        fake_audio = np.random.randint(0, 255, 50).tolist()
        self.parent.ui.visualizer.set_audio_data(fake_audio)
        logging.info("Playlist shuffled and playing first track")

    def clear_playlist(self):
        """Clear the current playlist and queue."""
        self.playlist = []
        self.queue = []
        self.current_playlist_index = -1
        self.current_track = None
        self.media_player.setMedia(QMediaContent())
        self.update_playlist_ui()
        self.update_now_playing()
        self.parent.ui.play_button.setText("Play")
        QMessageBox.information(self.parent, "Success", "Playlist and queue cleared!")
        logging.info("Playlist and queue cleared")

    def load_local_media(self):
        """Load local files, splitting large ones."""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self.parent,
            "Select Media Files",
            "",
            "Media Files (*.mp3 *.wav *.mp4 *.avi *.mkv);;All Files (*)"
        )
        if file_paths:
            for file_path in file_paths:
                if os.path.getsize(file_path) > self.chunk_size:
                    self.split_and_load(file_path)
                else:
                    self.playlist.append(file_path)
            self.current_playlist_index = 0
            self.update_playlist_ui()
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.playlist[0])))
            self.current_track = os.path.basename(self.playlist[0])
            self.update_now_playing()
            self.media_player.play()
            self.parent.ui.play_button.setText("Pause")
            logging.info(f"Loaded local files: {file_paths}")

    def split_and_load(self, file_path):
        """Split large files into chunks and add to playlist."""
        try:
            base_name = os.path.splitext(file_path)[0]
            with open(file_path, "rb") as f:
                part_num = 0
                while True:
                    chunk = f.read(self.chunk_size)
                    if not chunk:
                        break
                    chunk_path = f"{base_name}_part{part_num}.mp3"
                    with open(chunk_path, "wb") as chunk_file:
                        chunk_file.write(chunk)
                    self.playlist.append(chunk_path)
                    part_num += 1
            logging.info(f"Split {file_path} into {part_num} parts")
        except Exception as e:
            QMessageBox.critical(self.parent, "Split Error", f"Failed to split file: {str(e)}")
            logging.error(f"File split failed: {str(e)}")

    def fetch_youtube(self):
        """Fetch default YouTube music content."""
        self.parent.ui.download_progress.setValue(0)
        worker = FetchWorker(self.cache_dir, query="music")
        self.workers.append(worker)
        worker.tracks_fetched.connect(self.on_tracks_fetched)
        worker.track_downloaded.connect(self.on_track_downloaded)
        worker.error_occurred.connect(self.on_error)
        worker.progress_updated.connect(self.parent.ui.download_progress.setValue)
        worker.start()

    def search_youtube(self):
        """Search YouTube based on user input."""
        query = self.parent.ui.search_input.text().strip()
        if query:
            self.parent.ui.download_progress.setValue(0)
            worker = FetchWorker(self.cache_dir, query=query)
            self.workers.append(worker)
            worker.tracks_fetched.connect(self.on_tracks_fetched)
            worker.track_downloaded.connect(self.on_track_downloaded)
            worker.error_occurred.connect(self.on_error)
            worker.progress_updated.connect(self.parent.ui.download_progress.setValue)
            worker.start()
        else:
            QMessageBox.warning(self.parent, "Oops!", "Enter a search term, ya dingus!")

    def on_tracks_fetched(self, tracks):
        """Handle fetched tracks from worker thread."""
        self.web_tracks = tracks
        self.update_track_grid()
        logging.info(f"Fetched {len(self.web_tracks)} tracks from YouTube API")

    def on_track_downloaded(self, file_path):
        """Handle downloaded track from worker thread."""
        self.playlist.append(file_path)
        self.current_playlist_index = len(self.playlist) - 1
        self.update_playlist_ui()
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
        self.current_track = os.path.basename(file_path)
        self.update_now_playing()
        self.media_player.play()
        self.parent.ui.play_button.setText("Pause")
        fake_audio = np.random.randint(0, 255, 50).tolist()
        self.parent.ui.visualizer.set_audio_data(fake_audio)
        self.parent.ui.download_progress.setValue(100)
        logging.info(f"Playing downloaded track: {file_path}")

    def on_error(self, error_msg):
        """Handle errors from worker thread."""
        QMessageBox.critical(self.parent, "Error", error_msg)
        self.parent.ui.download_progress.setValue(0)
        logging.error(error_msg)

    def play_from_grid(self, item):
        """Play a track from the web track grid when double-clicked."""
        index = self.parent.ui.track_grid.row(item)
        title, video_id, _ = self.web_tracks[index]
        self.parent.ui.download_progress.setValue(0)
        worker = FetchWorker(self.cache_dir)
        self.workers.append(worker)
        worker.track_downloaded.connect(self.on_track_downloaded)
        worker.error_occurred.connect(self.on_error)
        worker.progress_updated.connect(self.parent.ui.download_progress.setValue)
        worker.download_track(title, video_id)
        worker.start()

    def show_context_menu(self, position):
        """Show context menu for queuing tracks."""
        item = self.parent.ui.track_grid.itemAt(position)
        if not item:
            return
        index = self.parent.ui.track_grid.row(item)
        menu = QMenu()
        queue_action = QAction("Add to Queue", self.parent)
        queue_action.triggered.connect(lambda: self.add_to_queue(index))
        menu.addAction(queue_action)
        menu.exec_(self.parent.ui.track_grid.mapToGlobal(position))

    def add_to_queue(self, index):
        """Add a track to the queue without playing it immediately."""
        title, video_id, _ = self.web_tracks[index]
        self.parent.ui.download_progress.setValue(0)
        worker = FetchWorker(self.cache_dir)
        self.workers.append(worker)
        worker.track_downloaded.connect(lambda file_path: self.on_track_queued(file_path))
        worker.error_occurred.connect(self.on_error)
        worker.progress_updated.connect(self.parent.ui.download_progress.setValue)
        worker.download_track(title, video_id)
        worker.start()

    def on_track_queued(self, file_path):
        """Handle track added to queue."""
        self.queue.append(file_path)
        self.parent.ui.download_progress.setValue(100)
        QMessageBox.information(self.parent, "Success", f"Track queued: {os.path.basename(file_path)}")
        logging.info(f"Track queued: {file_path}")

    def on_media_status_changed(self, status):
        """Auto-play the next track from the queue when the current track ends."""
        if status == QMediaPlayer.EndOfMedia and self.queue:
            next_track = self.queue.pop(0)
            self.playlist.append(next_track)
            self.current_playlist_index = len(self.playlist) - 1
            self.update_playlist_ui()
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(next_track)))
            self.current_track = os.path.basename(next_track)
            self.update_now_playing()
            self.media_player.play()
            self.parent.ui.play_button.setText("Pause")
            fake_audio = np.random.randint(0, 255, 50).tolist()
            self.parent.ui.visualizer.set_audio_data(fake_audio)
            logging.info(f"Playing queued track: {next_track}")

    def update_track_grid(self):
        """Refresh the track grid with fetched web tracks and thumbnails."""
        self.parent.ui.track_grid.clear()
        for title, _, thumbnail_url in self.web_tracks:
            item = QListWidgetItem()
            try:
                response = requests.get(thumbnail_url)
                response.raise_for_status()
                with open(os.path.join(self.cache_dir, f"{title}_thumb.jpg"), "wb") as f:
                    f.write(response.content)
                item.setIcon(QIcon(os.path.join(self.cache_dir, f"{title}_thumb.jpg")))
            except Exception as e:
                logging.error(f"Failed to download thumbnail: {str(e)}")
            item.setText(title)
            item.setSizeHint(QSize(150, 150))
            self.parent.ui.track_grid.addItem(item)

    def update_playlist_ui(self):
        """Refresh the playlist widget with current files."""
        self.parent.ui.playlist_widget.clear()
        for file_path in self.playlist:
            self.parent.ui.playlist_widget.addItem(file_path)

    def update_now_playing(self):
        """Update the now-playing label."""
        if self.current_track:
            self.parent.ui.now_playing_label.setText(f"Now Playing: {self.current_track}")
        else:
            self.parent.ui.now_playing_label.setText("Now Playing: None")

    def save_playlist(self):
        """Save the current playlist to a JSON file."""
        try:
            with open(self.playlist_file, "w") as f:
                json.dump({"playlist": self.playlist, "web_tracks": self.web_tracks}, f)
            QMessageBox.information(self.parent, "Success", "Playlist saved!")
            logging.info("Playlist saved to JSON")
        except Exception as e:
            QMessageBox.critical(self.parent, "Save Error", f"Failed to save playlist: {str(e)}")
            logging.error(f"Playlist save failed: {str(e)}")

    def load_playlist(self):
        """Load a saved playlist from a JSON file."""
        try:
            if os.path.exists(self.playlist_file):
                with open(self.playlist_file, "r") as f:
                    data = json.load(f)
                    self.playlist = data.get("playlist", [])
                    self.web_tracks = data.get("web_tracks", [])
                    self.current_playlist_index = 0
                    self.update_playlist_ui()
                    self.update_track_grid()
                    if self.playlist:
                        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.playlist[0])))
                        self.current_track = os.path.basename(self.playlist[0])
                        self.update_now_playing()
                        self.media_player.play()
                        self.parent.ui.play_button.setText("Pause")
                    QMessageBox.information(self.parent, "Success", "Playlist loaded!")
                    logging.info("Playlist loaded from JSON")
            else:
                QMessageBox.warning(self.parent, "Oops!", "No saved playlist found!")
        except Exception as e:
            QMessageBox.critical(self.parent, "Load Error", f"Failed to load playlist: {str(e)}")
            logging.error(f"Playlist load failed: {str(e)}")

    def seek(self, position):
        """Jump to a specific time in the media."""
        self.media_player.setPosition(position)

    def set_volume(self, value):
        """Adjust volume, from whisper to wall-shaking."""
        self.media_player.setVolume(value)

    def update_duration(self, duration):
        """Set seek slider range when media loads."""
        self.parent.ui.seek_slider.setRange(0, duration)

    def update_position(self, position):
        """Update seek slider as media plays."""
        self.parent.ui.seek_slider.setValue(position)
        fake_audio = np.random.randint(0, 255, 50).tolist()
        self.parent.ui.visualizer.set_audio_data(fake_audio)

    def handle_error(self, error):
        """Show a popup if something goes wrong."""
        error_msg = self.media_player.errorString()
        QMessageBox.critical(self.parent, "Playback Error", f"Uh-oh: {error_msg}")
        logging.error(f"Media player error: {error_msg}")

    def cleanup(self):
        """Clean up threads on app close."""
        for worker in self.workers:
            worker.stop()
        self.workers.clear()

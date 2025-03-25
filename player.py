# player.py
"""Player module: Where the tunes and flicks come to life."""

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget
from PyQt5.QtCore import QUrl, QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPainter, QColor
import logging
import os
import random
import numpy as np
import json
import requests  # For YouTube API calls

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class FetchWorker(QThread):
    """Worker thread for fetching YouTube content via API."""
    tracks_fetched = pyqtSignal(list)  # Signal for fetched tracks: [(title, video_id), ...]
    error_occurred = pyqtSignal(str)   # Signal for errors

    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key

    def run(self):
        """Fetch music videos from YouTube API."""
        try:
            url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                "part": "snippet",
                "q": "music -inurl:(signup login)",  # Default query
                "type": "video",
                "maxResults": 20,
                "key": self.api_key,
                "videoCategoryId": "10",  # Music category
            }
            response = requests.get(url, params=params)
            data = response.json()
            if "items" in data:
                tracks = [(item["snippet"]["title"], item["id"]["videoId"]) for item in data["items"]]
                self.tracks_fetched.emit(tracks)
            else:
                self.error_occurred.emit("No tracks found in YouTube API response")
        except Exception as e:
            self.error_occurred.emit(f"Failed to fetch YouTube content: {str(e)}")

class VisualizerWidget(QWidget):
    """Simple audio visualizer widget."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.audio_data = []

    def set_audio_data(self, data):
        """Update visualizer with audio data."""
        self.audio_data = data
        self.update()

    def paintEvent(self, event):
        """Draw the visualizer bars."""
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.black)
        if not self.audio_data:
            return
        bar_width = self.width() // len(self.audio_data)
        for i, value in enumerate(self.audio_data):
            height = int(value * self.height() / 255)
            painter.setBrush(QColor(0, 255, 0))
            painter.drawRect(i * bar_width, self.height() - height, bar_width - 2, height)

class TuneBlasterPlayer:
    """Playback engine: The DJ spinning the tracks."""
    def __init__(self, parent):
        self.parent = parent
        self.media_player = QMediaPlayer(parent)
        self.media_player.setVideoOutput(self.parent.ui.video_display)
        self.playlist = []
        self.web_tracks = []  # Now stores (title, video_id)
        self.cache_dir = os.path.expanduser("~/TuneBlaster_Cache")
        self.config_dir = os.path.expanduser("~/TuneBlaster_Config")
        os.makedirs(self.cache_dir, exist_ok=True)
        os.makedirs(self.config_dir, exist_ok=True)
        self.chunk_size = 10 * 1024 * 1024  # 10MB chunks
        self.playlist_file = os.path.join(self.config_dir, "playlist.json")
        self.youtube_api_key = "AIzaSyDSEGZTR-Aa17Y5jIJ-jyinl18l97bhYp4"  # Replace with your key

        # Connect signals
        self.media_player.durationChanged.connect(self.update_duration)
        self.media_player.positionChanged.connect(self.update_position)
        self.media_player.error.connect(self.handle_error)

    def toggle_playback(self):
        """Play or pause the media, like a musical yo-yo."""
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.parent.ui.play_button.setText("Play")
        else:
            if self.media_player.media().isNull():
                self.fetch_music()
            else:
                self.media_player.play()
                self.parent.ui.play_button.setText("Pause")

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
            self.update_playlist_ui()
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.playlist[0])))
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

    def fetch_music(self):
        """Start fetching YouTube content in a worker thread."""
        self.worker = FetchWorker(self.youtube_api_key)
        self.worker.tracks_fetched.connect(self.on_tracks_fetched)
        self.worker.error_occurred.connect(self.on_error)
        self.worker.start()

    def on_tracks_fetched(self, tracks):
        """Handle fetched tracks from worker thread."""
        self.web_tracks = tracks
        self.update_track_list()
        # Play a random track
        if tracks:
            title, video_id = random.choice(tracks)
            self.play_youtube_track(video_id)
        logging.info(f"Fetched {len(self.web_tracks)} tracks from YouTube API")

    def on_error(self, error_msg):
        """Handle errors from worker thread."""
        QMessageBox.critical(self.parent, "Error", error_msg)
        logging.error(error_msg)

    def play_from_list(self, item):
        """Play a YouTube track from the web track list when double-clicked."""
        index = self.parent.ui.track_list.row(item)
        title, video_id = self.web_tracks[index]
        self.play_youtube_track(video_id)

    def play_youtube_track(self, video_id):
        """Play a YouTube video by ID."""
        url = f"https://www.youtube.com/watch?v={video_id}"
        self.media_player.setMedia(QMediaContent(QUrl(url)))
        self.media_player.play()
        self.parent.ui.play_button.setText("Pause")
        # Fake audio data for visualizer (real data needs audio analysis)
        fake_audio = np.random.randint(0, 255, 50).tolist()
        self.parent.ui.visualizer.set_audio_data(fake_audio)
        logging.info(f"Playing YouTube track: {video_id}")

    def filter_tracks(self, search_text):
        """Filter the track list based on search input, fetching new results if search changes."""
        if search_text:
            self.worker = FetchWorker(self.youtube_api_key)
            self.worker.tracks_fetched.connect(self.on_tracks_fetched)
            self.worker.error_occurred.connect(self.on_error)
            self.worker.run = lambda: self.search_youtube(search_text)  # Override run for search
            self.worker.start()
        else:
            self.update_track_list()

    def search_youtube(self, query):
        """Search YouTube API with custom query."""
        try:
            url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": 20,
                "key": self.youtube_api_key,
                "videoCategoryId": "10",
            }
            response = requests.get(url, params=params)
            data = response.json()
            if "items" in data:
                tracks = [(item["snippet"]["title"], item["id"]["videoId"]) for item in data["items"]]
                self.tracks_fetched.emit(tracks)
            else:
                self.error_occurred.emit("No tracks found for search")
        except Exception as e:
            self.error_occurred.emit(f"Failed to search YouTube: {str(e)}")

    def update_track_list(self):
        """Refresh the track list with fetched web tracks."""
        self.parent.ui.track_list.clear()
        for title, _ in self.web_tracks:
            self.parent.ui.track_list.addItem(title)

    def update_playlist_ui(self):
        """Refresh the playlist widget with current local files."""
        self.parent.ui.playlist_widget.clear()
        for file_path in self.playlist:
            self.parent.ui.playlist_widget.addItem(file_path)

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
                    self.update_playlist_ui()
                    self.update_track_list()
                    if self.playlist:
                        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.playlist[0])))
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

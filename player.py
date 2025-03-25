# player.py
"""Player module: Where the tunes and flicks come to life."""

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QUrl
import logging
import yt_dlp
import os
from threading import Thread
import random

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class TuneBlasterPlayer:
    """Playback engine: The DJ spinning the tracks."""
    def __init__(self, parent):
        self.parent = parent
        self.media_player = QMediaPlayer(parent)
        self.media_player.setVideoOutput(self.parent.ui.video_display)
        self.playlist = []  # Local files
        self.web_tracks = []  # Scraped tracks: (title, url)
        self.cache_dir = os.path.expanduser("~/TuneBlaster_Cache")
        os.makedirs(self.cache_dir, exist_ok=True)

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
                self.fetch_music()  # Auto-fetch if nothing’s loaded
            else:
                self.media_player.play()
                self.parent.ui.play_button.setText("Pause")

    def load_local_media(self):
        """Load local files, time to cue up the next banger!"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self.parent,
            "Select Media Files",
            "",
            "Media Files (*.mp3 *.wav *.mp4 *.avi *.mkv);;All Files (*)"
        )
        if file_paths:
            self.playlist.extend(file_paths)
            self.update_playlist_ui()
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_paths[0])))
            self.media_player.play()
            self.parent.ui.play_button.setText("Pause")
            logging.info(f"Loaded local files: {file_paths}")

    def fetch_music(self):
        """Fetch music from YouTube and play a random track."""
        Thread(target=self.scrape_youtube).start()

    def scrape_youtube(self):
        """Scrape YouTube for music tracks."""
        try:
            # Simple search for "music" (could expand with genres later)
            search_query = "music -inurl:(signup login)"
            ydl_opts = {
                "format": "bestaudio/best",
                "quiet": True,
                "extract_flat": True,  # Get metadata without downloading yet
                "default_search": "ytsearch20",  # Fetch 20 results
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(search_query, download=False)
                self.web_tracks = [(entry["title"], entry["url"]) for entry in result["entries"]]
                self.update_track_list()
                # Play a random track
                if self.web_tracks:
                    title, url = random.choice(self.web_tracks)
                    self.download_and_play(title, url)
                    logging.info(f"Fetched {len(self.web_tracks)} tracks from YouTube")
        except Exception as e:
            QMessageBox.critical(self.parent, "Fetch Error", f"Failed to fetch music: {str(e)}")
            logging.error(f"YouTube scrape failed: {str(e)}")

    def download_and_play(self, title, url):
        """Download a track and play it."""
        try:
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": os.path.join(self.cache_dir, f"{title}.%(ext)s"),
                "quiet": True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                self.playlist.append(file_path)
                self.update_playlist_ui()
                self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
                self.media_player.play()
                self.parent.ui.play_button.setText("Pause")
                logging.info(f"Playing downloaded track: {file_path}")
        except Exception as e:
            QMessageBox.critical(self.parent, "Download Error", f"Failed to download: {str(e)}")
            logging.error(f"Download failed: {str(e)}")

    def play_from_list(self, item):
        """Play a track from the web track list when double-clicked."""
        index = self.parent.ui.track_list.row(item)
        title, url = self.web_tracks[index]
        self.download_and_play(title, url)

    def filter_tracks(self, search_text):
        """Filter the track list based on search input."""
        self.parent.ui.track_list.clear()
        for title, url in self.web_tracks:
            if search_text.lower() in title.lower():
                self.parent.ui.track_list.addItem(title)

    def update_track_list(self):
        """Refresh the track list with fetched web tracks."""
        self.parent.ui.track_list.clear()
        for title, _ in self.web_tracks:
            self.parent.ui.track_list.addItem(title)

    def update_playlist_ui(self):
        """Refresh the playlist widget with current files."""
        self.parent.ui.playlist_widget.clear()
        for file_path in self.playlist:
            self.parent.ui.playlist_widget.addItem(file_path)

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

    def handle_error(self, error):
        """Show a popup if something goes wrong."""
        error_msg = self.media_player.errorString()
        QMessageBox.critical(self.parent, "Playback Error", f"Uh-oh: {error_msg}")
        logging.error(f"Media player error: {error_msg}")

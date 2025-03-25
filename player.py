# player.py
"""Player module: Where the tunes and flicks come to life."""

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QUrl
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class TuneBlasterPlayer:
    """Playback engine: The DJ spinning the tracks."""
    def __init__(self, parent):
        self.parent = parent
        self.media_player = QMediaPlayer(parent)
        self.media_player.setVideoOutput(self.parent.ui.video_display)
        self.playlist = []

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
                logging.warning("Nothing to play, mate!")
                QMessageBox.warning(self.parent, "Oops!", "Load some media first, ya dingus!")
            else:
                self.media_player.play()
                self.parent.ui.play_button.setText("Pause")

    def load_media(self):
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

    def load_stream(self):
        """Load an online stream from the URL input."""
        url = self.parent.ui.stream_input.text().strip()
        if url:
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url
            self.playlist.append(url)
            self.update_playlist_ui()
            self.media_player.setMedia(QMediaContent(QUrl(url)))
            self.media_player.play()
            self.parent.ui.play_button.setText("Pause")
            self.parent.ui.stream_input.clear()
            logging.info(f"Loaded stream: {url}")
        else:
            QMessageBox.warning(self.parent, "Oops!", "Enter a valid URL, ya dingus!")
            logging.warning("Empty URL input attempted.")

    def play_from_playlist(self, item):
        """Play a file or stream from the playlist when double-clicked."""
        media_source = item.text()
        if media_source.startswith("http://") or media_source.startswith("https://"):
            self.media_player.setMedia(QMediaContent(QUrl(media_source)))
        else:
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(media_source)))
        self.media_player.play()
        self.parent.ui.play_button.setText("Pause")
        logging.info(f"Playing from playlist: {media_source}")

    def update_playlist_ui(self):
        """Refresh the playlist widget with current files and URLs."""
        self.parent.ui.playlist_widget.clear()
        for media_source in self.playlist:
            self.parent.ui.playlist_widget.addItem(media_source)

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

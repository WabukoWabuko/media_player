# player.py
"""Player module: Where the tunes and flicks come to life."""

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QUrl

class TuneBlasterPlayer:
    """Playback engine: The DJ spinning the tracks."""
    def __init__(self, parent):
        self.parent = parent
        self.media_player = QMediaPlayer(parent)
        self.media_player.setVideoOutput(self.parent.ui.video_display)
        self.playlist = []  # Store file paths

        # Connect player signals for seek slider
        self.media_player.durationChanged.connect(self.update_duration)
        self.media_player.positionChanged.connect(self.update_position)

    def toggle_playback(self):
        """Play or pause the media, like a musical yo-yo."""
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.parent.ui.play_button.setText("Play")
        else:
            self.media_player.play()
            self.parent.ui.play_button.setText("Pause")

    def load_media(self):
        """Load files, time to cue up the next banger!"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self.parent,
            "Select Media Files",
            "",
            "Media Files (*.mp3 *.wav *.mp4 *.avi *.mkv);;All Files (*)"
        )
        if file_paths:
            self.playlist.extend(file_paths)
            self.update_playlist_ui()
            # Play the first file immediately
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_paths[0])))
            self.media_player.play()
            self.parent.ui.play_button.setText("Pause")

    def play_from_playlist(self, item):
        """Play a file from the playlist when double-clicked."""
        file_path = item.text()
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
        self.media_player.play()
        self.parent.ui.play_button.setText("Pause")

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

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

    def toggle_playback(self):
        """Play or pause the media, like a musical yo-yo."""
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.parent.ui.play_button.setText("Play")
        else:
            self.media_player.play()
            self.parent.ui.play_button.setText("Pause")

    def load_media(self):
        """Load a file, time to cue up the next banger!"""
        file_path, _ = QFileDialog.getOpenFileName(
            self.parent,
            "Select a Media File",
            "",
            "Media Files (*.mp3 *.wav *.mp4 *.avi *.mkv);;All Files (*)"
        )
        if file_path:
            media_content = QMediaContent(QUrl.fromLocalFile(file_path))
            self.media_player.setMedia(media_content)
            self.media_player.play()
            self.parent.ui.play_button.setText("Pause")

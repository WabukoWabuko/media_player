# player.py
"""Player module: Where the magic of sound and video happens."""
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QUrl

class MediaPlayerBackend:
    """Backend for playing media, the DJ behind the scenes."""
    def __init__(self, parent):
        self.parent = parent
        self.player = QMediaPlayer(parent)
        self.player.setVideoOutput(parent.ui.video_widget)

    def toggle_play(self):
        """Play or pause, like flipping a musical light switch."""
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.parent.ui.play_btn.setText("Play")
        else:
            self.player.play()
            self.parent.ui.play_btn.setText("Pause")

    def open_media(self):
        """Open a local file, time to drop the beat!"""
        file, _ = QFileDialog.getOpenFileName(
            self.parent, "Pick a Tune or Flick", "",
            "Media Files (*.mp3 *.wav *.mp4 *.avi);;All Files (*)"
        )
        if file:
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(file)))
            self.player.play()
            self.parent.ui.play_btn.setText("Pause")

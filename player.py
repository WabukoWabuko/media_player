# player.py
# Where the tunes and vids come to life - the DJ of the app

from PyQt6.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt6.QtCore import QUrl

class MediaPlayerLogic:
    """Handles all the playback wizardry."""
    def __init__(self, parent):
        # Parent is the main window, so we can talk to the UI
        self.parent = parent
        # Create the media player - our trusty jukebox
        self.player = QMediaPlayer(parent)
        
        # Connect signals to keep the UI in sync
        self.player.durationChanged.connect(self.update_duration)
        self.player.positionChanged.connect(self.update_position)

    def play_media(self, file_path=None, url=None):
        """Plays a local file or URL - versatility is our jam."""
        if file_path:
            # Local file? Convert to a QUrl and let it rip
            self.player.setSource(QUrl.fromLocalFile(file_path))
        elif url:
            # Online stream? Feed it straight to the player
            self.player.setSource(QUrl(url))
        self.player.play()

    def toggle_play(self):
        """Play or pause - because who doesn’t love a good toggle?"""
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def stop(self):
        """Stop the party - full reset."""
        self.player.stop()

    def set_position(self, position):
        """Seek to a spot in the track - precision is key."""
        self.player.setPosition(position)

    def update_duration(self, duration):
        """Tell the UI how long this masterpiece is."""
        self.parent.ui.seek_slider.setRange(0, duration)

    def update_position(self, position):
        """Keep the seek slider grooving along."""
        self.parent.ui.seek_slider.setValue(position)

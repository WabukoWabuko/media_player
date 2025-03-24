# core.py
# The beating heart of our media player, where the magic starts

from PyQt6.QtWidgets import QMainWindow
from ui import PlayerUI
from player import MediaPlayerLogic

class MediaPlayerApp(QMainWindow):
    """Main window class that ties everything together."""
    def __init__(self):
        super().__init__()
        # Set window title and size - big enough to impress, small enough to fit
        self.setWindowTitle("GrooveMaster 3000")
        self.resize(600, 400)

        # Initialize the player logic (the brains)
        self.player_logic = MediaPlayerLogic(self)
        # Set up the UI (the pretty face)
        self.ui = PlayerUI(self, self.player_logic)

        # Make the UI the star of the show
        self.setCentralWidget(self.ui)

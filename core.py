# core.py
"""Core module: The beating heart of TuneBlaster 3000."""

from PyQt5.QtWidgets import QMainWindow
from ui import TuneBlasterUI
from player import TuneBlasterPlayer

class TuneBlasterApp(QMainWindow):
    """Main window class: The conductor of our musical orchestra."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TuneBlaster 3000")
        self.setGeometry(100, 100, 600, 400)

        # Setup UI first
        self.ui = TuneBlasterUI(self)
        self.ui.setup_ui()

        # Then setup player
        self.player = TuneBlasterPlayer(self)

        # Connect UI signals to player slots
        self.ui.play_button.clicked.connect(self.player.toggle_playback)
        self.ui.open_button.clicked.connect(self.player.load_media)

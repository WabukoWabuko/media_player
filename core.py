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
        self.setGeometry(100, 100, 1200, 800)

        # Setup UI first
        self.ui = TuneBlasterUI(self)
        self.ui.setup_ui()

        # Then setup player
        self.player = TuneBlasterPlayer(self)

        # Connect UI signals to player slots
        self.ui.play_button.clicked.connect(self.player.toggle_playback)
        self.ui.next_button.clicked.connect(self.player.play_next_track)  # New connection
        self.ui.open_button.clicked.connect(self.player.load_local_media)
        self.ui.seek_slider.sliderMoved.connect(self.player.seek)
        self.ui.volume_slider.valueChanged.connect(self.player.set_volume)
        self.ui.track_grid.itemDoubleClicked.connect(self.player.play_from_grid)
        self.ui.fetch_button.clicked.connect(self.player.fetch_youtube)
        self.ui.search_input.returnPressed.connect(self.player.search_youtube)
        self.ui.save_button.clicked.connect(self.player.save_playlist)
        self.ui.load_button.clicked.connect(self.player.load_playlist)

    def closeEvent(self, event):
        """Ensure threads are terminated on close."""
        self.player.cleanup()
        event.accept()

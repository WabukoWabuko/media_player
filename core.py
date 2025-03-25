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
        self.setGeometry(100, 100, 800, 600)

        # Setup UI first
        self.ui = TuneBlasterUI(self)
        self.ui.setup_ui()

        # Then setup player
        self.player = TuneBlasterPlayer(self)

        # Connect UI signals to player slots
        self.ui.play_button.clicked.connect(self.player.toggle_playback)
        self.ui.open_button.clicked.connect(self.player.load_local_media)
        self.ui.seek_slider.sliderMoved.connect(self.player.seek)
        self.ui.seek_slider.sliderPressed.connect(self.player.start_seeking)
        self.ui.seek_slider.sliderReleased.connect(self.player.stop_seeking)
        self.ui.volume_slider.valueChanged.connect(self.player.set_volume)
        self.ui.track_list.itemDoubleClicked.connect(self.player.play_from_list)
        self.ui.fetch_button.clicked.connect(self.player.fetch_music)
        self.ui.search_input.textChanged.connect(self.player.filter_tracks)
        self.ui.save_button.clicked.connect(self.player.save_playlist)
        self.ui.load_button.clicked.connect(self.player.load_playlist)

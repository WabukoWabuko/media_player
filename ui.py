# ui.py
"""UI module: Dressing up TuneBlaster 3000 in style."""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSlider, QListWidget, QHBoxLayout, QLineEdit
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt
from player import VisualizerWidget

class TuneBlasterUI:
    """UI handler: Making our player look good and play nice."""
    def __init__(self, parent):
        self.parent = parent

    def setup_ui(self):
        """Build the interface, rolling out the red carpet for controls."""
        main_widget = QWidget(self.parent)
        self.parent.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        self.video_display = QVideoWidget()
        main_layout.addWidget(self.video_display)

        # Visualizer
        self.visualizer = VisualizerWidget()
        self.visualizer.setFixedHeight(100)
        main_layout.addWidget(self.visualizer)

        # Search and fetch layout
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search tracks...")
        search_layout.addWidget(self.search_input)
        self.fetch_button = QPushButton("Play Music")
        search_layout.addWidget(self.fetch_button)
        main_layout.addLayout(search_layout)

        # Track list
        self.track_list = QListWidget()
        main_layout.addWidget(self.track_list)

        # Controls
        controls_layout = QHBoxLayout()
        self.play_button = QPushButton("Play")
        controls_layout.addWidget(self.play_button)
        self.seek_slider = QSlider(Qt.Horizontal)
        self.seek_slider.setMinimum(0)
        self.seek_slider.setMaximum(1000)
        controls_layout.addWidget(self.seek_slider)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)
        controls_layout.addWidget(self.volume_slider)
        self.open_button = QPushButton("Open Local Files")
        controls_layout.addWidget(self.open_button)
        main_layout.addLayout(controls_layout)

        # Account buttons
        account_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Playlist")
        account_layout.addWidget(self.save_button)
        self.load_button = QPushButton("Load Playlist")
        account_layout.addWidget(self.load_button)
        main_layout.addLayout(account_layout)

        # Playlist widget (downloaded files)
        self.playlist_widget = QListWidget()
        main_layout.addWidget(self.playlist_widget)

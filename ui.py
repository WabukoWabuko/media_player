# ui.py
"""UI module: Dressing up TuneBlaster 3000 in style."""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSlider, QListWidget, QHBoxLayout, QLineEdit, QListWidgetItem
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

        # Video display (larger for video playback)
        self.video_display = QVideoWidget()
        self.video_display.setMinimumHeight(300)
        main_layout.addWidget(self.video_display)

        # Compact control bar (VLC style)
        control_bar = QHBoxLayout()
        self.play_button = QPushButton("Play")
        self.play_button.setFixedWidth(80)
        control_bar.addWidget(self.play_button)
        self.seek_slider = QSlider(Qt.Horizontal)
        self.seek_slider.setMinimum(0)
        self.seek_slider.setMaximum(1000)
        control_bar.addWidget(self.seek_slider)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)
        self.volume_slider.setFixedWidth(100)
        control_bar.addWidget(self.volume_slider)
        main_layout.addLayout(control_bar)

        # Visualizer (smaller, below controls)
        self.visualizer = VisualizerWidget()
        self.visualizer.setFixedHeight(50)
        main_layout.addWidget(self.visualizer)

        # Search and fetch bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search tracks...")
        search_layout.addWidget(self.search_input)
        self.fetch_button = QPushButton("Play Music")
        self.fetch_button.setFixedWidth(100)
        search_layout.addWidget(self.fetch_button)
        main_layout.addLayout(search_layout)

        # Track list (card-style with thumbnails)
        self.track_list = QListWidget()
        self.track_list.setStyleSheet("""
            QListWidget::item { 
                border: 1px solid #ccc; 
                padding: 5px; 
                margin: 2px; 
                background-color: #f0f0f0; 
            }
            QListWidget::item:selected { 
                background-color: #d0d0d0; 
            }
        """)
        self.track_list.setIconSize(QSize(50, 50))
        main_layout.addWidget(self.track_list)

        # Playlist and account buttons
        bottom_layout = QHBoxLayout()
        self.open_button = QPushButton("Open Local Files")
        bottom_layout.addWidget(self.open_button)
        self.save_button = QPushButton("Save Playlist")
        bottom_layout.addWidget(self.save_button)
        self.load_button = QPushButton("Load Playlist")
        bottom_layout.addWidget(self.load_button)
        main_layout.addLayout(bottom_layout)

        # Playlist widget (downloaded files)
        self.playlist_widget = QListWidget()
        self.playlist_widget.setMaximumHeight(100)
        main_layout.addWidget(self.playlist_widget)

    def add_item(self, text):
        """Add an item to the track list with card-like styling."""
        item = QListWidgetItem(text)
        item.setSizeHint(QSize(0, 60))  # Card height
        self.track_list.addItem(item)
        return item

# ui.py
"""UI module: Dressing up TuneBlaster 3000 in style."""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSlider, QListWidget, QHBoxLayout, QLineEdit, QLabel
from PyQt5.QtCore import Qt, QSize
from player import VisualizerWidget

class TuneBlasterUI:
    """UI handler: Making our player look good and play nice."""
    def __init__(self, parent):
        self.parent = parent

    def setup_ui(self):
        """Build the interface with a Spotify-like layout."""
        main_widget = QWidget(self.parent)
        self.parent.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Sidebar (Your Library)
        sidebar = QVBoxLayout()
        sidebar_widget = QWidget()
        sidebar_widget.setFixedWidth(200)
        sidebar_widget.setStyleSheet("background-color: #121212; color: white;")
        sidebar.setContentsMargins(10, 10, 10, 10)

        library_label = QLabel("Your Library")
        library_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        sidebar.addWidget(library_label)

        self.playlist_widget = QListWidget()
        self.playlist_widget.setStyleSheet("background-color: #1a1a1a; color: white; border: none;")
        sidebar.addWidget(self.playlist_widget)

        sidebar.addStretch()
        sidebar_widget.setLayout(sidebar)
        main_layout.addWidget(sidebar_widget)

        # Main content area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search YouTube (press Enter)...")
        self.search_input.setStyleSheet("background-color: #2a2a2a; color: white; padding: 5px; border-radius: 5px;")
        search_layout.addWidget(self.search_input)
        self.fetch_button = QPushButton("Browse YouTube")
        self.fetch_button.setStyleSheet("background-color: #1db954; color: white; padding: 5px; border-radius: 5px;")
        search_layout.addWidget(self.fetch_button)
        content_layout.addLayout(search_layout)

        # Track grid (like Spotify's "Good Morning" section)
        grid_label = QLabel("Discover Music")
        grid_label.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        content_layout.addWidget(grid_label)

        self.track_grid = QListWidget()
        self.track_grid.setStyleSheet("""
            QListWidget {
                background-color: #1a1a1a;
                color: white;
                border: none;
            }
            QListWidget::item {
                padding: 10px;
                border: 1px solid #2a2a2a;
                border-radius: 5px;
            }
            QListWidget::item:hover {
                background-color: #2a2a2a;
            }
        """)
        self.track_grid.setFlow(QListWidget.LeftToRight)
        self.track_grid.setWrapping(True)
        self.track_grid.setResizeMode(QListWidget.Adjust)
        self.track_grid.setIconSize(QSize(100, 100))
        self.track_grid.setFixedHeight(400)
        content_layout.addWidget(self.track_grid)

        # Now playing and controls
        now_playing_layout = QVBoxLayout()
        self.now_playing_label = QLabel("Now Playing: None")
        self.now_playing_label.setStyleSheet("color: white; font-size: 14px;")
        now_playing_layout.addWidget(self.now_playing_label)

        self.visualizer = VisualizerWidget()
        self.visualizer.setFixedHeight(50)
        now_playing_layout.addWidget(self.visualizer)

        controls_layout = QHBoxLayout()
        self.play_button = QPushButton("Play")
        self.play_button.setStyleSheet("background-color: #1db954; color: white; padding: 5px; border-radius: 5px;")
        controls_layout.addWidget(self.play_button)
        self.seek_slider = QSlider(Qt.Horizontal)
        self.seek_slider.setMinimum(0)
        self.seek_slider.setMaximum(1000)
        self.seek_slider.setStyleSheet("background-color: #2a2a2a; color: white;")
        controls_layout.addWidget(self.seek_slider)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)
        self.volume_slider.setStyleSheet("background-color: #2a2a2a; color: white;")
        controls_layout.addWidget(self.volume_slider)
        self.open_button = QPushButton("Open Local Files")
        self.open_button.setStyleSheet("background-color: #1db954; color: white; padding: 5px; border-radius: 5px;")
        controls_layout.addWidget(self.open_button)
        now_playing_layout.addLayout(controls_layout)

        # Account buttons
        account_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Playlist")
        self.save_button.setStyleSheet("background-color: #1db954; color: white; padding: 5px; border-radius: 5px;")
        account_layout.addWidget(self.save_button)
        self.load_button = QPushButton("Load Playlist")
        self.load_button.setStyleSheet("background-color: #1db954; color: white; padding: 5px; border-radius: 5px;")
        account_layout.addWidget(self.load_button)
        now_playing_layout.addLayout(account_layout)

        content_layout.addLayout(now_playing_layout)
        content_layout.addStretch()
        content_widget.setStyleSheet("background-color: #181818;")
        main_layout.addWidget(content_widget)

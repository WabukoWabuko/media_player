# ui.py
"""UI module: Dressing up TuneBlaster 3000 in style."""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSlider, QListWidget, QHBoxLayout, QLineEdit
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt

class TuneBlasterUI:
    """UI handler: Making our player look good and play nice."""
    def __init__(self, parent):
        self.parent = parent

    def setup_ui(self):
        """Build the interface, rolling out the red carpet for controls."""
        # Central widget and main layout
        main_widget = QWidget(self.parent)
        self.parent.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Video display
        self.video_display = QVideoWidget()
        main_layout.addWidget(self.video_display)

        # Streaming input layout
        stream_layout = QHBoxLayout()
        self.stream_input = QLineEdit()
        self.stream_input.setPlaceholderText("Enter stream URL (e.g., http://example.com/stream.mp3)")
        stream_layout.addWidget(self.stream_input)
        self.stream_button = QPushButton("Load Stream")
        stream_layout.addWidget(self.stream_button)
        main_layout.addLayout(stream_layout)

        # Controls layout
        controls_layout = QHBoxLayout()
        self.play_button = QPushButton("Play")
        controls_layout.addWidget(self.play_button)
        self.seek_slider = QSlider(Qt.Horizontal)
        self.seek_slider.setMinimum(0)
        self.seek_slider.setMaximum(1000)  # Updated dynamically
        controls_layout.addWidget(self.seek_slider)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)
        controls_layout.addWidget(self.volume_slider)
        self.open_button = QPushButton("Open Files")
        controls_layout.addWidget(self.open_button)
        main_layout.addLayout(controls_layout)

        # Playlist widget
        self.playlist_widget = QListWidget()
        main_layout.addWidget(self.playlist_widget)

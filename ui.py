# ui.py
"""UI module: Dressing up TuneBlaster 3000 in style."""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt5.QtMultimediaWidgets import QVideoWidget  # Fixed import!

class TuneBlasterUI:
    """UI handler: Making our player look good and play nice."""
    def __init__(self, parent):
        self.parent = parent

    def setup_ui(self):
        """Build the interface, rolling out the red carpet for controls."""
        # Central widget and layout
        main_widget = QWidget(self.parent)
        self.parent.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Video display area
        self.video_display = QVideoWidget()
        layout.addWidget(self.video_display)

        # Play/Pause button
        self.play_button = QPushButton("Play")
        layout.addWidget(self.play_button)

        # Open file button
        self.open_button = QPushButton("Open File")
        layout.addWidget(self.open_button)

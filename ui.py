# ui.py
"""UI module: Making this player look snazzy and functional."""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QVideoWidget

class PlayerUI:
    """UI class: The face of our media player, ready to dazzle."""
    def __init__(self, parent):
        self.parent = parent

    def setup_ui(self):
        """Set up the UI, laying out the red carpet for our controls."""
        central_widget = QWidget(self.parent)
        self.parent.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        self.video_widget = QVideoWidget()
        layout.add_widget(self.video_widget)
        self.play_btn = QPushButton("Play")
        layout.add_widget(self.play_btn)
        self.open_btn = QPushButton("Open File")
        layout.add_widget(self.open_btn)

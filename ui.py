# ui.py
# The fancy suit our media player wears - all style, no fuss

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSlider, QFileDialog
from PyQt6.QtCore import Qt

class PlayerUI(QWidget):
    """UI class that makes our player look good and work smooth."""
    def __init__(self, parent, player_logic):
        super().__init__(parent)
        self.player_logic = player_logic
        self.parent = parent

        # Set up the layout - vertical stack for simplicity
        self.layout = QVBoxLayout(self)

        # Video widget placeholder (we’ll add it later for video support)
        self.layout.addStretch()  # Placeholder for video area

        # Play/Pause button - the heart of the action
        self.play_btn = QPushButton("Play/Pause")
        self.play_btn.clicked.connect(self.player_logic.toggle_play)
        self.layout.addWidget(self.play_btn)

        # Seek slider - slide into your favorite part
        self.seek_slider = QSlider(Qt.Orientation.Horizontal)
        self.seek_slider.sliderMoved.connect(self.player_logic.set_position)
        self.layout.addWidget(self.seek_slider)

        # Open file button - let’s pick some bangers
        self.open_btn = QPushButton("Open File")
        self.open_btn.clicked.connect(self.open_file)
        self.layout.addWidget(self.open_btn)

    def open_file(self):
        """Pop open a file dialog and play the chosen file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self.parent, "Pick a Tune or Flick", "",
            "Media Files (*.mp3 *.wav *.mp4 *.avi);;All Files (*)"
        )
        if file_path:
            self.player_logic.play_media(file_path=file_path)

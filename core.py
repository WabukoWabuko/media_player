# core.py
"""Core module: The heart of our epic media player."""
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
from ui import PlayerUI
from player import MediaPlayerBackend

class MediaPlayerApp(QMainWindow):
    """Main app window, the grand maestro of our media symphony."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TuneBlaster 3000")
        self.setGeometry(100, 100, 600, 400)
        self.backend = MediaPlayerBackend(self)
        self.ui = PlayerUI(self)
        self.ui.setup_ui()
        self.ui.play_btn.clicked.connect(self.backend.toggle_play)
        self.ui.open_btn.clicked.connect(self.backend.open_media)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MediaPlayerApp()
    window.show()
    sys.exit(app.exec_())

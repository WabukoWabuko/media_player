# test.py
# A quick sanity check to see if PyQt6 is feeling groovy

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtMultimedia import QMediaPlayer
import sys

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("PyQt6 Vibe Check")
window.resize(400, 300)
player = QMediaPlayer(window)  # Test QtMultimedia
window.show()
sys.exit(app.exec())

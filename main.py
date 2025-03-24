# main.py
# The grand entrance to our media player empire!

import sys
from PyQt6.QtWidgets import QApplication
from core import MediaPlayerApp

if __name__ == "__main__":
    # Fire up the Qt engine, ready to rock all OSes
    app = QApplication(sys.argv)
    # Summon the main window like a boss
    window = MediaPlayerApp()
    window.show()
    # Let the show begin (and exit cleanly when done)
    sys.exit(app.exec())

# main.py
"""Entry point: Let’s get this party started!"""
from core import MediaPlayerApp
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MediaPlayerApp()
    window.show()
    sys.exit(app.exec_())

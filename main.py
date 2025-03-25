# main.py
"""Entry point: Kicking off TuneBlaster 3000 with a bang!"""

from core import TuneBlasterApp
from PyQt5.QtWidgets import QApplication
import sys

def main():
    """Launch the app, let’s get this show on the road!"""
    app = QApplication(sys.argv)
    window = TuneBlasterApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

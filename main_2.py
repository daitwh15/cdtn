from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import *
from homeScreen0 import Ui_MainWindow
import sys

class MusicPlayer(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.window = QMainWindow()
        self.setupUi(self)
        self.load_song()
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MusicPlayer()
    sys.exit(app.exec())
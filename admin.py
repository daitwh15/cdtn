from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from untitled2 import Ui_MainWindow
import sys

class AdminWork(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.window = QMainWindow()
        self.setupUi(self)
        self.show()
        
app = QApplication(sys.argv)
app.setStyle('Fusion')
window = AdminWork()
sys.exit(app.exec())

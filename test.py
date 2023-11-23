from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import QDate, Qt

date = QDate.currentDate()

print(date.toString(Qt.ISODate))
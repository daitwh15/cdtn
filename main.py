import sys
import re
import typing
import requests
import os
from PyQt5 import QtCore, QtWidgets, uic, QtNetwork, QtGui
from PyQt5.QtGui import QPixmap
# from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QMainWindow, QWidget, QMessageBox, QTableWidget, QVBoxLayout, QTableWidgetItem,QLabel
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi 
from PyQt5.QtMultimedia import QAudioOutput, QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl,QTime
import MySQLdb as mdb
from io import BytesIO

# log in screen
class loginScreen(QMainWindow):
    def __init__(self):
        super(loginScreen,self).__init__()
        uic.loadUi("login.ui",self)
        self.loginBtn.clicked.connect(self.login)
        self.signupBtn.clicked.connect(self.register)
        self.forgotPsw.clicked.connect(self.forgotPassword)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

    def login(self):
        username = self.username.text()
        password = self.password.text()
        
        db = mdb.connect('localhost','root','','user_db')
        query = db.cursor()
        query.execute("SELECT * FROM `user_management` WHERE username = '"+username+"' and password = '"+password+"' ")

        check = query.fetchone()
        if check:
            QMessageBox.information(self, "Chào mừng bạn đến với TwoCD","Đăng nhập thành công")
            widget.setCurrentWidget(mainPageLogged)
        else:
            QMessageBox.information(self, "Lỗi", "Đăng nhập thất bại. Vui lòng kiểm tra lại tài khoản hoặc mật khẩu!")
        # if len(username) == 0 or len(password) == 0:
        #     QMessageBox.information(self, "Lỗi", "Vui lòng điền đầy đủ các thông tin!")

    def register(self):
        widget.setCurrentWidget(signup)

    def forgotPassword(self):
        QMessageBox.information(self,"Lỗi", "In development")

# sign up screen
class registerScreen(QMainWindow):
    def __init__(self):
        super(registerScreen,self).__init__()
        uic.loadUi("signup.ui",self)
        self.loginBtn.clicked.connect(self.login)
        self.signupBtn.clicked.connect(self.signup)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

    def login(self):
        widget.setCurrentWidget(login)

    def signup(self):
        email = self.email.text()
        username = self.username.text()
        password = self.password.text()

        db = mdb.connect('localhost','root','','user_db')
        query = db.cursor()
        query.execute("SELECT * FROM `user_management` WHERE username = '"+username+"' and password = '"+password+"' ")
        check = query.fetchone()
        if check:
            QMessageBox.information(self,"Lỗi", "Đăng ký thất bại. Vui lòng kiểm tra lại!")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            QMessageBox.information(self, "Lỗi", "Tài khoản hoặc mật khẩu không hợp lệ!")
        else:
            query.execute("INSERT INTO `user_management` (`username`, `email`, `password`) VALUES ('"+username+"', '"+email+"', '"+password+"')")
            db.commit()
            QMessageBox.information(self, "Chào mừng bạn đến với TwoCD", "Dang ki thanh cong")
            widget.setCurrentWidget(login)
        # if len(email) == 0 or len(username) == 0 or len(password) == 0:
        #     QMessageBox.information(self, "Lỗi", "Vui lòng điền đầy đủ các thông tin!")

#  main page for unlogged in user
class unLoggedMainPage(QMainWindow):
    def __init__(self):
        super(unLoggedMainPage,self).__init__()
        uic.loadUi("main_page_unlogged.ui",self)
        self.login_btn.clicked.connect(self.goToLogin)
        self.signup_btn.clicked.connect(self.goToSignup)

        self.icon_only_widget.hide()
        self.home_btn_2.setChecked(True)
        self.stacked_widget.setCurrentIndex(0)
        self.home_btn.clicked.connect(self.showHome)
        self.home_btn_2.clicked.connect(self.showHome)
        self.library_btn.clicked.connect(self.showLibrary)
        self.library_btn_2.clicked.connect(self.showLibrary)
        
        self.text.setText('Chung an cut')
        self.listWidget.addItem('The Anh')
        self.listWidget.addItem('Chung')


    def showHome(self):
        self.stacked_widget.setCurrentIndex(0)

    def showLibrary(self):
        self.stacked_widget.setCurrentIndex(1) 

    def goToLogin(self):
        widget.setCurrentWidget(login)

    def goToSignup(self):
        widget.setCurrentWidget(signup)
# main page for logged in user
class loggedMainPage(QMainWindow):
    def __init__(self):
        super(loggedMainPage,self).__init__() 
        uic.loadUi("main_page_logged.ui",self)
        self.accountBtn.clicked.connect(self.goToProfile)


        # Show data-----------------

        self.layout = QVBoxLayout()

        db = mdb.connect('localhost','root','','user_db')
        query = db.cursor()
        query.execute("SELECT * FROM `baihat`")
        check = query.fetchall()

        self.tableWidget1.setRowCount(len(check)) ##set number of rows
        self.tableWidget1.setColumnCount(6)

        row = 0
        while True:
            sqlRow = query.fetchone()
            if sqlRow == None:
                break ##stops while loop if there is no more lines in sql table
            for col in range(0, 6): ##otherwise add row into tableWidget
                self.tableWidget1.setItem(row, col, QtGui.QTableWidgetItem(sqlRow[col]))
            row += 1
        
        # ten1 = QLabel()
        # ten1 = self.label_3.setText(f"{check[1]}")
        # casi = self.label_4.setText(f"{check[2]}")
        # my_string = check[4]
        # new_string = my_string[:-2]
        # print(new_string)
        
        # response = requests.get(new_string)
        # print(response)
        # image_data = BytesIO(response.content)
        # pixmap = QPixmap()
        # pixmap.loadFromData(image_data.getvalue())

        # image_label = self.label_2.setPixmap(pixmap)
        
        # self.layout.addWidget(image_label)

        # response = requests.get(new_string)
        # print(response)
        # image_data = BytesIO(response.content)
        # pixmap = QPixmap()
        # pixmap.loadFromData(image_data.getvalue())

        # image_label = self.label_2.setPixmap(pixmap)
        
        # self.layout.addWidget(image_label)
        
       

        # self.layout.addWidget(ten1)
        # self.layout.addWidget(casi)
        # # self.layout.addWidget(anh)
        # self.setLayout(self.layout)

       
       #Play Music--------------------
        # self.toolButtonPlay.setEnabled(False) 
        
        self.player = QMediaPlayer()
        # self.audio = QAudioOutput()

        # self.player.setAudioOutput(self.audio)

        # self.actionOpen_Music.triggered.connect(self.open_music)
        self.toolButtonPlay.clicked.connect(self.play_music)

        # self.player.positionChanged.connect(self.position_changed)
        # self.player.durationChanged.connect(self.duration_changed)

    # def open_music(self):
    #     # fileName= QFileDialog.getOpenFileName(self, "Open Music")
    #     fileName = "C:/Users/ADMIN/Downloads/TroiGiauTroiMangDi"
    #     if fileName != '' :
    #         self.player.setSource(QUrl.fromLocalFile(fileName))
    #         self.toolButtonPlay.setEnabled(True)

    def play_music(self):
        file = os.path.join(os.getcwd(), 'C:/Users/ADMIN/Downloads/TroiGiauTroiMangDi.mp3')
        url = QUrl.fromLocalFile(file)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()

    # def position_changed(self, position):
    #     if(self.horizontalSliderPlay.maximum() != self.player.duration()):
    #         self.horizontalSliderPlay.setMaximum(self.player.duration())

    #     self.horizontalSliderPlay.setValue(position)

    #     seconds = (position / 1000) % 60
    #     minutes = (position / 60000) % 60
    #     hours = (position / 2600000) % 24

    #     time = QTime(hours, minutes, seconds)
    #     self.labelTimer.setText(time.toString())

    # def duration_changed(self, duration):
    #     self.horizontalSliderPlay.setRange(0, duration)

    def goToProfile(self):
        widget.setCurrentWidget(profile)

# profile
class profileScreen(QMainWindow):
    def __init__(self):
        super(profileScreen, self).__init__()
        uic.loadUi("profile.ui",self)
        self.pushButton_6.clicked.connect(self.goToMC)
        self.pushButton_4.clicked.connect(self.goToMain)

    def goToMain(self):
         widget.setCurrentWidget(mainPageLogged)

    def goToMC(self):
         widget.setCurrentWidget(mainPage)

        # self.pushButton_4.clicked.connect(self.goToMain)
        # self.logOutBtn.clicked.connect(self.goToLogin)
    # def goToMain(self):
    #     widget.setCurrentWidget(mainPageLogged)
    # def goToLogin(self):
    #     widget.setCurrentWidget(login)

# run
app = QApplication(sys.argv)
login = loginScreen()
signup = registerScreen()
mainPage = unLoggedMainPage()
mainPageLogged = loggedMainPage()
profile = profileScreen()
widget = QStackedWidget()
widget.addWidget(login)
widget.addWidget(signup)
widget.addWidget(mainPage)
widget.addWidget(mainPageLogged)
widget.addWidget(profile)
widget.setCurrentWidget(mainPage)
widget.setFixedWidth(1440)
widget.setFixedHeight(920)
widget.show()

sys.exit(app.exec())
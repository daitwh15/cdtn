import sys
import re
import typing
import requests
import os
import time
from PyQt5 import QtMultimedia
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5 import QtCore, QtWidgets, uic, QtNetwork, QtGui
from PyQt5.QtGui import QPixmap
# from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QMainWindow, QWidget, QMessageBox, QTableWidget, QVBoxLayout, QTableWidgetItem,QLabel
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi 
from PyQt5.QtMultimedia import QAudioOutput, QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QTime, Qt
import MySQLdb as mdb
from io import BytesIO

# log in screen
# class loginScreen(QMainWindow):
#     def __init__(self):
#         super(loginScreen,self).__init__()
#         uic.loadUi("login.ui",self)
#         self.loginBtn.clicked.connect(self.login)
#         self.signupBtn.clicked.connect(self.register)
#         self.forgotPsw.clicked.connect(self.forgotPassword)
#         self.password.setEchoMode(QtWidgets.QLineEdit.Password)

#     def login(self):
#         logon = self.logon.text()
#         password = self.password.text()
        
#         db = mdb.connect('localhost','root','','music_app_db')
#         queryUsername = db.cursor()
#         queryEmail = db.cursor()
#         get_role = db.cursor()
#         get_id = db.cursor()
#         queryUsername.execute("SELECT * FROM `account_management` WHERE username = '"+logon+"' and password = '"+password+"'")
#         get_role.execute("SELECT `role` FROM `account_management` WHERE username = '"+logon+"'")
#         get_id.execute("SELECT `id` FROM `account_management` WHERE username = '"+logon+"'")
        
#         login_by_username = queryUsername.fetchone()
#         get_user_id = get_id.fetchone()
#         role = get_role.fetchone()


#         print(str(len(logon)) + " " + str(len(password)))
#         if login_by_username:
#             for i in get_user_id:
#                 self.thread = profileScreen(index = i)
#             for j in role:
#                 self.thread = loggedMainPage(index2 = j)
#             widget.setCurrentWidget(mainPageLogged)
#         else:
#             if len(logon) == 0:
#                 QMessageBox.information(self, "Login fail!", "Email address or username is required!")
#             elif len(password) == 0:
#                 QMessageBox.information(self, "Login fail!", "Password is required!")
#             elif len(password) > 16:
#                 QMessageBox.information(self, "Login fail!", "Password must be less than 16 characters!")
#             else:
#                 QMessageBox.information(self, "Login fail!", "Username, email address or password is incorrect!")
#     def register(self):
#         widget.setCurrentWidget(signup)

#     def forgotPassword(self):
#         QMessageBox.information(self,"Lỗi", "In development")

# sign up screen
# class registerScreen(QMainWindow):
#     def __init__(self):
#         super(registerScreen,self).__init__()
#         uic.loadUi("signup.ui",self)
#         self.loginBtn.clicked.connect(self.login)
#         self.signupBtn.clicked.connect(self.signup)
#         self.password.setEchoMode(QtWidgets.QLineEdit.Password)
#         self.password_again.setEchoMode(QtWidgets.QLineEdit.Password)

#     def login(self):
#         widget.setCurrentWidget(login)

#     def signup(self):
#         role = 1
#         username = self.username.text()
#         email = self.email.text()
#         password = self.password.text()
#         retype_password = self.password_again.text()

#         # if email == 'admin@gmail.com' and password == 'admin':
#         #     role = 0
#         # else:
#         #     role = 1

#         db = mdb.connect('localhost','root','','music_app_db')
#         query = db.cursor()
#         query.execute("SELECT * FROM `account_management` WHERE username = '"+username+"' and email = '"+email+"' and password = '"+password+"'")
#         account_check = query.fetchone()

#         if account_check:
#             QMessageBox.information(self, "Register fail!", "This account has already exists!")
#         elif len(username) == 0:
#             QMessageBox.information(self, "Register fail!", "Username is required!")
#         elif len(email) == 0:
#             QMessageBox.information(self, "Register fail!", "Email is required!")
#         elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
#             QMessageBox.information(self, "Register fail!", "Your email address is invalid!")
#         elif len(password) == 0:
#             QMessageBox.information(self, "Register fail!", "Password is required!")
#         elif len(password) > 16:
#             QMessageBox.information(self, "Register fail!", "Password must be less than 16 characters!")
#         elif password != retype_password:
#             QMessageBox.information(self, "Register fail!", "Passwords do not match!")
#         else:
#             query.execute("INSERT INTO `account_management` (`username`, `email`, `password`, `role`) VALUES ('"+username+"', '"+email+"', '"+password+"', '"+str(role)+"')")
#             db.commit()
#             QMessageBox.information(self, "Welcome!", "Sign up success!")
#             widget.setCurrentWidget(login)

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

        self.current_songs = []
        self.current_volume = 50

        self.player = QtMultimedia.QMediaPlayer()
        self.player.setVolume(self.current_volume)

        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.move_slider)

        self.music_btn.hide()
        self.listWidget.currentItemChanged.connect(self.show_btn)
        self.music_slider.sliderMoved[int].connect(lambda: self.player.setPosition(self.music_slider.value()))
        self.volume_slider.sliderMoved[int].connect(lambda: self.volume_changed())
        self.add_music_btn.clicked.connect(self.add_songs)
        # self.actionRemove_Selected.triggered.connect(self.remove_one_song)
        # self.actionRemove_All.triggered.connect(self.remove_all_songs)
        self.play_btn.clicked.connect(self.play_song)
        self.pause_btn.clicked.connect(self.pause_and_unpause)
        self.next_btn.clicked.connect(self.next_song)
        self.previous_btn.clicked.connect(self.previous_song)
        self.stop_btn.clicked.connect(self.stop_song)

    def show_btn(self):
        self.music_btn.show()

    def move_slider(self):
        # Update the slider
        if self.player.state() == QMediaPlayer.PlayingState:
            self.music_slider.setMinimum(0)
            self.music_slider.setMaximum(self.player.duration())
            slider_position = self.player.position()
            self.music_slider.setValue(slider_position)

            current_time = time.strftime('%M:%S', time.localtime(self.player.position() / 1000))
            song_duration = time.strftime('%M:%S', time.localtime(self.player.duration() / 1000))
            self.start_time_label.setText(f"{current_time}")
            self.end_time_label.setText(f"{song_duration}")

    def add_songs(self):
        # db = mdb.connect('localhost','root','','user_db')
        # get_songs = db.cursor()
        # get_link = get_songs.execute("SELECT * FROM `song_management`")
        # print(str(get_link))
        files, _ = QFileDialog.getOpenFileNames(
            self, caption='Add Songs',
            directory=':\\', filter="Supported Files (*.mp3;*.mpeg;*.ogg;*.m4a;*.MP3;*.wma;*.acc;*.amr)"
        )
        if files:
            for file in files:
                self.current_songs.append(file)
                self.listWidget.addItem(os.path.basename(file))

    def play_song(self):
        try:
            global stopped
            stopped = False

            current_selection = self.listWidget.currentRow()
            current_song = self.current_songs[current_selection]

            song_url = QMediaContent(QUrl.fromLocalFile(current_song))
            self.player.setMedia(song_url)
            self.player.play()
            self.move_slider()
        except Exception as e:
            print(f"Play song error: {e}")

    def pause_and_unpause(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def stop_song(self):
        self.player.stop()
        self.music_slider.setValue(0)
        self.start_time_label.setText(f"00:00")
        self.end_time_label.setText(f"00:00")

    def next_song(self):
        try:
            current_selection = self.listWidget.currentRow()

            if current_selection + 1 == len(self.current_songs):
                next_index = 0
            else:
                next_index = current_selection + 1
            current_song = self.current_songs[next_index]
            self.listWidget.setCurrentRow(next_index)
            song_url = QMediaContent(QUrl.fromLocalFile(current_song))
            self.player.setMedia(song_url)
            self.player.play()
            self.move_slider()
        except Exception as e:
            print(f"Next song error: {e}")

    def previous_song(self):
        try:
            current_selection = self.listWidget.currentRow()

            if current_selection == 0:
                previous_index = len(self.current_songs) - 1
            else:
                previous_index = current_selection - 1

            current_song = self.current_songs[previous_index]
            self.listWidget.setCurrentRow(previous_index)
            song_url = QMediaContent(QUrl.fromLocalFile(current_song))
            self.player.setMedia(song_url)
            self.player.play()
            self.move_slider()
        except Exception as e:
            print(f"Previous song error: {e}")

    def volume_changed(self):
        try:
            self.current_volume = self.volume_slider.value()
            self.player.setVolume(self.current_volume)
        except Exception as e:
            print(f"Changing volume error: {e}")      

    def showHome(self):
        db = mdb.connect('localhost','root','','user_db')
        
        # get_songs = db.cursor()
        # get_songs.execute("SELECT `TenBH` FROM `baihat`")
        
        get_link = db.cursor()
        get_link.execute("SELECT `Link` FROM `baihat`")
        
        link = get_link.fetchall()
        # result = get_songs.fetchall()
        
        # Chuyển danh sách các kết quả thành danh sách tên bài hát
        # song_names = [row[0] for row in result]
        
        song_link = [row[0] for row in link]
        # Chuyển danh sách tên bài hát thành chuỗi
        unique_items = []

        # for item in song_names:
        #     if item not in unique_items:
        #         unique_items.append(item)
        # print(unique_items)
        self.listWidget.clear()
        #self.current_songs.clear()
        # for song_name in unique_items:
            # self.listWidget.addItem(song_name)
        for link_value in song_link:
            self.current_songs.append(link_value)
        
        self.stacked_widget.setCurrentIndex(0)

    def showLibrary(self):
        self.stacked_widget.setCurrentIndex(1) 

    def goToLogin(self):
        # self.stop_song()
        widget.setCurrentWidget(login)

    def goToSignup(self):
        # self.stop_song()
        widget.setCurrentWidget(signup)
        
# main page for logged in user
class loggedMainPage(QMainWindow):
    def __init__(self, index2 = 0):
        super(loggedMainPage,self).__init__() 
        uic.loadUi("main_page_2.ui",self)
        self.account_btn.clicked.connect(self.goToProfile)

        self.role = index2
        print('Role: ' + str(self.role))
        if self.role == 1:
            self.add_music_btn.setEnabled(True)
        # else:
        #     self.add_music_btn.setEnabled(False)

        self.icon_only_widget.hide()
        self.home_btn_2.setChecked(True)
        self.stacked_widget.setCurrentIndex(0)
        self.home_btn.clicked.connect(self.showHome)
        self.home_btn_2.clicked.connect(self.showHome)
        self.library_btn.clicked.connect(self.showLibrary)
        self.library_btn_2.clicked.connect(self.showLibrary)

        self.current_songs = []
        self.current_volume = 50

        self.player = QtMultimedia.QMediaPlayer()
        self.player.setVolume(self.current_volume)

        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.move_slider)

        self.music_btn.hide()
        self.listWidget.currentItemChanged.connect(self.show_btn)
        self.music_slider.sliderMoved[int].connect(lambda: self.player.setPosition(self.music_slider.value()))
        self.volume_slider.sliderMoved[int].connect(lambda: self.volume_changed())
        self.add_music_btn.clicked.connect(self.add_songs)
        # self.actionRemove_Selected.triggered.connect(self.remove_one_song)
        # self.actionRemove_All.triggered.connect(self.remove_all_songs)
        self.play_btn.clicked.connect(self.play_song)
        self.pause_btn.clicked.connect(self.pause_and_unpause)
        self.next_btn.clicked.connect(self.next_song)
        self.previous_btn.clicked.connect(self.previous_song)
        self.stop_btn.clicked.connect(self.stop_song)

    def show_btn(self):
        self.music_btn.show()

    def move_slider(self):
        # Update the slider
        if self.player.state() == QMediaPlayer.PlayingState:
            self.music_slider.setMinimum(0)
            self.music_slider.setMaximum(self.player.duration())
            slider_position = self.player.position()
            self.music_slider.setValue(slider_position)

            current_time = time.strftime('%M:%S', time.localtime(self.player.position() / 1000))
            song_duration = time.strftime('%M:%S', time.localtime(self.player.duration() / 1000))
            self.start_time_label.setText(f"{current_time}")
            self.end_time_label.setText(f"{song_duration}")

    def add_songs(self):
        # db = mdb.connect('localhost','root','','user_db')
        # get_songs = db.cursor()
        # get_link = get_songs.execute("SELECT * FROM `song_management`")
        # print(str(get_link))
        files, _ = QFileDialog.getOpenFileNames(
            self, caption='Add Songs',
            directory=':\\', filter="Supported Files (*.mp3;*.mpeg;*.ogg;*.m4a;*.MP3;*.wma;*.acc;*.amr)"
        )
        if files:
            for file in files:
                self.current_songs.append(file)
                self.listWidget.addItem(os.path.basename(file))

    def play_song(self):
        try:
            global stopped
            stopped = False

            current_selection = self.listWidget.currentRow()
            current_song = self.current_songs[current_selection]

            song_url = QMediaContent(QUrl.fromLocalFile(current_song))
            self.player.setMedia(song_url)
            self.player.play()
            self.move_slider()
        except Exception as e:
            print(f"Play song error: {e}")

    def pause_and_unpause(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def stop_song(self):
        self.player.stop()
        self.music_slider.setValue(0)
        self.start_time_label.setText(f"00:00")
        self.end_time_label.setText(f"00:00")

    def next_song(self):
        try:
            current_selection = self.listWidget.currentRow()

            if current_selection + 1 == len(self.current_songs):
                next_index = 0
            else:
                next_index = current_selection + 1
            current_song = self.current_songs[next_index]
            self.listWidget.setCurrentRow(next_index)
            song_url = QMediaContent(QUrl.fromLocalFile(current_song))
            self.player.setMedia(song_url)
            self.player.play()
            self.move_slider()
        except Exception as e:
            print(f"Next song error: {e}")

    def previous_song(self):
        try:
            current_selection = self.listWidget.currentRow()

            if current_selection == 0:
                previous_index = len(self.current_songs) - 1
            else:
                previous_index = current_selection - 1

            current_song = self.current_songs[previous_index]
            self.listWidget.setCurrentRow(previous_index)
            song_url = QMediaContent(QUrl.fromLocalFile(current_song))
            self.player.setMedia(song_url)
            self.player.play()
            self.move_slider()
        except Exception as e:
            print(f"Previous song error: {e}")

    def volume_changed(self):
        try:
            self.current_volume = self.volume_slider.value()
            self.player.setVolume(self.current_volume)
            # self.volume_label.setText(f"{self.current_volume}")
        except Exception as e:
            print(f"Changing volume error: {e}")      

    def showHome(self):
        self.stacked_widget.setCurrentIndex(0)

    def showLibrary(self):
        self.stacked_widget.setCurrentIndex(1) 

    def goToLogin(self):
        # self.stop_song()
        widget.setCurrentWidget(login)

    def goToSignup(self):
        # self.stop_song()
        widget.setCurrentWidget(signup)

        # Show data-----------------

    #     self.layout = QVBoxLayout()

    #     db = mdb.connect('localhost','root','','user_db')
    #     query = db.cursor()
    #     query.execute("SELECT * FROM `baihat`")
    #     check = query.fetchall()

    #     self.tableWidget1.setRowCount(len(check)) ##set number of rows
    #     self.tableWidget1.setColumnCount(6)

    #     row = 0
    #     while True:
    #         sqlRow = query.fetchone()
    #         if sqlRow == None:
    #             break ##stops while loop if there is no more lines in sql table
    #         for col in range(0, 6): ##otherwise add row into tableWidget
    #             self.tableWidget1.setItem(row, col, QtGui.QTableWidgetItem(sqlRow[col]))
    #         row += 1
        
    #     # ten1 = QLabel()
    #     # ten1 = self.label_3.setText(f"{check[1]}")
    #     # casi = self.label_4.setText(f"{check[2]}")
    #     # my_string = check[4]
    #     # new_string = my_string[:-2]
    #     # print(new_string)
        
    #     # response = requests.get(new_string)
    #     # print(response)
    #     # image_data = BytesIO(response.content)
    #     # pixmap = QPixmap()
    #     # pixmap.loadFromData(image_data.getvalue())

    #     # image_label = self.label_2.setPixmap(pixmap)
        
    #     # self.layout.addWidget(image_label)

    #     # response = requests.get(new_string)
    #     # print(response)
    #     # image_data = BytesIO(response.content)
    #     # pixmap = QPixmap()
    #     # pixmap.loadFromData(image_data.getvalue())

    #     # image_label = self.label_2.setPixmap(pixmap)
        
    #     # self.layout.addWidget(image_label)
        
       

    #     # self.layout.addWidget(ten1)
    #     # self.layout.addWidget(casi)
    #     # # self.layout.addWidget(anh)
    #     # self.setLayout(self.layout)

       
    #    #Play Music--------------------
    #     # self.toolButtonPlay.setEnabled(False) 
        
    #     self.player = QMediaPlayer()
    #     # self.audio = QAudioOutput()

    #     # self.player.setAudioOutput(self.audio)

    #     # self.actionOpen_Music.triggered.connect(self.open_music)
    #     self.toolButtonPlay.clicked.connect(self.play_music)

        # self.player.positionChanged.connect(self.position_changed)
        # self.player.durationChanged.connect(self.duration_changed)

    # def open_music(self):
    #     # fileName= QFileDialog.getOpenFileName(self, "Open Music")
    #     fileName = "C:/Users/ADMIN/Downloads/TroiGiauTroiMangDi"
    #     if fileName != '' :
    #         self.player.setSource(QUrl.fromLocalFile(fileName))
    #         self.toolButtonPlay.setEnabled(True)

    # def play_music(self):
    #     file = os.path.join(os.getcwd(), 'C:/Users/ADMIN/Downloads/TroiGiauTroiMangDi.mp3')
    #     url = QUrl.fromLocalFile(file)
    #     content = QMediaContent(url)
    #     self.player.setMedia(content)
    #     self.player.play()

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
    def __init__(self, index = 0):
        super(profileScreen, self).__init__()
        uic.loadUi("test.ui",self)
        # self.pushButton_6.clicked.connect(self.goToMC)
        # self.pushButton_4.clicked.connect(self.goToMain)

        self.id = index
        print("Id: " + str(self.id))
        db = mdb.connect('localhost','root','','music_app_db')
        query = db.cursor()
        query.execute("SELECT username FROM `account_management` WHERE id = '"+str(self.id)+"'")
        username = query.fetchone()
        if username: 
            # print('Username: ' + str(username[0]))
            display = str(username[0])
            print("Username: " + display)

    def goToMain(self):
         widget.setCurrentWidget(mainPageLogged)

    def goToMC(self):
         widget.setCurrentWidget(mainPage)

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
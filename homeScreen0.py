import random
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import *
import MySQLdb as mdb
import songs
import time
import os

class Ui_MainWindow(object):
    def goToLogin(self):
        try:
            from loginScreen import Ui_LoginWindow
            self.login_window = QtWidgets.QMainWindow()
            self.ui = Ui_LoginWindow()
            self.ui.setupUi(self.login_window)
            self.login_window.show()
        except ImportError:
            pass

    def goToSignup(self):
        try:
            from signupScreen import Ui_SignupWindow
            self.signup_window = QtWidgets.QMainWindow()
            self.ui = Ui_SignupWindow()
            self.ui.setupUi(self.signup_window)
            self.signup_window.show()
        except ImportError:
            pass
        
    def load_song(self):
        self.free_song_list.clear()
        db = mdb.connect('localhost','root','','music_app_db')
        
        songs_name = db.cursor()
        songs_name.execute("SELECT song_management.name, artist_management.artist_name FROM `song_management` Join `artist_management` ON song_management.artist_id = artist_management.artist_id")
        
        query_name = songs_name.fetchall()
        names = [(row[0], row[1]) for row in query_name]
        
        for song in names:
            if song not in self.songs_name_list:
                self.songs_name_list.append(str(song))
        
        for song_tuple_str in self.songs_name_list:
            song_tuple = eval(song_tuple_str)
            
            song_name = song_tuple[0]
            artist_name = song_tuple[1]
            item = QListWidgetItem(f"{song_name} - {artist_name}")
            item_text = f"{song_name} - {artist_name}"
            item = QListWidgetItem(QIcon('resources3.qrc/music_icon.png'), item_text)
            self.free_song_list.addItem(item)
        
        songs_link = db.cursor()
        songs_link.execute("SELECT `link` FROM `song_management`")
        
        query_link = songs_link.fetchall()
        links = [row[0] for row in query_link]
        
        for link_value in links:
            self.current_songs.append(link_value)
            
        print(self.current_songs)
        
    def add_songs(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, caption='Add Songs', directory=':\\', 
            filter="Supported Files (*.mp3;*.mpeg;*.ogg;*.m4a;*.MP3;*.wma;*.acc;*.amr)"
        )

        if files:
            for file in files:
                self.current_songs.append(file)
                self.free_song_list.addItem(
                    QListWidgetItem(
                        QIcon('resources3.qrc/music_icon.png'),
                        os.path.basename(file)))
                 
    def show_btn(self):
        self.music_btn.show()

    def play_song(self):
        try:
            global stopped
            stopped = False

            current_selection = self.free_song_list.currentRow()
            current_song = self.current_songs[current_selection]

            song_url = QMediaContent(QUrl.fromLocalFile(current_song))
            self.player.setMedia(song_url)
            self.player.play()
            self.move_slider()
        except Exception as e:
            print(f"Play song error: {e}")
            
    def play_ads(self):
        music_path = 'ads/bugger.mp3'
        media_content = QMediaContent(QUrl.fromLocalFile(music_path))
        self.player.setMedia(media_content)
        self.player.play()
        
    def song_end(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.play_ads()

    def move_slider(self):
        if stopped:
            return
        else:
            if self.player.state() == QMediaPlayer.PlayingState:
                self.music_slider.setMinimum(0)
                self.music_slider.setMaximum(self.player.duration())
                slider_position = self.player.position()
                self.music_slider.setValue(slider_position)

                current_time = time.strftime('%M:%S', time.localtime(self.player.position() / 1000))
                song_duration = time.strftime('%M:%S', time.localtime(self.player.duration() / 1000))
                self.start_time_label.setText(f"{current_time}")
                self.end_time_label.setText(f"{song_duration}")

    def pause_and_unpause(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def stop_song(self):
        try:
            self.player.stop()
            self.music_slider.setValue(0)
            self.start_time_label.setText(f"00:00")
            self.end_time_label.setText(f"00:00")
            self.play_btn.isChecked(False)
        except Exception as e:
            print('Stopping song error: {e}')

    def default_next(self):
        try:
            current_media = self.player.media()
            current_song_url = current_media.canonicalUrl().path()[1:]
            current_song_index = self.current_songs.index(current_song_url)
            if current_song_index + 1 == len(self.current_songs):
                next_index = 0
            else:
                next_index = current_song_index + 1
            current_song = self.current_songs[next_index]
            self.free_song_list.setCurrentRow(next_index) 

            song_url = QMediaContent(QUrl.fromLocalFile(current_song))
            self.player.setMedia(song_url)
            self.player.play()
            self.move_slider()

        except Exception as e:
            print(f"Play song error: {e}")

    # def looped_next(self):
    #     try:
    #         current_media = self.player.media()
    #         current_song_url = current_media.canonicalUrl().path()[1:]
    #         current_song_index = self.current_songs.index(current_song_url)
    #         current_song = self.current_songs[current_song_index]
    #         self.free_song_list.setCurrentRow(current_song_index)     

    #         song_url = QMediaContent(QUrl.fromLocalFile(current_song))
    #         self.player.setMedia(song_url)
    #         self.player.play()
    #         self.move_slider()

    #     except Exception as e:
    #         print(f"Looped song error: {e}")

    # def shuffle_next(self):
    #     try:
    #         song_index = random.randint(0, len(self.current_songs))
    #         current_song = self.current_songs[song_index]
    #         self.free_song_list.setCurrentRow(song_index)     

    #         song_url = QMediaContent(QUrl.fromLocalFile(current_song))
    #         self.player.setMedia(song_url)
    #         self.player.play()
    #         self.move_slider()

    #     except Exception as e:
    #         print(f"Shuffled song error: {e}")

    def next_song(self):
        try:
            current_selection = self.free_song_list.currentRow()

            if current_selection + 1 == len(self.current_songs):
                next_index = 0
            else:
                next_index = current_selection + 1
            current_song = self.current_songs[next_index]
            self.free_song_list.setCurrentRow(next_index)
            song_url = QMediaContent(QUrl.fromLocalFile(current_song))
            self.player.setMedia(song_url)
            self.player.play()
            self.move_slider()
        except Exception as e:
            print(f"Next song error: {e}")

    def loop_one_song(self):
        try:
            global is_shuffled
            global looped

            if not looped:
                looped = True
                self.shuffle_btn.setEnabled(False)
            else:
                looped = False
                self.shuffle_btn.setEnabled(True)

        except Exception as e:
            print('Looping song error: {e}')

    def shuffled_playlist(self):
        try:
            global is_shuffled
            global looped

            if not is_shuffled:
                is_shuffled = True
                self.loop_btn.setEnabled(False)

            else:
                is_shuffled = False
                self.loop_btn.setEnabled(True)
        except Exception as e:
            print('Shuffle song error: {e}')

    def previous_song(self):
        try:
            current_selection = self.free_song_list.currentRow()

            if current_selection == 0:
                previous_index = len(self.current_songs) - 1
            else:
                previous_index = current_selection - 1

            current_song = self.current_songs[previous_index]
            self.free_song_list.setCurrentRow(previous_index)
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
            print(f"Volume change error: {e}")      

    def showHome(self):
        self.stacked_widget.setCurrentIndex(0)

    def playlistDisable(self):
        self.home_btn.setChecked(True)
        self.library_btn.setChecked(False)
        self.library_btn_2.setChecked(False)
        QMessageBox.information(None, "Login to continue", "Login to create playlists")
        
    def downloadDisable(self):
        self.home_btn.setChecked(True)
        self.pushButton_3.setChecked(False)
        self.pushButton_4.setChecked(False)
        QMessageBox.information(None, "Login to continue", "Login to open download")
            
    def showSearch(self):
        self.home_btn.setChecked(False)
        self.search_btn.setChecked(True)
        self.search_btn_2.setChecked(True)
        self.stacked_widget.setCurrentIndex(2)
        
        text = self.search_input.text()
        
        self.search_list.clear()
        db = mdb.connect('localhost','root','','music_app_db')
        query = db.cursor()
        query.execute("SELECT name FROM `song_management` WHERE name LIKE '"+ text +"%'")
        song = query.fetchall()
        found_song = [row[0] for row in song]
        
        if len(text) == 0:
            self.search_list.clear()
            songs.search_song_list.clear()
        else:
            for item in found_song:
                if item not in songs.search_song_list:
                    songs.search_song_list.append(item)
            for song_name in songs.search_song_list:
                self.search_list.addItem(
                    QListWidgetItem(
                    QIcon('resources3.qrc/music_icon.png'),
                    song_name))
                
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1337, 941)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("*{\n"
"border:none;\n"
"padding: 0px;\n"
"margin:0px;\n"
"color:#fff\n"
"}\n"
"\n"
"#centralwidget{\n"
"background-color: black;\n"
"}\n"
"\n"
"#icon_only_widget, #full_menu_widget, #main_widget{\n"
"background-color:#1f1f1f;\n"
"border-radius:6px\n"
"}\n"
"\n"
"#icon_only_widget QPushButton {\n"
"border:none;\n"
"padding:10px 30px;\n"
"border-radius:10px\n"
"}\n"
"\n"
"#icon_only_widget QPushButton:hover {\n"
"border-radius:0px;\n"
"background-color: rgba(236, 236, 236, 0.1);\n"
"}\n"
"\n"
"#full_menu_widget QPushButton {\n"
"border:none;\n"
"padding:10px 30px;\n"
"border-radius:10px;\n"
"color: gray\n"
"}\n"
"\n"
"#full_menu_widget QPushButton:hover {\n"
"border-radius:0px;\n"
"background-color: rgba(236, 236, 236, 0.1);\n"
"}\n"
"\n"
"#full_menu_widget QPushButton:checked {\n"
"color:white;\n"
"}\n"
"\n"
"#search_input{\n"
"border:none;\n"
"padding: 15px 10px;\n"
"border-radius: 20px;\n"
"background-color: #2A2A2A;\n"
"color:white;\n"
"}\n"
"\n"
"#search_input:hover {\n"
"border: 1px solid gray\n"
"}\n"
"\n"
"#search_input:focus {\n"
"border: 2px solid white\n"
"}\n"
"\n"
"#login_btn{\n"
"background-color:white;\n"
"padding: 10px 20px;\n"
"border-radius: 20px;\n"
"color:#121212;\n"
"}\n"
"\n"
"#signup_btn{\n"
"padding: 10px;\n"
"color: #A2A2A2;\n"
"}\n"
"\n"
"#signup_btn:hover{\n"
"color:white\n"
"}\n"
"\n"
"#add_music_btn {\n"
"border: 1px solid white;\n"
"border_radius: 6px;\n"
"padding:10px 8px\n"
"}\n"
"\n"
"#add_music_btn:hover {\n"
"background-color:white;\n"
"color:black\n"
"}\n"
"\n"
"#create_playlist_btn {\n"
"background-color:white;\n"
"padding: 10px 20px;\n"
"border-radius: 20px;\n"
"color:#121212;\n"
"}\n"
"\n"
"#free_song_list, #premium_song_list, #search_list{\n"
"background-color: #1f1f1f;\n"
"selection-background-color: rgba(255,255,255,100);;\n"
"selection-color: rgb(66, 66, 66);\n"
"}\n"
"\n"
"#widget QPushButton{\n"
"border-radius: 6px;\n"
"margin: 0 10px\n"
"}\n"
"\n"
"#widget QPushButton:hover{\n"
"background-color: rgba(255,255,255,100)\n"
"}\n"
"\n"
"#widget QPushButton:checked{\n"
"background-color: rgba(255,255,255,100);\n"
"}\n"
"\n"
"#stacked_widget {\n"
"border-top:10px solid black;\n"
"}\n"
"\n"
".QListWidget{\n"
"padding:10px;\n"
"font: 14pt \"Arial Rounded MT Bold\";\n"
"}\n"
"\n"
".QListWidget:Item {\n"
"padding:5px;\n"
"margin:10px \n"
"}")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.icon_only_widget = QtWidgets.QWidget(self.centralwidget)
        self.icon_only_widget.setObjectName("icon_only_widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.icon_only_widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.logo_layout = QtWidgets.QHBoxLayout()
        self.logo_layout.setContentsMargins(-1, -1, -1, 0)
        self.logo_layout.setSpacing(0)
        self.logo_layout.setObjectName("logo_layout")
        self.label = QtWidgets.QLabel(self.icon_only_widget)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        self.label.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(5)
        self.label.setFont(font)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("resources3.qrc/icons8-music-50.png"))
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.logo_layout.addWidget(self.label, 0, QtCore.Qt.AlignVCenter)
        self.verticalLayout_3.addLayout(self.logo_layout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, 20, 0, 0)
        self.verticalLayout.setSpacing(30)
        self.verticalLayout.setObjectName("verticalLayout")
        self.home_btn = QtWidgets.QPushButton(self.icon_only_widget)
        self.home_btn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources3.qrc/House.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.home_btn.setIcon(icon)
        self.home_btn.setIconSize(QtCore.QSize(40, 40))
        self.home_btn.setCheckable(True)
        self.home_btn.setAutoExclusive(True)
        self.home_btn.setObjectName("home_btn")
        self.verticalLayout.addWidget(self.home_btn)
        self.search_btn = QtWidgets.QPushButton(self.icon_only_widget)
        self.search_btn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("resources3.qrc/icons8-search-50.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search_btn.setIcon(icon1)
        self.search_btn.setIconSize(QtCore.QSize(40, 40))
        self.search_btn.setCheckable(True)
        self.search_btn.setAutoExclusive(True)
        self.search_btn.setObjectName("search_btn")
        self.verticalLayout.addWidget(self.search_btn)
        self.library_btn = QtWidgets.QPushButton(self.icon_only_widget)
        self.library_btn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("resources3.qrc/Playlist.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.library_btn.setIcon(icon2)
        self.library_btn.setIconSize(QtCore.QSize(40, 40))
        self.library_btn.setCheckable(True)
        self.library_btn.setAutoExclusive(True)
        self.library_btn.setObjectName("library_btn")
        self.verticalLayout.addWidget(self.library_btn)
        self.pushButton_3 = QtWidgets.QPushButton(self.icon_only_widget)
        self.pushButton_3.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("resources3.qrc/download.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon3)
        self.pushButton_3.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 522, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.gridLayout.addWidget(self.icon_only_widget, 0, 0, 1, 1)
        self.full_menu_widget = QtWidgets.QWidget(self.centralwidget)
        self.full_menu_widget.setObjectName("full_menu_widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.full_menu_widget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(5)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.full_menu_widget)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(30)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(0, 20, 0, 0)
        self.verticalLayout_2.setSpacing(30)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.home_btn_2 = QtWidgets.QPushButton(self.full_menu_widget)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(15)
        self.home_btn_2.setFont(font)
        self.home_btn_2.setIcon(icon)
        self.home_btn_2.setIconSize(QtCore.QSize(40, 40))
        self.home_btn_2.setCheckable(True)
        self.home_btn_2.setAutoExclusive(True)
        self.home_btn_2.setObjectName("home_btn_2")
        self.verticalLayout_2.addWidget(self.home_btn_2, 0, QtCore.Qt.AlignLeft)
        self.search_btn_2 = QtWidgets.QPushButton(self.full_menu_widget)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(15)
        self.search_btn_2.setFont(font)
        self.search_btn_2.setIcon(icon1)
        self.search_btn_2.setIconSize(QtCore.QSize(40, 40))
        self.search_btn_2.setCheckable(True)
        self.search_btn_2.setAutoExclusive(True)
        self.search_btn_2.setObjectName("search_btn_2")
        self.verticalLayout_2.addWidget(self.search_btn_2, 0, QtCore.Qt.AlignLeft)
        self.library_btn_2 = QtWidgets.QPushButton(self.full_menu_widget)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(15)
        self.library_btn_2.setFont(font)
        self.library_btn_2.setIcon(icon2)
        self.library_btn_2.setIconSize(QtCore.QSize(40, 40))
        self.library_btn_2.setCheckable(True)
        self.library_btn_2.setAutoExclusive(True)
        self.library_btn_2.setObjectName("library_btn_2")
        self.verticalLayout_2.addWidget(self.library_btn_2)
        self.pushButton_4 = QtWidgets.QPushButton(self.full_menu_widget)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(15)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setIcon(icon3)
        self.pushButton_4.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_2.addWidget(self.pushButton_4, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 511, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.gridLayout.addWidget(self.full_menu_widget, 0, 1, 1, 1)
        self.main_widget = QtWidgets.QWidget(self.centralwidget)
        self.main_widget.setObjectName("main_widget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.main_widget)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.header_page = QtWidgets.QWidget(self.main_widget)
        self.header_page.setMinimumSize(QtCore.QSize(0, 40))
        self.header_page.setObjectName("header_page")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.header_page)
        self.horizontalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.menu_btn = QtWidgets.QPushButton(self.header_page)
        self.menu_btn.setMinimumSize(QtCore.QSize(44, 40))
        self.menu_btn.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("resources3.qrc/icons8-menu-50.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menu_btn.setIcon(icon4)
        self.menu_btn.setIconSize(QtCore.QSize(40, 40))
        self.menu_btn.setCheckable(True)
        self.menu_btn.setObjectName("menu_btn")
        self.horizontalLayout_3.addWidget(self.menu_btn, 0, QtCore.Qt.AlignLeft)
        spacerItem2 = QtWidgets.QSpacerItem(150, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.search_box = QtWidgets.QHBoxLayout()
        self.search_box.setContentsMargins(-1, -1, 0, -1)
        self.search_box.setSpacing(0)
        self.search_box.setObjectName("search_box")
        self.search_input = QtWidgets.QLineEdit(self.header_page)
        self.search_input.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(10)
        self.search_input.setFont(font)
        self.search_input.setObjectName("search_input")
        self.search_box.addWidget(self.search_input)
        self.horizontalLayout_3.addLayout(self.search_box)
        spacerItem3 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.signup_btn = QtWidgets.QPushButton(self.header_page)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(10)
        self.signup_btn.setFont(font)
        self.signup_btn.setObjectName("signup_btn")
        self.horizontalLayout_2.addWidget(self.signup_btn, 0, QtCore.Qt.AlignRight)
        self.login_btn = QtWidgets.QPushButton(self.header_page)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(10)
        self.login_btn.setFont(font)
        self.login_btn.setIconSize(QtCore.QSize(40, 40))
        self.login_btn.setObjectName("login_btn")
        self.horizontalLayout_2.addWidget(self.login_btn, 0, QtCore.Qt.AlignRight)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_5.addWidget(self.header_page)
        self.stacked_widget = QtWidgets.QStackedWidget(self.main_widget)
        self.stacked_widget.setObjectName("stacked_widget")
        self.home_widget = QtWidgets.QWidget()
        self.home_widget.setObjectName("home_widget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.home_widget)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.music_list = QtWidgets.QWidget(self.home_widget)
        self.music_list.setObjectName("music_list")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.music_list)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.free_song_list = QtWidgets.QListWidget(self.music_list)
        self.free_song_list.setObjectName("free_song_list")
        self.verticalLayout_7.addWidget(self.free_song_list)
        self.add_music_btn = QtWidgets.QPushButton(self.music_list)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(13)
        self.add_music_btn.setFont(font)
        self.add_music_btn.setObjectName("add_music_btn")
        self.verticalLayout_7.addWidget(self.add_music_btn, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_6.addWidget(self.music_list)
        self.music_btn = QtWidgets.QWidget(self.home_widget)
        self.music_btn.setObjectName("music_btn")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.music_btn)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.widget_2 = QtWidgets.QWidget(self.music_btn)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.horizontalLayout_7.addWidget(self.widget_2)
        self.widget = QtWidgets.QWidget(self.music_btn)
        self.widget.setObjectName("widget")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setSpacing(10)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(10)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.shuffle_btn = QtWidgets.QPushButton(self.widget)
        self.shuffle_btn.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("resources3.qrc/random.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.shuffle_btn.setIcon(icon5)
        self.shuffle_btn.setIconSize(QtCore.QSize(40, 40))
        self.shuffle_btn.setCheckable(True)
        self.shuffle_btn.setObjectName("shuffle_btn")
        self.horizontalLayout_6.addWidget(self.shuffle_btn)
        self.previous_btn = QtWidgets.QPushButton(self.widget)
        self.previous_btn.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("resources3.qrc/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.previous_btn.setIcon(icon6)
        self.previous_btn.setIconSize(QtCore.QSize(40, 40))
        self.previous_btn.setObjectName("previous_btn")
        self.horizontalLayout_6.addWidget(self.previous_btn)
        self.pause_btn = QtWidgets.QPushButton(self.widget)
        self.pause_btn.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("resources3.qrc/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pause_btn.setIcon(icon7)
        self.pause_btn.setIconSize(QtCore.QSize(40, 40))
        self.pause_btn.setCheckable(False)
        self.pause_btn.setObjectName("pause_btn")
        self.horizontalLayout_6.addWidget(self.pause_btn)
        self.play_btn = QtWidgets.QPushButton(self.widget)
        self.play_btn.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("resources3.qrc/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.play_btn.setIcon(icon8)
        self.play_btn.setIconSize(QtCore.QSize(40, 40))
        self.play_btn.setCheckable(False)
        self.play_btn.setObjectName("play_btn")
        self.horizontalLayout_6.addWidget(self.play_btn)
        self.stop_btn = QtWidgets.QPushButton(self.widget)
        self.stop_btn.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("resources3.qrc/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stop_btn.setIcon(icon9)
        self.stop_btn.setIconSize(QtCore.QSize(40, 40))
        self.stop_btn.setCheckable(True)
        self.stop_btn.setObjectName("stop_btn")
        self.horizontalLayout_6.addWidget(self.stop_btn)
        self.next_btn = QtWidgets.QPushButton(self.widget)
        self.next_btn.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("resources3.qrc/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.next_btn.setIcon(icon10)
        self.next_btn.setIconSize(QtCore.QSize(40, 40))
        self.next_btn.setObjectName("next_btn")
        self.horizontalLayout_6.addWidget(self.next_btn)
        self.loop_btn = QtWidgets.QPushButton(self.widget)
        self.loop_btn.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("resources3.qrc/shuffle.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.loop_btn.setIcon(icon11)
        self.loop_btn.setIconSize(QtCore.QSize(40, 40))
        self.loop_btn.setCheckable(True)
        self.loop_btn.setObjectName("loop_btn")
        self.horizontalLayout_6.addWidget(self.loop_btn)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setText("")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("resources3.qrc/plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon12)
        self.pushButton_2.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_6.addWidget(self.pushButton_2)
        self.pushButton_5 = QtWidgets.QPushButton(self.widget)
        self.pushButton_5.setText("")
        self.pushButton_5.setIcon(icon3)
        self.pushButton_5.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_6.addWidget(self.pushButton_5)
        self.verticalLayout_9.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(10, -1, 10, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.start_time_label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(10)
        self.start_time_label.setFont(font)
        self.start_time_label.setObjectName("start_time_label")
        self.horizontalLayout_5.addWidget(self.start_time_label)
        self.music_slider = QtWidgets.QSlider(self.widget)
        self.music_slider.setOrientation(QtCore.Qt.Horizontal)
        self.music_slider.setObjectName("music_slider")
        self.horizontalLayout_5.addWidget(self.music_slider)
        self.end_time_label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(10)
        self.end_time_label.setFont(font)
        self.end_time_label.setObjectName("end_time_label")
        self.horizontalLayout_5.addWidget(self.end_time_label)
        self.verticalLayout_9.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7.addWidget(self.widget)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton = QtWidgets.QPushButton(self.music_btn)
        self.pushButton.setText("")
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("resources3.qrc/volume_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon13)
        self.pushButton.setIconSize(QtCore.QSize(30, 30))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_4.addWidget(self.pushButton)
        self.volume_slider = QtWidgets.QSlider(self.music_btn)
        self.volume_slider.setMinimumSize(QtCore.QSize(0, 0))
        self.volume_slider.setOrientation(QtCore.Qt.Horizontal)
        self.volume_slider.setObjectName("volume_slider")
        self.horizontalLayout_4.addWidget(self.volume_slider, 0, QtCore.Qt.AlignRight)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_4)
        self.verticalLayout_6.addWidget(self.music_btn)
        self.stacked_widget.addWidget(self.home_widget)
        self.playlist_widget = QtWidgets.QWidget()
        self.playlist_widget.setObjectName("playlist_widget")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.playlist_widget)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.create_playlist_btn = QtWidgets.QPushButton(self.playlist_widget)
        self.create_playlist_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.create_playlist_btn.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(15)
        self.create_playlist_btn.setFont(font)
        self.create_playlist_btn.setObjectName("create_playlist_btn")
        self.verticalLayout_8.addWidget(self.create_playlist_btn, 0, QtCore.Qt.AlignHCenter)
        self.listWidget = QtWidgets.QListWidget(self.playlist_widget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_8.addWidget(self.listWidget)
        self.stacked_widget.addWidget(self.playlist_widget)
        self.search_widget = QtWidgets.QWidget()
        self.search_widget.setObjectName("search_widget")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.search_widget)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.search_list = QtWidgets.QListWidget(self.search_widget)
        self.search_list.setObjectName("search_list")
        self.verticalLayout_10.addWidget(self.search_list)
        self.stacked_widget.addWidget(self.search_widget)
        self.favorite_widget = QtWidgets.QWidget()
        self.favorite_widget.setObjectName("favorite_widget")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.favorite_widget)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_2 = QtWidgets.QLabel(self.favorite_widget)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(25)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_11.addWidget(self.label_2, 0, QtCore.Qt.AlignTop)
        self.stacked_widget.addWidget(self.favorite_widget)
        self.verticalLayout_5.addWidget(self.stacked_widget)
        self.gridLayout.addWidget(self.main_widget, 0, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stacked_widget.setCurrentIndex(0)
        self.menu_btn.toggled['bool'].connect(self.icon_only_widget.setVisible) # type: ignore
        self.menu_btn.toggled['bool'].connect(self.full_menu_widget.setHidden) # type: ignore
        self.home_btn.toggled['bool'].connect(self.home_btn_2.setChecked) # type: ignore
        self.home_btn_2.toggled['bool'].connect(self.home_btn.setChecked) # type: ignore
        self.library_btn.toggled['bool'].connect(self.library_btn_2.setChecked) # type: ignore
        self.library_btn_2.toggled['bool'].connect(self.library_btn.setChecked) # type: ignore
        self.search_btn.toggled['bool'].connect(self.search_btn_2.setChecked) # type: ignore
        self.search_btn_2.toggled['bool'].connect(self.search_btn.setChecked) # type: ignore
        self.pushButton_3.toggled['bool'].connect(self.pushButton_4.setChecked) # type: ignore
        self.pushButton_4.toggled['bool'].connect(self.pushButton_3.setChecked) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_3.setText(_translate("MainWindow", "MUSIC"))
        self.home_btn_2.setText(_translate("MainWindow", "Home"))
        self.search_btn_2.setText(_translate("MainWindow", "Search"))
        self.library_btn_2.setText(_translate("MainWindow", "Your playlist"))
        self.pushButton_4.setText(_translate("MainWindow", "Download"))
        self.search_input.setPlaceholderText(_translate("MainWindow", "What do you want to listen to?"))
        self.signup_btn.setText(_translate("MainWindow", "Sign up"))
        self.login_btn.setText(_translate("MainWindow", "Log in"))
        self.add_music_btn.setText(_translate("MainWindow", "Add music"))
        self.start_time_label.setText(_translate("MainWindow", "00:00"))
        self.end_time_label.setText(_translate("MainWindow", "00:00"))
        self.create_playlist_btn.setText(_translate("MainWindow", "Create your playlist"))
        self.label_2.setText(_translate("MainWindow", "Download"))
        
        self.login_btn.clicked.connect(self.goToLogin)
        self.login_btn.clicked.connect(MainWindow.close)
        self.signup_btn.clicked.connect(self.goToSignup)
        self.signup_btn.clicked.connect(MainWindow.close)
        
        self.icon_only_widget.hide()
        self.home_btn_2.setChecked(True)

        self.home_btn.clicked.connect(self.showHome)
        self.home_btn_2.clicked.connect(self.showHome)
        
        self.library_btn.clicked.connect(self.playlistDisable)
        self.library_btn_2.clicked.connect(self.playlistDisable)
        
        self.pushButton_3.clicked.connect(self.downloadDisable)
        self.pushButton_4.clicked.connect(self.downloadDisable)
        
        self.search_btn.clicked.connect(self.showSearch)
        self.search_btn_2.clicked.connect(self.showSearch)
        self.search_input.textChanged.connect(self.showSearch)
        
        self.add_music_btn.clicked.connect(self.add_songs)
        self.add_music_btn.hide()
        
        global stopped
        global looped
        global is_shuffled

        stopped = False
        looped = False
        is_shuffled = False
        
        self.songs_name_list = []
        self.current_songs = []
        
        self.current_volume = 50
        self.player = QMediaPlayer()
        self.player.setVolume(self.current_volume)
        
        self.timer = QTimer(MainWindow)
        self.timer.start(1000)
        self.timer.timeout.connect(self.move_slider)
        
        self.volume_slider.sliderMoved[int].connect(lambda: self.volume_changed())
        self.music_slider.sliderMoved[int].connect(lambda: self.player.setPosition(self.music_slider.value()))
        
        self.music_btn.hide()
        self.free_song_list.currentItemChanged.connect(self.show_btn)
        
        self.play_btn.clicked.connect(self.play_song)
        self.pause_btn.clicked.connect(self.pause_and_unpause)
        self.stop_btn.clicked.connect(self.stop_song)
        self.next_btn.clicked.connect(self.next_song)
        self.previous_btn.clicked.connect(self.previous_song)
        self.loop_btn.clicked.connect(self.loop_one_song)
        self.shuffle_btn.clicked.connect(self.shuffled_playlist)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

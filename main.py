import sys
import re
import typing
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QMainWindow, QWidget, QMessageBox
from PyQt5.uic import loadUi
import MySQLdb as mdb

# log in screen
class loginScreen(QMainWindow):
    def __init__(self):
        super(loginScreen,self).__init__()
        uic.loadUi("login.ui",self)
        self.loginBtn.clicked.connect(self.login)
        self.goToRegister.clicked.connect(self.register)
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
        self.goToLogin.clicked.connect(self.login)
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
        uic.loadUi("main_page.ui",self)
        # self.goToLoginScreen.clicked.connect(self.goToLogin)
    
    # def goToLogin(self):
    #     widget.setCurrentWidget(login)

# main page for logged in user
class loggedMainPage(QMainWindow):
    def __init__(self):
        super(loggedMainPage,self).__init__() 
        uic.loadUi("main_page_logged.ui",self)
        self.accountBtn.clicked.connect(self.goToProfile)

    def goToProfile(self):
        widget.setCurrentWidget(profile)

# profile
class profileScreen(QMainWindow):
    def __init__(self):
        super(profileScreen, self).__init__()
        uic.loadUi("profile.ui",self)
        # self.pushButton_4.clicked.connect(self.goToMain)
        self.logOutBtn.clicked.connect(self.goToLogin)
    # def goToMain(self):
    #     widget.setCurrentWidget(mainPageLogged)
    def goToLogin(self):
        widget.setCurrentWidget(login)

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
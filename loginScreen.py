from PyQt5 import QtCore, QtGui, QtWidgets
from homeScreen1 import Ui_HomeWindow
from getPremium import Ui_PremRegWindow
from profileScreen import Ui_ProfileWindow
from PyQt5.QtWidgets import *
import MySQLdb as mdb

class Ui_LoginWindow(object):
    def closeWindows(self):
        current_window = QtWidgets.QApplication.activeWindow()
        if current_window is not None:
            current_window.close()
            
    def goToSignup(self):
        try:
            from signupScreen import Ui_SignupWindow
            self.signup_window = QtWidgets.QMainWindow()
            self.ui = Ui_SignupWindow()
            self.ui.setupUi(self.signup_window)
            self.signup_window.show()
        except ImportError:
            pass

    def goToHomePage(self):
        try:
            from homeScreen1 import Ui_HomeWindow
            self.home_window = QtWidgets.QMainWindow()
            self.ui = Ui_HomeWindow()
            self.ui.setupUi(self.home_window)
            self.ui.load_song()
            self.home_window.show()
            self.closeWindows()
        except ImportError:
            pass

    def login(self):
        username = self.logon.text()
        password = self.password.text()
        
        db = mdb.connect('localhost','root','','music_app_db')
        query = db.cursor()
        premium = db.cursor()
        id = db.cursor()
        query.execute("SELECT * FROM `user_management` WHERE username = '"+username+"' and password = '"+password+"'")
        # premium.execute("SELECT `premium` FROM `user_management` WHERE username = '"+username+"'")
        # id.execute("SELECT `user_id` FROM `user_management` WHERE username = '"+username+"'")
        
        loginSuccess = query.fetchone()
        if loginSuccess:
            premium.execute("SELECT `premium` FROM user_management WHERE username = %s", (username,))
            id.execute("SELECT `user_id` FROM user_management WHERE username = %s", (username,))
            get_premium = premium.fetchone()[0]
            get_id = id.fetchone()[0]
            QMessageBox.information(None, "Login success!", "Welcome!")
            
            try:
                # get_username = username
                # sendNameToProfile= Ui_ProfileWindows
                # sendNameToProfile.receive_username(get_username)
                
                sendIdToPremReg = Ui_PremRegWindow
                sendIdToPremReg.receive_id(get_id)
                
                sendPremToHome = Ui_HomeWindow()
                sendPremToHome.receive_prem(get_premium)
            except TypeError:
                pass
            
            try:
                MainWindow.close()
            except NameError:
                pass
            self.goToHomePage()
        else:
            if len(username) == 0:
                QMessageBox.information(None, "Login fail!", "Username is required")
            elif len(password) == 0:
                QMessageBox.information(None, "Login fail!", "Password is required")
            elif len(password) > 16 or len(password) < 8:
                QMessageBox.information(None, "Login fail!", "Password must be more than 8 characters less than 16 characters!")
            else:
                QMessageBox.information(None, "Login fail!", "Username or password is incorrect!")

    def passId(self, index):
        i = index
        print("ID: ", i)
        return i

    def forgotPassword(self):
        QMessageBox.information(self,"Lỗi", "In development")
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1440, 920)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("*{\n"
"color:white\n"
"}\n"
"\n"
"#background {\n"
"background-color:black\n"
"}\n"
"\n"
"#login_form {\n"
"background-color:#121212;\n"
"border-radius: 15px\n"
"}\n"
"\n"
"#login_form QLineEdit {\n"
"background-color:#121212;\n"
"border-radius: 4px;\n"
"border: 1px solid gray;\n"
"padding: 0px 10px;\n"
"height: 55px;\n"
"color:white;\n"
"}\n"
"\n"
"#login_form QLineEdit:hover {\n"
"border: 1.5px solid white\n"
"}\n"
"\n"
"#login_form QLineEdit:focus {\n"
"border: 1.5px solid white\n"
"}\n"
"\n"
"#forgotPsw {\n"
"border:none;\n"
"background-color:#121212;\n"
"color:white;\n"
"}\n"
"\n"
"#loginBtn {\n"
"background-color:#1BD760;\n"
"border-radius:5px;\n"
"color:#121212;\n"
"padding:5px;\n"
"height:40px\n"
"}\n"
"\n"
"#signupBtn {\n"
"background-color:#121212;\n"
"border:none;\n"
"color:white\n"
"}")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.background = QtWidgets.QFrame(self.centralwidget)
        self.background.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.background.setFrameShadow(QtWidgets.QFrame.Raised)
        self.background.setObjectName("background")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.background)
        self.verticalLayout_2.setContentsMargins(400, 150, 400, 200)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.login_form = QtWidgets.QWidget(self.background)
        self.login_form.setObjectName("login_form")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.login_form)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.login_title_field = QtWidgets.QWidget(self.login_form)
        self.login_title_field.setObjectName("login_title_field")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.login_title_field)
        self.verticalLayout_4.setContentsMargins(100, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(self.login_title_field)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(30)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label, 0, QtCore.Qt.AlignVCenter)
        self.verticalLayout_3.addWidget(self.login_title_field)
        self.in4_blank_field = QtWidgets.QWidget(self.login_form)
        self.in4_blank_field.setObjectName("in4_blank_field")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.in4_blank_field)
        self.verticalLayout_5.setContentsMargins(100, 0, 100, 0)
        self.verticalLayout_5.setSpacing(15)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.logon = QtWidgets.QLineEdit(self.in4_blank_field)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(14)
        self.logon.setFont(font)
        self.logon.setObjectName("logon")
        self.verticalLayout_5.addWidget(self.logon)
        self.password = QtWidgets.QLineEdit(self.in4_blank_field)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(14)
        self.password.setFont(font)
        self.password.setObjectName("password")
        self.verticalLayout_5.addWidget(self.password)
        self.forgotPsw = QtWidgets.QPushButton(self.in4_blank_field)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(13)
        font.setUnderline(True)
        self.forgotPsw.setFont(font)
        self.forgotPsw.setObjectName("forgotPsw")
        self.verticalLayout_5.addWidget(self.forgotPsw, 0, QtCore.Qt.AlignRight)
        self.verticalLayout_3.addWidget(self.in4_blank_field)
        self.login_button_field = QtWidgets.QWidget(self.login_form)
        font = QtGui.QFont()
        font.setFamily("Papyrus")
        self.login_button_field.setFont(font)
        self.login_button_field.setObjectName("login_button_field")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.login_button_field)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.widget = QtWidgets.QWidget(self.login_button_field)
        self.widget.setObjectName("widget")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_7.setContentsMargins(190, 0, 190, 0)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.loginBtn = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(15)
        self.loginBtn.setFont(font)
        self.loginBtn.setObjectName("loginBtn")
        self.verticalLayout_7.addWidget(self.loginBtn)
        self.verticalLayout_6.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(self.login_button_field)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_8.setContentsMargins(100, -1, -1, -1)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.widget_2)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2, 0, QtCore.Qt.AlignRight)
        self.signupBtn = QtWidgets.QPushButton(self.widget_2)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(13)
        font.setUnderline(True)
        self.signupBtn.setFont(font)
        self.signupBtn.setObjectName("signupBtn")
        self.horizontalLayout.addWidget(self.signupBtn, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout_8.addLayout(self.horizontalLayout)
        self.verticalLayout_6.addWidget(self.widget_2)
        self.verticalLayout_3.addWidget(self.login_button_field)
        self.verticalLayout_2.addWidget(self.login_form)
        self.verticalLayout.addWidget(self.background)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Login"))
        self.logon.setPlaceholderText(_translate("MainWindow", "Username"))
        self.password.setPlaceholderText(_translate("MainWindow", "Password"))
        self.forgotPsw.setText(_translate("MainWindow", "Forgot password?"))
        self.loginBtn.setText(_translate("MainWindow", "Log in"))
        self.label_2.setText(_translate("MainWindow", "Not a member?"))
        self.signupBtn.setText(_translate("MainWindow", "Sign up"))
        
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.loginBtn.clicked.connect(self.login)
        self.signupBtn.clicked.connect(self.goToSignup)
        self.signupBtn.clicked.connect(MainWindow.close)
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_LoginWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

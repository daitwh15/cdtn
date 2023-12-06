from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import MySQLdb as mdb

class Ui_PremRegWindow(object):
    def closeWindows(self):
        current_window = QtWidgets.QApplication.activeWindow()
        if current_window is not None:
            current_window.close()
            
    def goToLogin(self):
        try:
            from loginScreen import Ui_LoginWindow
            self.login_window = QtWidgets.QMainWindow()
            self.ui = Ui_LoginWindow()
            self.ui.setupUi(self.login_window)
            self.login_window.show()
            self.closeWindows()
        except ImportError:
            pass
        
    def receive_id(get_id):
        Ui_PremRegWindow.id = get_id
        print(f"ID: {Ui_PremRegWindow.id}")
        
    def quickPremReg(self):
        user_fullname = self.full_name.text()
        payment_method = None
        if self.credit_card.isChecked():
            payment_method = "Credit card"
        elif self.momo_wallet.isChecked():
            payment_method = "Momo wallet"
        
        db = mdb.connect('localhost','root','','music_app_db')
        query = db.cursor()
        if len(user_fullname) == 0:
            QMessageBox.information(None, "Error", "Please enter your full name")
        elif not self.credit_card.isChecked() and not self.momo_wallet.isChecked():
            QMessageBox.information(None, "Error", "Please choose a payment method")
        else:
            QMessageBox.information(None, "Thank you!", "You have successfully registered for the premium package")
            query.execute("INSERT INTO `premium_payment_management` (`user_id`, `username`, `price`, `duration`, `payment_method`, `type_plan`) VALUES ('"+str(Ui_PremRegWindow.id)+"', '"+user_fullname+"','"+str(59000)+"', '"+str(3)+"', '"+payment_method+"', '"+str(2)+"')")
            query.execute("UPDATE `user_management` SET premium = '"+str(1)+"' WHERE user_id = '"+str(Ui_PremRegWindow.id)+"'")
            db.commit()
            self.goToLogin()
        

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(20, -1, -1, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(20, -1, 400, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.full_name = QtWidgets.QLineEdit(self.widget)
        self.full_name.setObjectName("full_name")
        self.horizontalLayout_2.addWidget(self.full_name)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.credit_card = QtWidgets.QRadioButton(self.widget)
        self.credit_card.setObjectName("credit_card")
        self.horizontalLayout_3.addWidget(self.credit_card, 0, QtCore.Qt.AlignHCenter)
        self.momo_wallet = QtWidgets.QRadioButton(self.widget)
        self.momo_wallet.setObjectName("momo_wallet")
        self.horizontalLayout_3.addWidget(self.momo_wallet, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.confirm = QtWidgets.QPushButton(self.widget)
        self.confirm.setObjectName("confirm")
        self.horizontalLayout.addWidget(self.confirm, 0, QtCore.Qt.AlignHCenter)
        self.view_plans = QtWidgets.QPushButton(self.widget)
        self.view_plans.setObjectName("view_plans")
        self.horizontalLayout.addWidget(self.view_plans, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout.addWidget(self.widget_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "$$$ for 3 months of Premium"))
        self.label_2.setText(_translate("MainWindow", "Enjoy an ad-free music listening experience"))
        self.label_3.setText(_translate("MainWindow", "Full name:"))
        self.credit_card.setText(_translate("MainWindow", "Credit card"))
        self.momo_wallet.setText(_translate("MainWindow", "Momo wallet"))
        self.confirm.setText(_translate("MainWindow", "Get Started"))
        self.view_plans.setText(_translate("MainWindow", "View plans"))
        
        self.confirm.clicked.connect(self.quickPremReg)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_PremRegWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

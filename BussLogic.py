from SignInWindow import Ui_Dialog as SignInWindow_Ui
from MainWindow import Ui_MainWindow as MainWindow_Ui
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import sys
from mailserver import *
import traceback

class SignInWindowUi(SignInWindow_Ui, QtWidgets.QDialog):
    def __init__(self):
        super(SignInWindowUi, self).__init__()
        self.setupUi(self)

    def fetch_info(self):
        if self.comboBoxServerAddress.currentText() == "QQ Mail":
            mail_server_address = "mail.qq.com"
        elif self.comboBoxServerAddress.currentText() == "WHU E-mail":
            mail_server_address = "email.whu.edu.cn"
        elif self.comboBoxServerAddress.currentText() == "Gmail":
            mail_server_address = "mail.google.com"
        elif self.comboBoxServerAddress.currentText() == "163 Mail":
            mail_server_address = "mail.163.com"
        username = self.lineEditUsername.text()
        password = self.lineEditPassword.text()
        return mail_server_address, username, password


class MainWindowUi(MainWindow_Ui, QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindowUi, self).__init__()
        self.setupUi(self)
        self.list_widget = self.listWidget
        self.stacked_widget = self.stackedWidget
        self.change_stacked_widget()

    def change_stacked_widget(self):
        self.list_widget.currentRowChanged.connect(self.display_subpage)

    # def change_stacked_widget(self):
    #     self.list_widget.currentRowChanged.connect(self.display_subpage)

    def display_subpage(self, i):
        self.stacked_widget.setCurrentIndex(i)

    def set_text_edit(self, mail_server, username, password):
        text = mail_server + username + password
        self.textEdit.setText(text)

class MailServer(Smtp, Pop3):
    def __init__(self):
        self.mail_server = " "
        self.username = " "
        self.password = " "
        self.smtp = None
        self.pop3 = None

    def info_init(self, mail_server, username, password):
        self.mail_server = mail_server
        self.username = username
        self.password = password
        try:
            self.smtp = Smtp(mailserver=mail_server, username=username, password=password)
            self.pop3 = Pop3(mailserver=mail_server, username=username, password=password)
        except Exception as e:
            print(e)
        else:
            print(mail_server, username, password)

# class BackendThread(QThread):
#     click_push_btn_sign_in = pyqtSignal(object)
#
#     def click_push_btn_sign_in_event(self, event):
#         if event.buttons == Qt.LeftButton:
#             self.click_push_btn_sign_in.emit()

    # def run(self):
    #     if

class BussLogic:
    def __init__(self):
        self.sign_in_window = SignInWindowUi()
        self.main_window = MainWindowUi()
        self.mail_server = MailServer()
        self.sign_in_window.pushButtonSignin.clicked.connect(self.click_sign_in)

    def click_sign_in(self):
        print(1)
        self.mail_server = MailServer()
        print(3)
        mail_server_address, username, password = self.sign_in_window.fetch_info()
        print(4)
        self.mail_server.info_init(mail_server=mail_server_address, username=username, password=password)
        print(2)
        self.sign_in_window.close()

    def trans_info(self):
        mail_server_address, username, password = self.sign_in_window.fetch_info()
        self.mail_server.info_init(mail_server_address, username, password)

    # def control_flow(self):
        # self.sign_in_window.info_signal.connect(self.mail_server.info_init)
        # self.sign_in_window.pushButtonSignin.clicked.connect(lambda: {self.trans_info(), self.sign_in_window.close()})
        # self.sign_in_window.pushButtonSignin.clicked.connect(self.click_push_btn_sign_in)
        # self.main_window.change_stacked_widget()

        # self.sign_in_window.info_signal.connect(self.main_window.set_text_edit)
        # self.sign_in_window.show()
        # return self.select_mail_server()
        # self.sign_window.setupUi()
        # self.sign_window.pushButtonSignin.clicked.connect(self.show_main_window)



    # def show_main_window(self):
    #     self.sign_in_window.close()
    #     self.main_window.show()

    # def slot_sign_in(self):
    #     self.sign_window.close()
    #     self.main_window.show()

    # def on_click_sign_in(self):
    #     # self.sign_window.show()
    #     # self.sign_window.pushButtonSignin.clicked.connect(lambda: {self.sign_window.close(), self.main_window.show()})
    #     self.sign_window.pushButtonSignin.clicked.connect(self.slot_sign_in)

    # def select_mail_server(self):
    #     if self.sign_in_window.comboBoxServerAddress.currentText() == "QQ Mail":
    #         self.mail_server = "mail.qq.com"
    #     elif self.sign_in_window.comboBoxServerAddress.currentText() == "WHU E-mail":
    #         self.mail_server = "email.whu.edu.cn"
    #     elif self.sign_in_window.comboBoxServerAddress.currentText() == "Gmail":
    #         self.mail_server = "mail.google.com"
    #     elif self.sign_in_window.comboBoxServerAddress.currentText() == "163 Mail":
    #         self.mail_server = "mail.163.com"
    #     self.username = self.sign_in_window.lineEditUsername.text()
    #     self.password = self.sign_in_window.lineEditPassword.text()
    #     print(self.mail_server, self.username, self.password)

# class ClickListWidget:
#     def __init__(self):
#         self.main_window = MainWindowUi()
#         self.list_widget = self.main_window.listWidget
#         self.stacked_widget = self.main_window.stackedWidget
#
#     def change_stacked_widget(self):
#         self.list_widget.currentRowChanged.connect(self.display)
#
#     def display(self, i):
#         self.stacked_widget.setCurrentIndex(i)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    buss = BussLogic()
    buss.sign_in_window.exec()
    buss.main_window.show()
    # main = MainWindowUi()
    # main.show()
    # click_list_widget = ClickListWidget()
    # click_list_widget.change_stacked_widget()
    # mail_server, username, password = sign_in_buss.select_mail_server()
    # sign_in_buss.on_click_sign_in()
    sys.exit(app.exec_())

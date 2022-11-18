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
        self.mail_server_address = "mail.qq.com" # Default
        self.comboBoxServerAddress.activated.connect(self.select_server_address)

    def fetch_info(self):
        username = self.lineEditUsername.text()
        password = self.lineEditPassword.text()
        return self.mail_server_address, username, password

    def select_server_address(self):
        if self.comboBoxServerAddress.currentText() == "QQ Mail":
            self.mail_server_address = "smtp.qq.com"
        elif self.comboBoxServerAddress.currentText() == "WHU E-Mail":
            self.mail_server_address = "smtp.whu.edu.cn"
        elif self.comboBoxServerAddress.currentText() == "Gmail":
            self.mail_server_address = "smtp.google.com"
        elif self.comboBoxServerAddress.currentText() == "163 Mail":
            self.mail_server_address = "smtp.163.com"

class MainWindowUi(MainWindow_Ui, QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindowUi, self).__init__()
        self.setupUi(self)
        self.list_widget = self.listWidget
        self.stacked_widget = self.stackedWidget
        self.change_stacked_widget()

    def change_stacked_widget(self):
        self.list_widget.currentRowChanged.connect(self.display_subpage)

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

class BussLogic:
    def __init__(self):
        self.sign_in_window = SignInWindowUi()
        self.main_window = MainWindowUi()
        self.mail_server = MailServer()
        self.sender_proc = None
        self.sign_in_window.pushButtonSignin.clicked.connect(self.click_sign_in)
        self.main_window.pushButtonSend.clicked.connect(self.click_send)

    def click_sign_in(self):
        self.mail_server = MailServer()
        mail_server_address, username, password = self.sign_in_window.fetch_info()
        self.mail_server.info_init(mail_server=mail_server_address, username=username, password=password)
        self.sign_in_window.close()

    def click_send(self):
        self.sender_proc = Sender_proc(sender=self.mail_server.username,
                                       receiver=self.main_window.lineEditTo.text(),
                                       subject=self.main_window.lineEditSubject.text(),
                                       message=self.main_window.textEdit.toPlainText())
        mail = self.sender_proc.gene_mail_class()
        path = self.sender_proc.store(mail)
        self.mail_server.smtp.mail = mail
        self.mail_server.smtp.path = path
        self.mail_server.smtp.sendmail()
        self.main_window.display_subpage(3)

    def trans_info(self):
        mail_server_address, username, password = self.sign_in_window.fetch_info()
        self.mail_server.info_init(mail_server_address, username, password)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    buss = BussLogic()
    buss.sign_in_window.exec()
    buss.main_window.show()
    sys.exit(app.exec_())

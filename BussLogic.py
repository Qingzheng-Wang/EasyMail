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
        BussLogic.win_stage=0
        self.setupUi(self)
        self.mail_server_address = "smtp.qq.com" # Default
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
        self.main_window.pushButtonSave.clicked.connect(self.click_save)
        self.main_window.Reflesh_Button.clicked.connect(self.reflesh_recv)
        self.main_window.listWidget.itemClicked.connect(self.show_recv)
        self.main_window.listWidget_2.itemClicked.connect(self.show_mail)
        self.main_window.listWidget.itemClicked.connect(self.show_draft)
        self.main_window.listWidget_3.itemClicked.connect(self.open_draft)
        self.main_window.pushButtonBackToInbox.clicked.connect(self.compose_to_inbox)
        self.main_window.pushButtonComposeAnotherEmail.clicked.connect(self.back_to_comp)
        self.main_window.Delete_Button.clicked.connect(self.delete_mail)
        self.main_window.Resend_button.clicked.connect(self.resend_butt)

    def resend_butt(self):
        print('111')
        uid=self.uid
        result=sql.SQL.search_sql_by_uid_with_sender(self.mail_server.username,uid,'Draft')
        mail=Mail()
        mail.sender=result[0][0]
        mail.receiver=result[0][1]
        mail.topic=result[0][2]
        mail.uid=result[0][3]
        self.mail_server.smtp.mail = mail
        self.mail_server.smtp.path = "C:\\MailServer\\Draft"
        no=self.mail_server.smtp.sendmail()
        if(no==errno):
            self.main_window.close()
            self.sign_in_window.exec()
        sql.SQL.delete_sql(uid,'Draft')
        os.remove("C:\\MailServer\\Draft\\"+uid+'.txt')
        self.main_window.display_subpage(3)

    def delete_mail(self):
        uid=self.uid
        result=sql.SQL.search_sql_by_uid(self.mail_server.username,uid,'Mail')
        index=result[0][4]
        self.mail_server.pop3.recvmail('DELE',index)
        self.reflesh_recv()
        
    def show_draft(self,item):
        if(item.text()=='Drafts'):
            self.main_window.listWidget_3.clear()
            recvaddr=self.mail_server.username
            dbtuple=sql.SQL.show_tables()
            dblist=''
            for i in dbtuple:
                dblist+=i[0]
            if(dblist.find('draft')==-1):
                sql.SQL.create_sql('Draft')
            recvtuple=sql.SQL.search_sql_by_sender(recvaddr,'Draft')
            if(recvtuple==None):
                return
            for t in recvtuple:
                tmp=List_item(t[2],t[0],t[3],t[4])
                self.main_window.listWidget_3.addItem(tmp)
                self.main_window.listWidget_3.setItemWidget(tmp,tmp.widgit)

    def open_draft(self,item):
        uid=item.uid
        self.uid=uid
        f=open('C:\\MailServer\\Draft\\'+uid+'.txt')
        msg=f.read()
        self.main_window.textBrowser_2.setText(msg)

    def compose_to_inbox(self):
        self.main_window.stacked_widget.setCurrentIndex(1)

    def back_to_comp(self):
        self.main_window.lineEditTo.clear()
        self.main_window.lineEditSubject.clear()
        self.main_window.textEdit.clear()
        self.main_window.stacked_widget.setCurrentIndex(0)

    def click_sign_in(self):
        self.mail_server = MailServer()
        mail_server_address, username, password = self.sign_in_window.fetch_info()
        if(username=="" or password==""):
            return
        self.mail_server.info_init(mail_server=mail_server_address, username=username, password=password)
        BussLogic.win_stage=1
        self.sign_in_window.close()

    def click_send(self):
        self.sender_proc = Sender_proc(sender=self.mail_server.username,
                                       receiver=self.main_window.lineEditTo.text(),
                                       subject=self.main_window.lineEditSubject.text(),
                                       message=self.main_window.textEdit.toPlainText())
        mail = self.sender_proc.gene_mailclass()
        self.sender_proc.store()
        self.mail_server.smtp.mail = mail
        self.mail_server.smtp.path = "C:\\MailServer\\Draft"
        no=self.mail_server.smtp.sendmail()
        if(no==errno):
            self.main_window.close()
            self.sign_in_window.exec()
        self.main_window.display_subpage(3)

    def click_save(self):
        self.sender_proc = Sender_proc(sender=self.mail_server.username,
                                       receiver=self.main_window.lineEditTo.text(),
                                       subject=self.main_window.lineEditSubject.text(),
                                       message=self.main_window.textEdit.toPlainText())
        mail=self.sender_proc.gene_mailclass()
        self.sender_proc.store()
        sql.SQL.add_sql(mail.sender,mail.receiver,mail.topic,mail.uid,0,'Draft')

    def trans_info(self):
        mail_server_address, username, password = self.sign_in_window.fetch_info()
        self.mail_server.info_init(mail_server_address, username, password)

    def reflesh_recv(self):
        self.main_window.listWidget_2.clear()
        self.mail_server.pop3.recvmail('LIST',0)
        recvaddr=self.mail_server.username
        recvtuple=sql.SQL.search_sql(recvaddr,'Mail')
        if(recvtuple==None):
            return
        for t in recvtuple:
            tmp=List_item(t[2],t[0],t[3],t[4])
            self.main_window.listWidget_2.addItem(tmp)
            self.main_window.listWidget_2.setItemWidget(tmp,tmp.widgit)

    def show_recv(self,item):
        if(item.text()=='Inbox'):
            self.main_window.listWidget_2.clear()
            recvaddr=self.mail_server.username
            dbtuple=sql.SQL.show_tables()
            dblist=''
            for i in dbtuple:
                dblist+=i[0]
            if(dblist.find('mail')==-1):
                sql.SQL.create_sql('Mail')
            recvtuple=sql.SQL.search_sql(recvaddr,'Mail')
            if(recvtuple==None):
                return
            for t in recvtuple:
                tmp=List_item(t[2],t[0],t[3],t[4])
                self.main_window.listWidget_2.addItem(tmp)
                self.main_window.listWidget_2.setItemWidget(tmp,tmp.widgit)

    def show_mail(self,item):
        uid=item.uid
        self.uid=uid
        if(not os.path.exists('C:\\MailServer\\'+uid+'.txt')):
            self.mail_server.pop3.recvmail('RETR',item.index)
        f=open('C:\\MailServer\\'+uid+'.txt')
        msg=f.read()
        try:
            self.main_window.textBrowser.setText(msg)
        except Exception as e:
            print(e)

class List_item(QtWidgets.QListWidgetItem):
    def __init__(self,subject,sender,uid,index):
        super().__init__()
        self.uid=uid
        self.index=index
        self.widgit=QtWidgets.QWidget()
        self.subject_label=QtWidgets.QLabel()
        self.subject_label.setText(subject)
        self.sender_label=QtWidgets.QLabel()
        self.sender_label.setText(sender)
        self.hbox=QtWidgets.QVBoxLayout()
        self.hbox.addWidget(self.sender_label)
        self.hbox.addWidget(self.subject_label)
        self.widgit.setLayout(self.hbox)
        self.setSizeHint(self.widgit.sizeHint())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    buss = BussLogic()
    buss.sign_in_window.exec()
    # if(BussLogic.win_stage==0):
    #     exit()
    buss.main_window.show()
    sys.exit(app.exec_())

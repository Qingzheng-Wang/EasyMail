from SigninWindow import Ui_Dialog as SignWindow_Ui
from MainWindow import Ui_Form as MainWindow_Ui
from PyQt5 import QtCore, QtWidgets
import sys

class SignWindowUi(QtWidgets.QDialog, SignWindow_Ui):
    def __init__(self):
        super(SignWindowUi, self).__init__()
        self.setupUi(self)

class MainWindowUi(QtWidgets.QWidget, MainWindow_Ui):
    def __init__(self):
        super(MainWindowUi, self).__init__()
        self.setupUi(self)
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    signWindow = SignWindowUi()
    signWindow.show()
    mainWindow = MainWindowUi()
    signWindow.pushButtonSignin.clicked.connect(lambda: {signWindow.close(), mainWindow.show()})
    sys.exit(app.exec_())
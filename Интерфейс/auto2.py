from uis.auto import Ui_Dialog
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import roli2
import lk2
from run import Run


class Account(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(self.Reg)
        self.ui.pushButton.clicked.connect(self.login)
        self.note = QtWidgets.QErrorMessage()
        self.r = Run()



    def Reg(self):
        adr = self.ui.lineEdit_6.text()
        fio = self.ui.lineEdit_5.text()
        log = self.ui.lineEdit_3.text()
        pas = int(self.ui.lineEdit_4.text())
        vs = int(self.ui.lineEdit_7.text())
        kldtp = int(self.ui.lineEdit_8.text())
        klnsh = int(self.ui.lineEdit_9.text())
        self.r.reg_users(adr, log, fio, vs, kldtp, klnsh, pas)
        # self.ui.lineEdit_6.clear()
        self.note.setWindowTitle("Успех")
        self.note.showMessage("Регистрация успешна")

    def login(self):
        log = self.ui.lineEdit.text()
        pas = self.ui.lineEdit_2.text()
        adr = self.r.get_adr(log)
        user = self.r.get_user(adr)
        if user[1] == 0 or user[1] == 1:
            self.open = roli2.Account(adr)
            self.open.show()
        if user[1] == 2 or user[1] == 3:
            self.open = lk2.Account(adr)
            self.open.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = Account()
    myapp.show()
    sys.exit(app.exec())

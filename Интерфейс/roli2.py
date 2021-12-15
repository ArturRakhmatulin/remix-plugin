from uis.roli import Ui_DialogRoli
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import run


class Account(QtWidgets.QMainWindow):
    def __init__(self, adr):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_DialogRoli()
        self.ui.setupUi(self)
        self.r = run.Run()
        self.adr = adr
        self.balanc = self.r.w3.eth.getBalance(self.adr)
        self.ui.label_3.setText(str(self.balanc / 10 ** 18))
        user = self.r.get_user(adr)
        print(user)
        self.role = user[1]
        if self.role == 0:
            self.ui.label.setText("БАНК")
        if self.role == 1:
            self.ui.label.setText("СТРАХОВАЯ КОМПАНИЯ")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = Account("0xCe33952B10b0E59ACD13CB8EfedfddBE364D562A")
    myapp.show()
    sys.exit(app.exec())

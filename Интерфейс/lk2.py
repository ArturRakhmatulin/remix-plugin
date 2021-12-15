from uis.lk import Ui_DialogLK
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import run


class Account(QtWidgets.QMainWindow):
    def __init__(self, adr):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_DialogLK()
        self.ui.setupUi(self)
        self.run = run.Run()
        self.adr = adr
        self.ui.pushButton.clicked.connect(self.reg_license)
        self.ui.pushButton_2.clicked.connect(self.prolong_license)
        self.ui.pushButton_3.clicked.connect(self.reg_car)
        self.ui.pushButton_8.clicked.connect(self.add_accident)
        self.ui.pushButton_5.clicked.connect(self.countCV)
        self.ui.pushButton_6.clicked.connect(self.pay_fee)
        self.ui.pushButton_4.clicked.connect(self.add_fine)
        self.ui.pushButton_7.clicked.connect(self.pay_fine)
        user = self.run.get_user(self.adr)
        rol = user[1]
        if rol != 3:
            self.ui.tab_5.deleteLater()
        self.info()
        self.note = QtWidgets.QErrorMessage()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.info)
        self.timer.start(3000)

    def info(self):
        self.balanc = self.run.w3.eth.getBalance(self.adr)
        self.ui.label_5.setText(str(self.balanc / 10 ** 18) + " ETH")
        user = self.run.get_user(self.adr)
        self.ui.label_4.setText(str(user[0]))
        self.ui.label_14.setText(str(user[3]))
        self.ui.label_16.setText(str(user[4]))
        self.ui.label_18.setText(str(user[5]))
        sv = round(user[6] / 10 ** 18, 2)
        self.ui.label_20.setText(str(sv) + " ETH")
        self.ui.label_28.setText(str(user[8]))
        self.ui.label_27.setText(str(user[9]))


        if user[2] == 1000:
            self.ui.label_10.setText("НЕуказанно")
            self.ui.label_11.setText("НЕуказанно")
            self.ui.label_12.setText("НЕуказанно")
        else:
            li = self.run.lisenses(user[2])
            self.ui.label_10.setText(str(li[0]))
            self.ui.label_11.setText(str(li[1]))
            if li[2] == 1:
                self.ui.label_12.setText("A")
            if li[2] == 2:
                self.ui.label_12.setText("B")
            if li[2] == 3:
                self.ui.label_12.setText("C")

    def reg_license(self):
        try:
            nomer = int(self.ui.lineEdit.text())
            sroc = int(self.ui.lineEdit_2.text())
            kateg = self.ui.lineEdit_3.text()
            if kateg == "A":
                kateg = 1
            if kateg == "B":
                kateg = 2
            if kateg == "C":
                kateg = 3
            ad = self.run.lisenses(nomer)[3]
            if ad == '0x0000000000000000000000000000000000000000':
                self.run.reg_license(nomer, sroc, kateg, self.adr)
                self.note.setWindowTitle("Успех")
                self.note.showMessage("Добавлено успешно")
            else:
                self.note.setWindowTitle("Ошибка")
                self.note.showMessage("Лицензия занята")
        except:
            self.note.setWindowTitle("Ошибка")
            self.note.showMessage("Проверьте данные")

    def prolong_license(self):
        user = self.run.get_user(self.adr)
        kl = user[5]
        if kl == 0:
            nomer = user[2]
            self.run.prolong_license(nomer, self.adr)
            li = self.run.lisenses(nomer)
            self.ui.label_11.setText(str(li[1]))
            self.note.setWindowTitle("Успех")
            self.note.showMessage("Продление успешно")
        else:
            self.note.setWindowTitle("Ошибка")
            self.note.showMessage("Оплатите штраф")

    def reg_car(self):
        try:
            category = self.ui.lineEdit_4.text()
            if category == "A":
                category = 1
            if category == "B":
                category = 2
            if category == "C":
                category = 3
            user = self.run.get_user(self.adr)
            cat = self.run.lisenses(user[2])[2]
            if category == cat:
                lifetime = int(self.ui.lineEdit_6.text())
                market_price = int(self.ui.lineEdit_5.text())
                self.run.reg_car(category, lifetime, market_price, self.adr)

                lifetime = user[8]
                market_price = user[9]
                self.ui.label_28.setText(str(lifetime))
                self.ui.label_27.setText(str(market_price))
                self.note.setWindowTitle("Успех")
                self.note.showMessage("ТС успешно добавлено")
            else:
                self.note.setWindowTitle("Ошибка")
                self.note.showMessage("Вы не имеете необходимой категориеи")
        except:
            self.note.setWindowTitle("Ошибка")
            self.note.showMessage("Проверьте данные")

    def countCV(self):
        user = self.run.get_user(self.adr)
        rc = user[9]
        if rc != 0:
            ci = user[8]
            klnsh = user[5]
            kldtp = user[4]
            vs = user[3]
            SV = abs(rc * abs(1 - ci / 10) * 0.1 + 0.2 * klnsh + kldtp - 0.2 * vs)
            SV = round(SV, 3)
            self.ui.label_21.setText(str(SV) + " ETH")
        else:
            self.note.setWindowTitle("Ошибка")
            self.note.showMessage("Вы Успешно оплатили взно")

    def pay_fee(self):
        user = self.run.get_user(self.adr)
        sv = self.ui.label_21.text()
        if sv != "":
            sv = int(float(self.ui.label_21.text()[:-4]) * 10 ** 18)
            self.run.pay_fee(sv, self.adr)
            sv = round(user[6] / 10 ** 18, 2)
            self.ui.label_20.setText(str(sv) + " ETH")
            self.note.setWindowTitle("Успех")
            self.note.showMessage("Вы Успешно оплатили взнос")
        else:
            self.note.setWindowTitle("Ошибка")
            self.note.showMessage("рассчитайте страховой взнос")

    def add_accident(self):
        nomer = int(self.ui.lineEdit_8.text())
        self.run.add_accident(nomer, self.adr)
        user = self.run.get_user(self.adr)
        value = user[6] * 10
        self.run.payment_fee(nomer, value, self.adr)
        self.note.setWindowTitle("Успех")
        self.note.showMessage("Вы Успешно выписали штраф")

    def add_fine(self):
        nomer = int(self.ui.lineEdit_7.text())
        self.run.add_fine(nomer, self.adr)
        self.note.setWindowTitle("Успех")
        self.note.showMessage("Вы Успешно оформили ДТП ")

    def pay_fine(self):
        user = self.run.get_user(self.adr)
        klnsh = user[5]
        if klnsh != 0:
            self.run.pay_fine(self.adr)
            self.note.setWindowTitle("Успех")
            self.note.showMessage("Вы Успешно оплатили штраф ")
        else:
            self.note.setWindowTitle("Ошибка")
            self.note.showMessage("У Вас нет штраф ")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = Account("0x4788E1180653b6515153148eA1B052b89Fe17c2A")
    # myapp = Account("0x4a33bb269609BF21FB8B76F95e6955fb2A74Bd02")
    myapp.show()
    sys.exit(app.exec())

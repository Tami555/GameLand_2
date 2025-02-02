import os
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow


class Registration(QMainWindow):
    """ Главный класс для идентификации пользователя от него идет выбор -> регистрация или вход"""
    finished = pyqtSignal()

    def __init__(self, l, s):
        """ l, s - классы регистрации или входа"""
        super().__init__()
        self.setFixedSize(625, 778)
        self.move(400, 0)
        self.l = l
        self.s = s
        uic.loadUi(f'{os.getcwd()}/all_registration.ui', self)
        self.btn_sign_up.clicked.connect(self.sign)
        self.btn_login_up.clicked.connect(self.login)

    def login(self):
        """Для входа в существующий аккаунт"""
        self.hide()
        self.l.show()

    def sign(self):
        """Для регистрации (нового аккаунта)"""
        self.hide()
        self.s.show()

    def closeEvent(self, event):
        """При закрытии создаем сигнал"""
        super().closeEvent(event)
        self.finished.emit()
        os.chdir('..')
        print('Final rega', os.getcwd())


# app = QApplication(sys.argv)
# login = SignLogin('Log_in.ui', 2)
# sign = SignLogin('Sign_up.ui', 1)
#
# win = Registration(login, sign)
#
# win.show()
# sys.exit(app.exec())
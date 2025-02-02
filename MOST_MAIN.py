"""Самый главный файл, объединяет все остальные"""
import sys, os
import traceback
from PyQt6 import uic
from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtGui import QMovie
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from Registration.rrrr import Registration
from Registration.Sign_or_Login import SignLogin
from Profile.pppp import Profile
from Profile.Edit_profile import Edit

from Profile.Block_game import BoxGame
from ALL_GAMES.Sapper_game.sapper_game import main as sapper
from ALL_GAMES.Geese_Game.main import main as geese
from ALL_GAMES.Cow_game.cow_game import game_main as cow


class Preview(QMainWindow):
    """Окно для показа превью"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GameLand')
        self.setFixedSize(480, 480)
        self.move(500, 100)
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 480, 480)
        background = QMovie('gameLand_move.gif')
        self.label.setMovie(background)
        background.start()
        QTimer.singleShot(4500, self.close)

    def closeEvent(self, event):
        # Вызываем сигнал, что бы сообщить о закрытии окна
        self.closed.emit()
        super().closeEvent(event)

    closed = pyqtSignal()


class Started(QMainWindow):
    """ Основной класс (самый важный) в нем объединяется и регистрация и игры и само окно"""

    def __init__(self):
        super().__init__()
        uic.loadUi('MOST_MAIN_STYLE.ui', self)
        self.setFixedSize(625, 778)
        self.move(400, 0)
        self.btn_started.clicked.connect(self.starting)
        self.registration = self.profile = None
        self.is_hidden = False  # Флаг для отслеживания состояния окна

    def read_file(self):
        """Читаем файл"""
        try:
            with open(f'./now_user.txt', 'r', encoding='utf-8') as file:
                line_data = file.readline()
                print('Читаю', line_data)
                return False if line_data == '' else True
        except FileNotFoundError:
            return False

    def starting(self):
        """Запускаем приложение по кнопке Start"""
        try:
            if not self.is_hidden:
                self.hide()  # Скрываем окно Started перед открытием других окон
                self.is_hidden = True

            if self.read_file() is False:
                # Если файл пустой, отправляем пользователя на регистрацию (или на вход)
                self.open_registration()

            else:
                # Иначе, сразу открывается аккаунт пользователя
                self.show_profile()
        except Exception as e:
            print(e, 'starting')

    def open_registration(self):
        """Для показа регистрации ил входа"""
        try:
            os.chdir('Registration')
            login = SignLogin(f'{os.getcwd()}/Log_in.ui', 2)  # Окно для входа
            sign = SignLogin(f'{os.getcwd()}/Sign_up.ui', 1)  # Окно для регистрации
            self.registration = Registration(login, sign)  # Окно родительское (выбор: рега или вход)

            login.get_parent(self.registration)
            sign.get_parent(self.registration)

            self.registration.show()
            self.registration.finished.connect(self.registration_closed)
        except Exception as e:
            print(e, 'reg error')

    def show_profile(self):
        """Для показа профиля с играми"""
        try:
            self.profile = Profile([x[1] for x in all_games])  # Окно самого профиля
            edit_win = Edit(self.profile.data, self.profile.signals)  # Окно для изменения профиля
            self.profile.get_edit(edit_win)

            # Игры и их добавление
            self.add_games()
            self.profile.show()
            self.profile.finished.connect(self.profile_closed)
        except Exception as e:
            print(e)

    def add_games(self):
        global all_games
        for img, title, fun_game in all_games:
            g = BoxGame(img, title, fun_game)
            self.profile.create_games(g.forma)

    def registration_closed(self):
        """Обработка закрытия регистрации"""
        self.show()  # показываем окно started после закрытия окна registration
        self.is_hidden = False  # сбрасываем флаг
        if self.registration:
            self.registration.close()
            self.registration = None

    def profile_closed(self):
        """Обработка закрытия профиля"""
        self.show()  # показываем окно started после закрытия окна profile
        self.is_hidden = False  # сбрасываем флаг
        print('Close Profile')
        if self.profile:
            self.profile.close()
            self.profile = None


# Чтобы добавить игру, нужно ее импортировать, добавить в этот массив и подключить checking_the_record
all_games = [(r'..\ALL_GAMES\Sapper_game\icon.png', 'Sapper', sapper),
             (r'..\ALL_GAMES\Geese_Game\icon.jpg', 'Catch a goose', geese),
             (r'..\ALL_GAMES\Cow_game\data\cow_icon.jpg', 'Cowscape', cow)]

if __name__ == "__main__":
    try:
        print(os.getcwd())
        app = QApplication(sys.argv)
        pr = Preview()
        start = Started()
        pr.closed.connect(start.show)
        pr.show()
        sys.exit(app.exec())
    except Exception as e:
        print(e, 'n')
        traceback.print_exc()
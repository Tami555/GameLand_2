from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QVBoxLayout, QWidget, QTableWidgetItem
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import pyqtSignal, QObject
from work_database_fail import create_now_user, get_infa
import os


class EditSignals(QObject):
    """Класс для передачи сигнала"""
    edit_closed = pyqtSignal()


class Profile(QMainWindow):
    """Класс профиля пользователя"""
    finished = pyqtSignal()

    def __init__(self, lst_games):
        super().__init__()
        print('CREATE PROFILE', os.getcwd())
        os.chdir('Profile')
        uic.loadUi(f'{os.getcwd()}\\profile_window.ui', self)
        self.setFixedSize(841, 615)
        self.lst_games = lst_games
        # Для My profile
        self.data = None
        self.full_infa_user()
        self.leave_account_btn.clicked.connect(self.leave_account)  # Кнопка для выхода из аккаунта
        self.edit_profile.clicked.connect(self.edit_account)  # Кнопка для редактирования программы

        self.signals = EditSignals()  # Сигналы для быстрого обновления профиля
        self.signals.edit_closed.connect(self.full_infa_user)

        self.layout = QVBoxLayout()  # Сбор блоков игр
        self.layout.setSpacing(30)
        self.w = QWidget()
        self.w.setLayout(self.layout)
        self.scroll_area.setWidget(self.w)

        self.full_table_records()  # Заполнение таблицы рекордов
        self.tabWidget.currentChanged.connect(self.on_tab_changed)

    def full_infa_user(self):
        """Заполняет информацию о пользователе (My profile)"""
        try:
            file = open("C:\\Users\\Tami\\Desktop\\New_Game\\now_user.txt", 'r', encoding='utf-8')
            infa = file.readline()
            if infa != '':
                infa = infa.split(';')
                self.data = infa
                self.for_name.setText(infa[0])
                self.for_email.setText(infa[2])
                self.for_password.setText(infa[1])
                self.avatar.setPixmap(QPixmap(f'./Avatars/{infa[3]}.jpg'))
                file.seek(0)
        except Exception as e:
            print('Проблема с пользовательским файлом!!!!!', e)

    def leave_account(self):
        """Выход из аккаунта (с подтверждением)"""
        valid = QMessageBox.question(
            self, '', "Do you really want to log out of your account? ",
            buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if valid == QMessageBox.StandardButton.Yes:
            create_now_user()
            self.close()

    def get_edit(self, edit):
        """Добавление окна для изменения профиля"""
        self.edit_win = edit

    def edit_account(self):
        """Показ окна для изменения профиля"""
        try:
            self.edit_win.show()
        except Exception as e:
            print(e)

    def create_games(self, gamebox):
        """Добавление новых игр"""
        self.layout.addWidget(gamebox)

    def full_table_records(self):
        """Заполнение Таблицы рекордов"""
        try:
            title = ['Games', 'Records']
            self.tableWidget.setColumnCount(len(title))
            self.tableWidget.setHorizontalHeaderLabels(title)
            self.tableWidget.setRowCount(0)
            records = get_infa()[4:]  # получаем список кортежей
            # games = ['Sapper', 'Catch a goose', 'Cowscape']  # это должно быть в столбце Games

            for i in range(len(records)):  # перебираем кортежи и индекс
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)  # добавляем строку
                self.tableWidget.setItem(i, 0, QTableWidgetItem(str(self.lst_games[i])))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(str(records[i])))

        except Exception as e:
            print('Заполнение Таблички :(', e)

    def on_tab_changed(self, index):
        if index == 1:
            self.full_table_records()

    def closeEvent(self, event):
        """При закрытии создаем сигнал"""
        super().closeEvent(event)
        self.finished.emit()
        os.chdir('..')
        print('Final prof', os.getcwd())


# app = QApplication(sys.argv)
# # g1 = BoxGame(r'..\Sapper_game\icon.png', 'Sapper', main)
#
# win = Profile()
# # win.create_games(g1.forma)
# # congratulations = Win_Show() #########
#
# # edit_win = Edit(win.data, win.signals)
# win.show()
# sys.exit(app.exec())
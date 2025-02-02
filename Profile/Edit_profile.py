import re
import sqlite3
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6.QtGui import QPixmap, QImage
from PIL import Image
from check_password import check_password
from work_database_fail import get_infa, create_now_user, update_result_DB


class Edit(QMainWindow):
    """Окно для изменения профиля"""
    def __init__(self, lst, signals):
        super().__init__()
        # подключаемся к БД
        self.database = sqlite3.connect('C:\\Users\\Tami\\Desktop\\New_Game\\GameLand_db.sql')
        self.cur = self.database.cursor()

        uic.loadUi(r'.\edit_profile.ui', self)
        self.name, self.password, self.email, self.ava = lst[:4]

        self.full_poles()  # Заполнение всех полей
        self.create_ava = self.new_avatar_path = None

        self.update_profile.clicked.connect(self.edit_profile)  # Кнопка для сохранения изменений
        self.signals = signals  # Сигнал для быстрой передачи обновлений род окну

    def mousePressEvent(self, event):
        """ Нажатие на аватарку"""
        if event.button() == Qt.MouseButton.LeftButton:
            if 170 <= event.pos().x() <= 311 and 80 <= event.pos().y() <= 221:
                self.edit_avatar()

    def full_poles(self):
        # os.chdir('..')
        self.avatar_ed.setPixmap(QPixmap(f'./Avatars/{self.ava}.jpg'))
        self.name_ed.setText(self.name)
        self.email_ed.setText(self.email)
        self.password_ed.setText(self.password)

    def edit_avatar(self):
        """Изменение аватарки"""
        try:
            fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '',
                                                'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')[0]
            if fname:
                img = Image.open(fname)
                #  Для идентификации фотографий
                count = self.cur.execute('SELECT COUNT(*) FROM users;').fetchone()[0]
                query_rank = """SELECT rank FROM (SELECT *, ROW_NUMBER() OVER (ORDER BY Password) AS rank FROM users)
                             AS subquery WHERE Password = ?; """
                count += self.cur.execute(query_rank, (self.password,)).fetchone()[0]
                self.create_ava = f'user{count}'
                self.new_avatar_path = f'./Avatars/{self.create_ava}.jpg'

                img_q = QImage(fname)
                img_q = QPixmap.fromImage(img_q).scaled(141, 141)
                self.avatar_ed.setPixmap(img_q)

                self.message_ed.setStyleSheet("color: green;")
                self.message_ed.setText('Avatar is loaded, but not saved yet!')

        except Exception as e:
            self.message_ed.setStyleSheet("color: red;")
            self.message_ed.setText('Error with the image')
            print(e)

    def edit_other_data(self):
        """Проверка всех остальных введенных данных"""
        try:
            # Проверка на корректность данных (пароля, почты, имени)
            password = self.password_ed.text()
            email = self.email_ed.text()
            name = self.name_ed.text()

            parol_message = check_password(password)
            email_message = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
            infa = get_infa(password)

            print('Введенный пароль:', password)
            print('Наш пароль:', self.password)

            if isinstance(parol_message, str) or\
                    email_message is None or \
                    (infa is not None and password != self.password) or\
                    name == '':

                self.message_ed.setStyleSheet("color: red;")

                if infa is not None and password != self.password:
                    msg = 'This password is busy, come up with another one'
                    print('Проблема с паролем', infa, password, self.password)

                elif isinstance(parol_message, str):
                    msg = parol_message
                    print('Не корректный паролъ')

                elif name == '':
                    msg = 'An empty field'

                elif email_message is None:
                    msg = 'Invalid email address.'

                self.message_ed.setText(msg)
                print('НЕ могу обновить профиль, ОШИБКИ')
                return None
            else:
                return name, email, password
        except Exception as e:
            print(e)

    def edit_profile(self):
        """Обновляет все данные (для Кнопки)"""
        try:
            data = self.edit_other_data()
            p = None
            if data is not None:
                print('HRERE 1')
                n, e, p = data
                update_result_DB('Name', n, self.password)
                update_result_DB('Email', e, self.password)
                update_result_DB('Password', p, self.password)
                print('HRERE 2')

            # if self.create_ava is not None:
            #     update_result_DB('Avatar', self.create_ava, self.password)
            if self.new_avatar_path:
                self.avatar_ed.pixmap().toImage().save(self.new_avatar_path)
                img = Image.open(self.new_avatar_path)
                update_result_DB('Avatar', self.create_ava, self.password)

            if p is not None:
                res = get_infa(p)
                create_now_user(res)
                self.password = p
                self.close()

        except Exception as e:
            print(e)
            # self.close()

    def closeEvent(self, event):
        self.signals.edit_closed.emit()
        self.message_ed.setText('')
        super().closeEvent(event)


# app = QApplication(sys.argv)
# win = Edit('Антон',  'antony@gmail.com', 'qwaszx123A', 'non_person')
# win.show()
# sys.exit(app.exec())
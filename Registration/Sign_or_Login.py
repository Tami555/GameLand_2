import re
import sqlite3
import os
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QTimer
from check_password import check_password
from work_database_fail import get_infa, create_now_user


class SignLogin(QMainWindow):
    """Класс для входа и для регистрации"""
    def __init__(self, interface, word):
        super().__init__()
        self.setFixedSize(625, 778)
        self.move(400, 0)
        uic.loadUi(interface, self)

        # подключаемся к БД
        os.chdir('..')
        self.database = sqlite3.connect('C:\\Users\\Tami\\Desktop\\New_Game\\GameLand_db.sql')
        self.cur = self.database.cursor()
        os.chdir('Registration')

        # стрелочка для закрытия окна
        self.arrow_return.setIcon(QIcon('return.png'))
        self.arrow_return.clicked.connect(self.for_arrow)

        if word == 1:
            self.btn_sign_up_go.clicked.connect(self.go_sign)  # кнопка для регистрации
        else:
            self.btn_login_up_go.clicked.connect(self.go_login)  # кнопка для входа

        # получение имя, почты и пароля пользователя
        self.name = ''
        self.email = ''
        self.password = ''
        self.parent = None

    def get_parent(self, parent):
        """Добавление Родителя"""
        self.parent = parent

    def for_arrow(self):
        """Для стрелочки"""
        self.close()
        self.parent.show()

    @staticmethod
    def check_full(pole, answer):
        """Проверка наличия данных в полях"""
        if pole == '':
            answer.setStyleSheet("color: red;")
            answer.setText('the field must be filled in')
            return False
        answer.setStyleSheet("color: green;")
        answer.setText('good')
        return True

    def go_sign(self):
        """Метод для регистрации аккаунта (окно регистрации)"""
        try:
            """ Получаем данные из ввода и обращаемся к БД """
            self.password = self.line_password.text()
            self.email = self.line_email.text()
            self.name = self.line_name.text()

            n = self.check_full(self.name, self.answer_message_1)
            e = self.check_full(self.email, self.answer_message_3)
            p = self.check_full(self.password, self.answer_message_2)

            if p and n and e:
                """ Обращение к БД для создания новой записи о пользователе"""
                # Проверка на корректность данных (пароля и почты)
                parol_message = check_password(self.password)
                email_message = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.email)
                print(email_message)
                if isinstance(parol_message, str) or not email_message:
                    if isinstance(parol_message, str):
                        self.answer_message_2.setStyleSheet("color: red;")
                        self.answer_message_2.setText(parol_message)

                    if not email_message:
                        self.answer_message_3.setStyleSheet("color: red;")
                        self.answer_message_3.setText("Invalid email address.")
                else:
                    result = get_infa(self.password)

                    if result is None:
                        self.cur.execute("""
                            INSERT INTO users(Name, Password, Email)
                            VALUES(?, ?, ?)""", (self.name, self.password, self.email))
                        self.database.commit()

                        # Записываем пользователя
                        result = get_infa(self.password)
                        create_now_user(result)
                        QTimer.singleShot(1000, self.close)  # закрываем текущее окно
                        self.parent.close()

                    else:
                        self.answer_message_2.setStyleSheet("color: red;")
                        self.answer_message_2.setText('This password is busy, come up with another one')
                    self.database.commit()

        except Exception as e:
            print(e)

    def go_login(self):
        """Метод для входа в аккаунт (окно входа)"""
        try:
            """ Получаем данные из ввода и обращаемся к БД """
            self.password = self.line_password.text()
            self.name = self.line_name.text()

            n = self.check_full(self.name, self.answer_message_1)
            p = self.check_full(self.password, self.answer_message_2)
            if p and n:
                # Обращение к БД для получения данных о существующем пользователе (по имени и паролю)
                result = self.cur.execute("""
                                SELECT * FROM users WHERE Password = ? AND Name = ?""",
                                          (self.password, self.name)).fetchone()
                if result is None:
                    self.answer_message_2.setStyleSheet("color: red;")
                    self.answer_message_2.setText('The username or password is incorrect!!!')

                else:
                    print(f'Есть такой Пользователь, это же {result[0]}')
                    create_now_user(result)
                    QTimer.singleShot(1000, self.close)  # закрываем текущее окно
                    self.parent.close()

        except Exception as e:
            print(e)

    def closeEvent(self, event):
        # перед закрытием окна очищаем ввод
        try:
            self.line_password.setText('')
            self.answer_message_2.setText('')

            self.line_name.setText('')
            self.answer_message_1.setText('')

            self.line_email.setText('')
            self.answer_message_3.setText('')
        except Exception:
            pass
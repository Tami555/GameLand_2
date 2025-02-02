from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QPushButton
from PyQt6.QtGui import QPixmap


class BoxGame:
    """ Класс для создания блока игр"""
    def __init__(self, img, title, app):
        self.img = img
        self.title = title
        self.app = app
        self.forma = self.create_form()

    def create_form(self):
        forma = QLabel()
        forma.setFixedSize(600, 100)
        forma.setStyleSheet('background: black;')

        lay_h = QHBoxLayout()

        icon = QLabel()
        icon.setPixmap(QPixmap(self.img))
        icon.setFixedSize(50, 50)

        title = QLabel(f"{self.title}")
        title.setFixedSize(180, 41)
        title.setStyleSheet("""
        font-family: "Cascadia Momo SemiBold";
        font-size: 20pt;
        color: white;""")

        play_btn = QPushButton('Play')
        play_btn.setFixedSize(141, 41)
        play_btn.setStyleSheet("""
        font-family: "Cascadia Code SemiBold";
        font-size: 10pt;
        color: white;
        background: #46CC00;
        """)
        play_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        play_btn.clicked.connect(self.app)

        lay_h.addWidget(icon)
        lay_h.addWidget(title)
        lay_h.addWidget(play_btn)
        forma.setLayout(lay_h)
        return forma
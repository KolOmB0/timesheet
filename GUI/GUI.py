# -*- coding: utf-8 -*-
# Created by: PyQt5 UI code generator 5.15.11
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QDateEdit, QLabel
)
from PyQt5.QtCore import QCoreApplication, QDate

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("Dialog")

        # Левый блок: дата + кнопки
        self.date = QDateEdit()
        self.date.setObjectName("data")
        self.date.setDate(QDate.currentDate())
        self.date.setDisplayFormat("MM.yyyy")

        self.button1 = QPushButton()
        self.button2 = QPushButton()
        self.button3 = QPushButton()
        self.button4 = QPushButton()
        self.button5 = QPushButton()
        self.button6 = QPushButton()

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.date)
        left_layout.addWidget(self.button1)
        left_layout.addWidget(self.button2)
        left_layout.addWidget(self.button3)
        left_layout.addWidget(self.button4)
        left_layout.addWidget(self.button5)
        left_layout.addWidget(self.button6)
        left_layout.addStretch()

        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        left_widget.setFixedWidth(100)

        # Правый блок (будущая таблица)
        self.content_area = QLabel("Здесь будет таблица")
        self.content_area.setStyleSheet("background-color: #f0f0f0; border: 1px solid gray;")
        self.content_area.setMinimumWidth(400)

        # Основной макет
        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.content_area)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.name_widgets_object()

        # Подключение сигналов
        self.button1.clicked.connect(lambda: self.show_content("Табель учета рабочего времени"))
        self.button2.clicked.connect(lambda: self.show_content("Табель сменности"))
        self.button3.clicked.connect(lambda: self.show_content("Развозка"))
        self.button4.clicked.connect(lambda: self.show_content("Обеды"))
        self.button5.clicked.connect(lambda: self.show_content("Отпуска"))
        self.button6.clicked.connect(lambda: self.show_content("Сотрудники"))

    def name_widgets_object(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Табель"))
        self.button1.setText(_translate("QPushButton1", "Табель учета рабочего времени"))
        self.button2.setText(_translate("QPushButton2", "Табель сменности"))
        self.button3.setText(_translate("QPushButton3", "Развозка"))
        self.button4.setText(_translate("QPushButton4", "Обеды"))
        self.button5.setText(_translate("QPushButton5", "Отпуска"))
        self.button6.setText(_translate("QPushButton6", "Сотрудники"))

    def show_content(self, text):
        self.content_area.setText(f"Выбрано: {text}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
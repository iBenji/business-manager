import sys
import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget, QMessageBox, QLabel, QLineEdit

app = QApplication(sys.argv)

#! Настройки основного окна
window = QMainWindow()
window.setWindowTitle("depShop Интерфейс")
window.setGeometry(100, 100, 600, 400)
window.setStyleSheet("background-color: rgba(68, 68, 68, 1);")

#! Настройки менюбара
menubar = QMenuBar(window)
menubar.setStyleSheet("color: rgba(255, 255, 255, 1);")
# ? Вкладки в менюбаре
file_menu = menubar.addMenu("Менеджер")
products_menu = file_menu.addMenu("Продукции")

# TODO Настройка Продукция Apple
apple_menu = products_menu.addAction("Продукция Apple")
apple_window = None  # Глобальная переменная для ссылки на окно "Продукция Apple"
profit_lineEdit = None


def open_apple_products():
    global apple_window
    global table
    global profit_lineEdit
    
    # Если окно уже открыто, не создаем новое окно, а просто активируем его
    if apple_window is not None:
        apple_window.showNormal()
        apple_window.activateWindow()
        return

    # Создание нового окна
    apple_window = QMainWindow()
    apple_window.setWindowTitle("Продукция Apple")
    apple_window.setGeometry(200, 200, 800, 600)
    apple_window.setStyleSheet("background-color: rgba(68, 68, 68, 1);")

    # Создание таблицы с данными
    table = QTableWidget(apple_window)
    table.setGeometry(0, 0, 800, 500)
    table.setStyleSheet("background-color: rgba(68, 68, 68, 1);")
    table.setStyleSheet("color: rgba(0, 196, 3, 1);")
    table.setColumnCount(5)  # Указывает количество колонок
    table.setHorizontalHeaderLabels(['Название', 'Стоимость', 'Состояние', 'Страна привоза', 'Количество'])
    table.horizontalHeader().setDefaultSectionSize(130)  # Установка ширины заголовка

    # Загрузка данных из файла
    load_data()

    # Добавление данных в таблицу
    table.setRowCount(1)  # Указывает количество строк

    # Создание метки и поля ввода для прибыли
    profit_label = QLabel("Прибыль:", apple_window)
    profit_label.setStyleSheet("color: rgba(255, 255, 255, 1);")
    profit_label.setGeometry(20, 520, 70, 30)

    profit_lineEdit = QLineEdit(apple_window)
    profit_lineEdit.setStyleSheet("background-color: rgba(255, 255, 255, 1);")
    profit_lineEdit.setGeometry(100, 520, 150, 30)
    profit_lineEdit.setReadOnly(True)

    # Создание кнопки "Рассчитать прибыль"
    calculate_button = QPushButton("Рассчитать прибыль", apple_window)
    calculate_button.setStyleSheet("background-color: rgba(38, 38, 38, 1);")
    calculate_button.setStyleSheet("color: rgba(0, 153, 255, 1);")
    calculate_button.setGeometry(270, 520, 200, 30)
    calculate_button.clicked.connect(calculate_profit_apple)

    # Создание кнопки "добавить строку"
    button = QPushButton("Добавить строку", apple_window)
    button.setStyleSheet("background-color: rgba(38, 38, 38, 1);")
    button.setStyleSheet("color: rgba(0, 153, 255, 1);")
    button.setGeometry(300, 520, 200, 30)
    button.clicked.connect(add_apple_row)

    # Создание кнопки "сохранить"
    save_button = QPushButton("Сохранить", apple_window)
    save_button.setStyleSheet("background-color: rgba(38, 38, 38, 1);")
    save_button.setStyleSheet("color: rgba(0, 153, 255, 1);")
    save_button.setGeometry(600, 520, 200, 30)
    save_button.clicked.connect(save_data)

    # Размещение таблицы и кнопок на виджете
    widget = QWidget(apple_window)
    layout = QVBoxLayout(widget)
    layout.addWidget(table)
    layout.addWidget(profit_label)
    layout.addWidget(profit_lineEdit)
    layout.addWidget(calculate_button)
    layout.addWidget(button)
    layout.addWidget(save_button)
    widget.setLayout(layout)

    apple_window.setCentralWidget(widget)
    
    # Добавление обработчика события закрытия окна
    apple_window.closeEvent = lambda event: reset_profit_lineEdit(profit_lineEdit)
    apple_window.show()

def calculate_profit_apple():
    total_profit = 0

    for row in range(table.rowCount()):
        price_item = table.item(row, 1)
        quantity_item = table.item(row, 4)

        if price_item is not None and quantity_item is not None:
            price = float(price_item.text())
            quantity = int(quantity_item.text())

            total_profit += price * quantity

    profit_lineEdit.setText(str(total_profit))


def load_data():
    try:
        with open('data.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            data = list(reader)
        table.setRowCount(len(data))
        for row in range(len(data)):
            for column in range(table.columnCount()):
                item = QTableWidgetItem(data[row][column])
                table.setItem(row, column, item)
    except FileNotFoundError:
        pass


def save_data():
    data = []
    for row in range(table.rowCount()):
        row_data = []
        for column in range(table.columnCount()):
            item = table.item(row, column)
            if item is not None:
                row_data.append(item.text())
            else:
                row_data.append('')
        data.append(row_data)
    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    QMessageBox.information(
        apple_window, "Сохранение данных", "Данные успешно сохранены.")


def add_apple_row():
    global apple_window

    # Если окно не было создано, ничего не делаем
    if apple_window is None:
        return

    # Получаем таблицу из окна и определяем текущее количество строк
    table = apple_window.centralWidget().layout().itemAt(0).widget()
    current_row_count = table.rowCount()

    # Добавляем новую строку
    table.setRowCount(current_row_count + 1)

    # Устанавливаем пустые ячейки для новой строки
    for column in range(table.columnCount()):
        table.setItem(current_row_count, column, QTableWidgetItem(""))


apple_menu.triggered.connect(open_apple_products)

# TODO Настройка Электронные товары
electronics_menu = products_menu.addAction("Электронные товары")
# Глобальные переменные
electronics_window = None

def open_electronics_products():
    global electronics_window
    global electronics_table
    global profit_lineEdit

    # Если окно уже открыто, не создаем новое окно, а просто активируем его
    if electronics_window is not None:
        electronics_window.showNormal()
        electronics_window.activateWindow()
        return

    # Создание нового окна
    electronics_window = QMainWindow()
    electronics_window.setWindowTitle("Электронная продукция")
    electronics_window.setGeometry(200, 200, 800, 600)
    electronics_window.setStyleSheet("background-color: rgba(68, 68, 68, 1);")

    # Создание таблицы с данными
    electronics_table = QTableWidget(electronics_window)
    electronics_table.setGeometry(0, 0, 800, 500)
    electronics_table.setStyleSheet("background-color: rgba(68, 68, 68, 1);")
    electronics_table.setStyleSheet("color: rgba(0, 196, 3, 1);")
    electronics_table.setColumnCount(5)  # Указывает количество колонок
    electronics_table.setHorizontalHeaderLabels(
        ['Название', 'Стоимость', 'Состояние', 'Страна привоза', 'Количество'])
    electronics_table.horizontalHeader().setDefaultSectionSize(130)  # Установка ширины заголовка

    # Загрузка данных из файла
    load_electronics_data()

    # Создание метки и поля ввода для прибыли
    profit_label = QLabel("Прибыль:", electronics_window)
    profit_label.setStyleSheet("color: rgba(255, 255, 255, 1);")
    profit_label.setGeometry(20, 520, 70, 30)

    profit_lineEdit = QLineEdit(electronics_window)
    profit_lineEdit.setStyleSheet("background-color: rgba(255, 255, 255, 1);")
    profit_lineEdit.setGeometry(100, 520, 150, 30)
    profit_lineEdit.setReadOnly(True)

    # Создание кнопки "Рассчитать прибыль"
    calculate_button = QPushButton("Рассчитать прибыль", electronics_window)
    calculate_button.setStyleSheet("background-color: rgba(38, 38, 38, 1);")
    calculate_button.setStyleSheet("color: rgba(0, 153, 255, 1);")
    calculate_button.setGeometry(270, 520, 200, 30)
    calculate_button.clicked.connect(calculate_profit_electronic)

    # Создание кнопки "добавить строку"
    button = QPushButton("Добавить строку", electronics_window)
    button.setStyleSheet("background-color: rgba(38, 38, 38, 1);")
    button.setStyleSheet("color: rgba(0, 153, 255, 1);")
    button.setGeometry(300, 520, 200, 30)
    button.clicked.connect(add_electronics_row)

    # Создание кнопки "сохранить"
    save_button = QPushButton("Сохранить", electronics_window)
    save_button.setStyleSheet("background-color: rgba(38, 38, 38, 1);")
    save_button.setStyleSheet("color: rgba(0, 153, 255, 1);")
    save_button.setGeometry(600, 520, 200, 30)
    save_button.clicked.connect(save_electronics_data)

    # Размещение таблицы и кнопок на виджете
    widget = QWidget(electronics_window)
    layout = QVBoxLayout(widget)
    layout.addWidget(electronics_table)
    layout.addWidget(profit_label)
    layout.addWidget(profit_lineEdit)
    layout.addWidget(calculate_button)
    layout.addWidget(button)
    layout.addWidget(save_button)
    widget.setLayout(layout)

    electronics_window.setCentralWidget(widget)
    electronics_window.show()
    # Добавление обработчика события закрытия окна
    electronics_window.closeEvent = lambda event: reset_profit_lineEdit(profit_lineEdit)

    electronics_window.show()


def calculate_profit_electronic():
    total_profit = 0

    for row in range(electronics_table.rowCount()):
        price_item = electronics_table.item(row, 1)
        quantity_item = electronics_table.item(row, 4)

        if price_item is not None and quantity_item is not None:
            price = float(price_item.text())
            quantity = int(quantity_item.text())

            total_profit += price * quantity
            
    profit_lineEdit.setText(str(total_profit))

def reset_profit_lineEdit(lineEdit):
    lineEdit.setText('')

def load_electronics_data():
    try:
        with open('electronics_data.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            data = list(reader)
        electronics_table.setRowCount(len(data))
        for row in range(len(data)):
            for column in range(electronics_table.columnCount()):
                item = QTableWidgetItem(data[row][column])
                electronics_table.setItem(row, column, item)
    except FileNotFoundError:
        pass

def save_electronics_data():
    data = []
    for row in range(electronics_table.rowCount()):
        row_data = []
        for column in range(electronics_table.columnCount()):
            item = electronics_table.item(row, column)
            if item is not None:
                row_data.append(item.text())
            else:
                row_data.append('')
        data.append(row_data)

    with open('electronics_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    QMessageBox.information(electronics_window, "Сохранение данных", "Данные успешно сохранены.")


def add_electronics_row():
    global electronics_window

    # Если окно не было создано, ничего не делаем
    if electronics_window is None:
        return

    # Получаем таблицу из окна и определяем текущее количество строк
    table = electronics_window.centralWidget().layout().itemAt(0).widget()
    current_row_count = table.rowCount()

    # Добавляем новую строку
    table.setRowCount(current_row_count + 1)

    # Устанавливаем пустые ячейки для новой строки
    for column in range(table.columnCount()):
        table.setItem(current_row_count, column, QTableWidgetItem(""))


electronics_menu.triggered.connect(open_electronics_products)

window.setMenuBar(menubar)
window.show()
sys.exit(app.exec())

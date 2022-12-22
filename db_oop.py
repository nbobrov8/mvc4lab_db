#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PySide2.QtWidgets import (
    QTableView,
    QApplication,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QWidget,
    QLineEdit,
    QFrame,
    QLabel,
    QHeaderView,
    QDateEdit,
    QTabWidget
)
from PySide2.QtCore import (
    Signal
)
from PySide2.QtCore import QSortFilterProxyModel, Qt, QRect
import sys


class DateBase:
    def __init__(self, db_file) -> None:
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(db_file)
        if not db.open():
            return False
        self.q = QSqlQuery()
        self.q.exec_(
            """
        CREATE TABLE IF NOT EXISTS Seller (
            "Код продавца" text PRIMARY KEY,
            "ФИО" text,
            "Дата рождения" date,
            "Работает с " date);"""
        )
        self.q.exec_(
            """
        CREATE TABLE IF NOT EXISTS Client (
            "Уникальный номер" text PRIMARY KEY,
            "ФИО" text,
            "Дата покупки" date,
            "Номер телефона" text);"""
        )
        self.q.exec_(
            """
        CREATE TABLE IF NOT EXISTS Board (
            "Уникальный номер" text PRIMARY KEY,
            "Код продавца" text,
            "Способ оплаты" text,
            "Статус сделки" text);"""
        )
        self.q.exec_(
            """INSERT INTO Seller VALUES("RC6", "Бобров Н.В.", "19.12.2002", "01.10.2021")"""
        )
        self.q.exec_(
            """INSERT INTO Seller VALUES("CR7", "Иванов И.И.", "20.12.2001", "01.09.2020")"""
        )
        self.q.exec_(
            """INSERT INTO Seller VALUES("MS1", "Смирнов С.С.", "14.05.2000", "24.03.2019")"""
        )
        self.q.exec_(
            """INSERT INTO Seller VALUES("NJ2", "Петров А.К.", "01.07.1999", "22.04.2018")"""
        )
        self.q.exec_(
            """INSERT INTO Seller VALUES("LK1", "Сидоров Л.Г.", "24.11.2001", "05.10.2020")"""
        )
        self.q.exec_(
            """INSERT INTO Seller VALUES("OC7", "Овечкин М.О.", "01.09.1995", "14.03.2016")"""
        )
        self.q.exec_(
            """INSERT INTO Client VALUES("202", "Плотников Д.В.", "15.08.2021", "+7 918 765 67 92")"""
        )
        self.q.exec_(
            """INSERT INTO Client VALUES("303", "Злыгостев И.С.", "21.12.2021", "+7 913 445 64 77")"""
        )
        self.q.exec_(
            """INSERT INTO Client VALUES("404", "Галяс Д.И.", "14.06.2020", "+7 909 445 64 70")"""
        )
        self.q.exec_(
            """INSERT INTO Client VALUES("505", "Семенов С.М.", "16.08.2021", "+7 918 777 77 92")"""
        )
        self.q.exec_(
            """INSERT INTO Client VALUES("606", "Шелудько Ч.С.", "22.11.2020", "+7 913 444 44 00")"""
        )
        self.q.exec_(
            """INSERT INTO Client VALUES("707", "Хачатуров Р.К.", "27.10.2022", "+7 909 005 14 17")"""
        )
        self.q.exec_(
            """INSERT INTO Board VALUES("202", "NJ2", "Бесконтактный", "Закрыта")"""
        )
        self.q.exec_(
            """INSERT INTO Board VALUES("303", "LK1", "Наличный расчет", "Активна")"""
        )
        self.q.exec_(
            """INSERT INTO Board VALUES("404", "NJ2", "СБП", "Отложена")"""
        )
        self.q.exec_(
            """INSERT INTO Board VALUES("505", "RC6", "Бесконтактный", "Закрыта")"""
        )
        self.q.exec_(
            """INSERT INTO Board VALUES("606", "CR7", "Наличный расчет", "Закрыта")"""
        )
        self.q.exec_(
            """INSERT INTO Board VALUES("707", "MS1", "СБП", "Отложена")"""
        )


class TableView:
    tabBarClicked = Signal(int)

    def __init__(self, parent):
        self.parent = parent
        self.SetupUI()
        self.current_tab = "Seller"
        self.tab_id = "Код продавца"

    def SetupUI(self):
        self.parent.setGeometry(400, 500, 1000, 650)
        self.parent.setWindowTitle("База данных торгового дома")
        self.main_conteiner = QGridLayout()
        self.frame1 = QFrame()
        self.frame2 = QFrame()
        self.frame2.setVisible(False)
        self.main_conteiner.addWidget(self.frame1, 0, 0)
        self.main_conteiner.addWidget(self.frame2, 0, 0)
        self.frame1.setStyleSheet(
            """
            font-family: montserrat;
            font-size: 12px;
            font: bold;
            """
        )
        self.frame2.setStyleSheet(
            """
            font-family: montserrat;
            font-size: 12px;
            font: bold;
            """
        )
        self.table_view = QTableView()
        self.table_view.setModel(self.tableCar())
        self.table_view2 = QTableView()
        self.table_view2.setModel(self.tableOwner())
        self.table_view3 = QTableView()
        self.table_view3.setModel(self.tableDocs())
        self.table_view.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_view.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table_view.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table_view3.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_view3.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_view3.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table_view3.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table_view2.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_view2.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_view2.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table_view2.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.layout_main = QGridLayout(self.frame1)
        self.layh = QHBoxLayout()
        self.btn_add = QPushButton("Добавить")
        self.btn_del = QPushButton("Удалить")
        self.layh.addWidget(self.btn_add)
        self.layh.addWidget(self.btn_del)
        self.tab_conteiner = QTabWidget()
        self.tab_conteiner.setTabShape(QTabWidget.Triangular)
        self.tab_conteiner.addTab(self.table_view, "Продавцы")
        self.tab_conteiner.addTab(self.table_view2, "Клиенты")
        self.tab_conteiner.addTab(self.table_view3, "Данные о завершенных покупках")
        self.layout_main.addWidget(self.tab_conteiner, 0, 0)
        self.layout_main.addLayout(self.layh, 1, 0)
        self.parent.setLayout(self.main_conteiner)
        self.btn_del.clicked.connect(self.delete)
        self.btn_add.clicked.connect(self.add)
        self.layout_grid = QGridLayout(self.frame2)
        self.btn_add2 = QPushButton("Добавить данные")
        self.btn_add2.setFixedWidth(300)
        self.btn_otmena = QPushButton("Отмена")
        self.line_name = QLineEdit()
        self.name = QLabel("ФИО клиента: ")
        self.doc_num_line = QLineEdit()
        self.doc_num = QLabel("Уникальный номер клиента: ")
        self.color_line = QDateEdit()
        self.color_line.setCalendarPopup(True)
        self.color_line.setTimeSpec(Qt.LocalTime)
        self.color_line.setGeometry(QRect(220, 31, 133, 20))
        self.color = QLabel("Работает с: ")
        self.dateb_line = QDateEdit()
        self.dateb_line.setCalendarPopup(True)
        self.dateb_line.setTimeSpec(Qt.LocalTime)
        self.dateb_line.setGeometry(QRect(220, 31, 133, 20))
        self.dateb = QLabel("Дата продажи: ")
        self.line_pasport = QLineEdit()
        self.pasport = QLabel("Номер телефона: ")
        self.vin_line = QLineEdit()
        self.vin = QLabel("ФИО продавца: ")
        self.marka_line = QDateEdit()
        self.marka_line.setCalendarPopup(True)
        self.marka_line.setTimeSpec(Qt.LocalTime)
        self.marka_line.setGeometry(QRect(220, 31, 133, 20))
        self.marka = QLabel("Дата рождения продавца: ")
        self.uid_line = QLineEdit()
        self.uid = QLabel('Уникальный код продавца')
        self.model_line = QLineEdit()
        self.docs_reg = QLabel("Способ оплаты: ")
        self.docs_reg_line = QLineEdit()
        self.cate_line = QLineEdit()
        self.cate = QLabel("Статус сделки: ")
        self.layout_grid.addWidget(self.line_name, 0, 1)
        self.layout_grid.addWidget(self.name, 0, 0)
        self.layout_grid.addWidget(self.doc_num, 1, 0)
        self.layout_grid.addWidget(self.doc_num_line, 1, 1)
        self.layout_grid.addWidget(self.dateb, 2, 0)
        self.layout_grid.addWidget(self.dateb_line, 2, 1)
        self.layout_grid.addWidget(self.marka_line, 3, 1)
        self.layout_grid.addWidget(self.marka, 3, 0)
        self.layout_grid.addWidget(self.uid, 4, 0)
        self.layout_grid.addWidget(self.uid_line, 4, 1)
        self.layout_grid.addWidget(self.line_pasport, 5, 1)
        self.layout_grid.addWidget(self.pasport, 5, 0)
        self.layout_grid.addWidget(self.vin_line, 6, 1)
        self.layout_grid.addWidget(self.vin, 6, 0)
        self.layout_grid.addWidget(self.color_line, 7, 1)
        self.layout_grid.addWidget(self.color, 7, 0)
        self.layout_grid.addWidget(self.docs_reg_line, 8, 1)
        self.layout_grid.addWidget(self.docs_reg, 8, 0)
        self.layout_grid.addWidget(self.cate, 9, 0)
        self.layout_grid.addWidget(self.cate_line, 9, 1)
        self.layout_grid.addWidget(self.btn_add2, 10, 1)
        self.layout_grid.addWidget(self.btn_otmena, 10, 0)
        self.btn_otmena.clicked.connect(self.back)
        self.btn_add2.clicked.connect(self.add_data)
        self.tab_conteiner.tabBarClicked.connect(self.handle_tabbar_clicked)

    def tableCar(self):
        self.raw_model = QSqlTableModel()
        self.sqlquery = QSqlQuery()
        self.query = """SELECT * FROM Seller"""
        self.sqlquery.exec_(self.query)
        self.raw_model.setQuery(self.sqlquery)
        self.current_tab = "Seller"
        self.model = QSortFilterProxyModel()
        self.model.setSourceModel(self.raw_model)
        return self.model

    def tableOwner(self):
        self.raw_model = QSqlTableModel()
        self.sqlquery = QSqlQuery()
        self.query = """SELECT * FROM Client"""
        self.sqlquery.exec_(self.query)
        self.raw_model.setQuery(self.sqlquery)
        self.current_tab = "Client"
        self.model = QSortFilterProxyModel()
        self.model.setSourceModel(self.raw_model)
        return self.model

    def tableDocs(self):
        self.raw_model = QSqlTableModel()
        self.sqlquery = QSqlQuery()
        self.query = """SELECT * FROM Board"""
        self.sqlquery.exec_(self.query)
        self.raw_model.setQuery(self.sqlquery)
        self.current_tab = "Board"
        self.tab_id = "Код продавца"
        self.model = QSortFilterProxyModel()
        self.model.setSourceModel(self.raw_model)
        return self.model

    def add(self):
        self.frame1.setVisible(False)
        self.frame2.setVisible(True)

    def back(self):
        self.frame1.setVisible(True)
        self.frame2.setVisible(False)

    def update(self):
        self.table_view.setModel(self.tableCar())
        self.table_view2.setModel(self.tableOwner())
        self.table_view3.setModel(self.tableDocs())


    def add_data(self):
        self.sqlquery = QSqlQuery()
        self.query = "INSERT INTO Seller VALUES('{}', '{}', '{}', '{}')".format(self.uid_line.text(), self.vin_line.text(), self.marka_line.text(), self.color_line.text())
        self.sqlquery.exec_(self.query)
        self.query = "INSERT INTO Client VALUES('{}', '{}', '{}', '{}')".format(self.doc_num_line.text(), self.line_name.text(), self.dateb_line.text(), self.line_pasport.text())
        self.sqlquery.exec_(self.query)
        self.query = "INSERT INTO Board VALUES('{}', '{}', '{}', '{}')".format(self.doc_num_line.text(), self.uid_line.text(), self.docs_reg_line.text(), self.cate_line.text())
        self.sqlquery.exec_(self.query)
        self.update()
        self.frame1.setVisible(True)
        self.frame2.setVisible(False)

    def cell_click(self):
        if self.current_tab == "Seller":
            return self.table_view.model().data(self.table_view.currentIndex())
        if self.current_tab == "Client":
            return self.table_view3.model().data(self.table_view3.currentIndex())
        if self.current_tab == "Board":
            return self.table_view2.model().data(self.table_view2.currentIndex())

    def delete(self):
        self.sqlquery = QSqlQuery()
        self.query = f"""DELETE FROM {self.current_tab} WHERE ("{self.tab_id}" = "{self.cell_click()}")"""
        print(self.query)
        self.sqlquery.exec_(self.query)
        self.update()

    def handle_tabbar_clicked(self, index):
        if(index==0):
            self.current_tab = "Seller"
            self.tab_id = "Код продавца"
        elif(index==1):
            self.current_tab = "Client"
            self.tab_id = "Уникальный номер"
        else:
            self.tab_id = "Уникальный номер"
            self.current_tab = "Board"

class MainWindow(QWidget):
    def __init__(self) -> None:
        QWidget.__init__(self)
        self.my_datebase = DateBase("datebase.db")
        if not self.my_datebase:
            sys.exit(-1)
        self.main_view = TableView(self)


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
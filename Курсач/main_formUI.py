# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1608, 865)
        MainWindow.setMaximumSize(QtCore.QSize(1631, 865))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tables_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.tables_comboBox.setGeometry(QtCore.QRect(1400, 40, 191, 32))
        self.tables_comboBox.setObjectName("tables_comboBox")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1400, 10, 121, 18))
        self.label.setObjectName("label")
        self.queries_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.queries_comboBox.setGeometry(QtCore.QRect(1400, 110, 191, 32))
        self.queries_comboBox.setObjectName("queries_comboBox")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1400, 80, 121, 18))
        self.label_2.setObjectName("label_2")
        self.visualizeTable_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.visualizeTable_pushButton.setGeometry(QtCore.QRect(1400, 740, 201, 34))
        self.visualizeTable_pushButton.setObjectName("visualizeTable_pushButton")
        self.visualizeQuery_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.visualizeQuery_pushButton.setGeometry(QtCore.QRect(1400, 780, 201, 34))
        self.visualizeQuery_pushButton.setObjectName("visualizeQuery_pushButton")
        self.addRecord_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.addRecord_pushButton.setGeometry(QtCore.QRect(1400, 190, 191, 34))
        self.addRecord_pushButton.setObjectName("addRecord_pushButton")
        self.deleteRecord_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteRecord_pushButton.setGeometry(QtCore.QRect(1400, 270, 191, 34))
        self.deleteRecord_pushButton.setObjectName("deleteRecord_pushButton")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 10, 1381, 801))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setMinimumSize(QtCore.QSize(1200, 600))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.addRow_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.addRow_pushButton.setGeometry(QtCore.QRect(1400, 150, 191, 34))
        self.addRow_pushButton.setObjectName("addRow_pushButton")
        self.saveToExcel_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveToExcel_pushButton.setGeometry(QtCore.QRect(1400, 700, 201, 31))
        self.saveToExcel_pushButton.setObjectName("saveToExcel_pushButton")
        self.buildSummaryChart_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.buildSummaryChart_pushButton.setGeometry(QtCore.QRect(1400, 660, 201, 31))
        self.buildSummaryChart_pushButton.setObjectName("buildSummaryChart_pushButton")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(1390, 320, 211, 241))
        self.groupBox.setObjectName("groupBox")
        self.columnCriteria_textEdit = QtWidgets.QTextEdit(self.groupBox)
        self.columnCriteria_textEdit.setGeometry(QtCore.QRect(10, 150, 181, 31))
        self.columnCriteria_textEdit.setObjectName("columnCriteria_textEdit")
        self.columns_comboBox = QtWidgets.QComboBox(self.groupBox)
        self.columns_comboBox.setGeometry(QtCore.QRect(10, 40, 181, 22))
        self.columns_comboBox.setObjectName("columns_comboBox")
        self.findByCriteria_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.findByCriteria_pushButton.setGeometry(QtCore.QRect(10, 190, 181, 34))
        self.findByCriteria_pushButton.setObjectName("findByCriteria_pushButton")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 20, 191, 16))
        self.label_3.setObjectName("label_3")
        self.enableSorting_checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.enableSorting_checkBox.setGeometry(QtCore.QRect(10, 70, 171, 17))
        self.enableSorting_checkBox.setObjectName("enableSorting_checkBox")
        self.sortByAscending_radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.sortByAscending_radioButton.setEnabled(False)
        self.sortByAscending_radioButton.setGeometry(QtCore.QRect(10, 100, 191, 17))
        self.sortByAscending_radioButton.setChecked(True)
        self.sortByAscending_radioButton.setObjectName("sortByAscending_radioButton")
        self.sortByDescending_radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.sortByDescending_radioButton.setEnabled(False)
        self.sortByDescending_radioButton.setGeometry(QtCore.QRect(10, 120, 191, 17))
        self.sortByDescending_radioButton.setObjectName("sortByDescending_radioButton")
        self.updateRecord_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.updateRecord_pushButton.setGeometry(QtCore.QRect(1400, 230, 191, 34))
        self.updateRecord_pushButton.setObjectName("updateRecord_pushButton")
        self.editChildTable_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.editChildTable_pushButton.setGeometry(QtCore.QRect(1400, 590, 201, 31))
        self.editChildTable_pushButton.setObjectName("editChildTable_pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1608, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Выберите таблицу:"))
        self.label_2.setText(_translate("MainWindow", "Выберите запрос:"))
        self.visualizeTable_pushButton.setText(_translate("MainWindow", "Визуализировать таблицу"))
        self.visualizeQuery_pushButton.setText(_translate("MainWindow", "Визуализировать запрос"))
        self.addRecord_pushButton.setText(_translate("MainWindow", "Добавить запись"))
        self.deleteRecord_pushButton.setText(_translate("MainWindow", "Удалить запись"))
        self.addRow_pushButton.setText(_translate("MainWindow", "Добавить строку в таблицу"))
        self.saveToExcel_pushButton.setText(_translate("MainWindow", "Сохранить в Excel"))
        self.buildSummaryChart_pushButton.setText(_translate("MainWindow", "Построить итоговую диаграмму"))
        self.groupBox.setTitle(_translate("MainWindow", "Сортировка и фильтрация"))
        self.findByCriteria_pushButton.setText(_translate("MainWindow", "Поиск по критерию"))
        self.label_3.setText(_translate("MainWindow", "Выберите поле: "))
        self.enableSorting_checkBox.setText(_translate("MainWindow", "Сортировка"))
        self.sortByAscending_radioButton.setText(_translate("MainWindow", "Отсортировать по возрастанию"))
        self.sortByDescending_radioButton.setText(_translate("MainWindow", "Отсортировать по убыванию"))
        self.updateRecord_pushButton.setText(_translate("MainWindow", "Изменить запись"))
        self.editChildTable_pushButton.setText(_translate("MainWindow", "Редактировать дочернюю таблицу"))

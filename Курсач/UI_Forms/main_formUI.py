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
        MainWindow.resize(1407, 660)
        MainWindow.setMaximumSize(QtCore.QSize(1631, 865))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 1406, 655))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.main_verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.main_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.main_verticalLayout.setObjectName("main_verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setMinimumSize(QtCore.QSize(400, 400))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.visualizeQuery_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.visualizeQuery_pushButton.setObjectName("visualizeQuery_pushButton")
        self.verticalLayout_4.addWidget(self.visualizeQuery_pushButton)
        self.saveToExcel_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.saveToExcel_pushButton.setObjectName("saveToExcel_pushButton")
        self.verticalLayout_4.addWidget(self.saveToExcel_pushButton)
        self.visualizeTable_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.visualizeTable_pushButton.setObjectName("visualizeTable_pushButton")
        self.verticalLayout_4.addWidget(self.visualizeTable_pushButton)
        self.updateRecord_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.updateRecord_pushButton.setObjectName("updateRecord_pushButton")
        self.verticalLayout_4.addWidget(self.updateRecord_pushButton)
        self.addRecord_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.addRecord_pushButton.setObjectName("addRecord_pushButton")
        self.verticalLayout_4.addWidget(self.addRecord_pushButton)
        self.deleteRecord_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.deleteRecord_pushButton.setObjectName("deleteRecord_pushButton")
        self.verticalLayout_4.addWidget(self.deleteRecord_pushButton)
        self.addRow_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.addRow_pushButton.setObjectName("addRow_pushButton")
        self.verticalLayout_4.addWidget(self.addRow_pushButton)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.queries_comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_2)
        self.queries_comboBox.setObjectName("queries_comboBox")
        self.verticalLayout_4.addWidget(self.queries_comboBox)
        self.params_textEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget_2)
        self.params_textEdit.setMinimumSize(QtCore.QSize(400, 30))
        self.params_textEdit.setMaximumSize(QtCore.QSize(400, 30))
        self.params_textEdit.setObjectName("params_textEdit")
        self.verticalLayout_4.addWidget(self.params_textEdit)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label.setSizeIncrement(QtCore.QSize(0, 25))
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.tables_comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_2)
        self.tables_comboBox.setObjectName("tables_comboBox")
        self.verticalLayout_4.addWidget(self.tables_comboBox)
        self.groupBox = QtWidgets.QGroupBox(self.verticalLayoutWidget_2)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 125))
        self.groupBox.setObjectName("groupBox")
        self.columnCriteria_textEdit = QtWidgets.QTextEdit(self.groupBox)
        self.columnCriteria_textEdit.setGeometry(QtCore.QRect(210, 50, 181, 31))
        self.columnCriteria_textEdit.setObjectName("columnCriteria_textEdit")
        self.columns_comboBox = QtWidgets.QComboBox(self.groupBox)
        self.columns_comboBox.setGeometry(QtCore.QRect(10, 40, 181, 22))
        self.columns_comboBox.setObjectName("columns_comboBox")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 20, 191, 16))
        self.label_3.setObjectName("label_3")
        self.enableSorting_checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.enableSorting_checkBox.setGeometry(QtCore.QRect(10, 70, 171, 17))
        self.enableSorting_checkBox.setObjectName("enableSorting_checkBox")
        self.sortByAscending_radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.sortByAscending_radioButton.setEnabled(False)
        self.sortByAscending_radioButton.setGeometry(QtCore.QRect(210, 10, 191, 17))
        self.sortByAscending_radioButton.setChecked(True)
        self.sortByAscending_radioButton.setObjectName("sortByAscending_radioButton")
        self.sortByDescending_radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.sortByDescending_radioButton.setEnabled(False)
        self.sortByDescending_radioButton.setGeometry(QtCore.QRect(210, 30, 191, 17))
        self.sortByDescending_radioButton.setObjectName("sortByDescending_radioButton")
        self.findByCriteria_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.findByCriteria_pushButton.setGeometry(QtCore.QRect(110, 90, 181, 34))
        self.findByCriteria_pushButton.setObjectName("findByCriteria_pushButton")
        self.verticalLayout_4.addWidget(self.groupBox)
        self.buildSummaryChart_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.buildSummaryChart_pushButton.setObjectName("buildSummaryChart_pushButton")
        self.verticalLayout_4.addWidget(self.buildSummaryChart_pushButton)
        self.editChildTable_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.editChildTable_pushButton.setObjectName("editChildTable_pushButton")
        self.verticalLayout_4.addWidget(self.editChildTable_pushButton)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.main_verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1407, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Главное окно"))
        self.visualizeQuery_pushButton.setText(_translate("MainWindow", "Отобразить запрос"))
        self.saveToExcel_pushButton.setText(_translate("MainWindow", "Сохранить в Excel"))
        self.visualizeTable_pushButton.setText(_translate("MainWindow", "Отобразить таблицу"))
        self.updateRecord_pushButton.setText(_translate("MainWindow", "Изменить запись"))
        self.addRecord_pushButton.setText(_translate("MainWindow", "Добавить запись"))
        self.deleteRecord_pushButton.setText(_translate("MainWindow", "Удалить запись"))
        self.addRow_pushButton.setText(_translate("MainWindow", "Добавить строку в таблицу"))
        self.label_2.setText(_translate("MainWindow", "Выберите запрос:"))
        self.label.setText(_translate("MainWindow", "Выберите таблицу:"))
        self.groupBox.setTitle(_translate("MainWindow", "Сортировка и фильтрация"))
        self.label_3.setText(_translate("MainWindow", "Выберите поле: "))
        self.enableSorting_checkBox.setText(_translate("MainWindow", "Сортировка"))
        self.sortByAscending_radioButton.setText(_translate("MainWindow", "Отсортировать по возрастанию"))
        self.sortByDescending_radioButton.setText(_translate("MainWindow", "Отсортировать по убыванию"))
        self.findByCriteria_pushButton.setText(_translate("MainWindow", "Поиск по критерию"))
        self.buildSummaryChart_pushButton.setText(_translate("MainWindow", "Построить итоговую диаграмму"))
        self.editChildTable_pushButton.setText(_translate("MainWindow", "Открыть составную форму"))

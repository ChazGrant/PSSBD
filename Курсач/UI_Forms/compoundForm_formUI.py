# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'compound_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(812, 495)
        self.mainTable_tableWidget = QtWidgets.QTableWidget(Form)
        self.mainTable_tableWidget.setGeometry(QtCore.QRect(10, 10, 791, 192))
        self.mainTable_tableWidget.setObjectName("mainTable_tableWidget")
        self.mainTable_tableWidget.setColumnCount(0)
        self.mainTable_tableWidget.setRowCount(0)
        self.childTables_comboBox = QtWidgets.QComboBox(Form)
        self.childTables_comboBox.setGeometry(QtCore.QRect(10, 220, 161, 22))
        self.childTables_comboBox.setObjectName("childTables_comboBox")
        self.childTable_tableWidget = QtWidgets.QTableWidget(Form)
        self.childTable_tableWidget.setGeometry(QtCore.QRect(230, 210, 571, 271))
        self.childTable_tableWidget.setObjectName("childTable_tableWidget")
        self.childTable_tableWidget.setColumnCount(0)
        self.childTable_tableWidget.setRowCount(0)
        self.addRecord_pushButton = QtWidgets.QPushButton(Form)
        self.addRecord_pushButton.setGeometry(QtCore.QRect(10, 330, 211, 34))
        self.addRecord_pushButton.setObjectName("addRecord_pushButton")
        self.updateRecord_pushButton = QtWidgets.QPushButton(Form)
        self.updateRecord_pushButton.setGeometry(QtCore.QRect(10, 370, 211, 34))
        self.updateRecord_pushButton.setObjectName("updateRecord_pushButton")
        self.addRowToMainTable_pushButton = QtWidgets.QPushButton(Form)
        self.addRowToMainTable_pushButton.setGeometry(QtCore.QRect(10, 250, 211, 34))
        self.addRowToMainTable_pushButton.setObjectName("addRowToMainTable_pushButton")
        self.deleteRecord_pushButton = QtWidgets.QPushButton(Form)
        self.deleteRecord_pushButton.setGeometry(QtCore.QRect(10, 410, 211, 34))
        self.deleteRecord_pushButton.setObjectName("deleteRecord_pushButton")
        self.addRowToChildTable_pushButton = QtWidgets.QPushButton(Form)
        self.addRowToChildTable_pushButton.setGeometry(QtCore.QRect(10, 290, 211, 34))
        self.addRowToChildTable_pushButton.setObjectName("addRowToChildTable_pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Составная форма"))
        self.addRecord_pushButton.setText(_translate("Form", "Добавить запись"))
        self.updateRecord_pushButton.setText(_translate("Form", "Изменить запись"))
        self.addRowToMainTable_pushButton.setText(_translate("Form", "Добавить строку в главную таблицу"))
        self.deleteRecord_pushButton.setText(_translate("Form", "Удалить запись"))
        self.addRowToChildTable_pushButton.setText(_translate("Form", "Добавить строку в дочернюю таблицу"))

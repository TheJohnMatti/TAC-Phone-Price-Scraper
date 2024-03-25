# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'table_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import webbrowser


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(10, 100, 1480, 680))
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setSortingEnabled(True)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.tableWidget.setColumnWidth(0, 114)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.setColumnWidth(1, 514)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.tableWidget.setColumnWidth(2, 114)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.setColumnWidth(3, 114)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.tableWidget.setColumnWidth(4, 114)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        self.tableWidget.setColumnWidth(5, 214)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        self.tableWidget.setColumnWidth(6, 114)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        self.tableWidget.setColumnWidth(7, 114)
        self.linkQueue = True
        self.counter = QtCore.QTimer(Form)
        self.counter.setInterval(500)
        self.counter.timeout.connect(self.reset_timer)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Website"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Title"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Min. Price"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Rating"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Used"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Condition"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Form", "Seller"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("Form", "Link"))

    def update_table(self, products):
        self.products = products
        self.tableWidget.setRowCount(len(products))
        for index, value in enumerate(products):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(index, item)
            item.setText(str(index))
            table_item = QtWidgets.QTableWidgetItem()
            table_item.setText(value.website)
            table_item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.tableWidget.setItem(index, 0, table_item)
            table_item = QtWidgets.QTableWidgetItem()
            table_item.setText(value.name)
            table_item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.tableWidget.setItem(index, 1, table_item)
            table_item = QtWidgets.QTableWidgetItem()
            table_item.setData(QtCore.Qt.DisplayRole, value.prices[0] if value.prices != [] else value.price)
            table_item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.tableWidget.setItem(index, 2, table_item)
            table_item = QtWidgets.QTableWidgetItem()
            table_item.setData(QtCore.Qt.DisplayRole, value.rating)
            table_item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.tableWidget.setItem(index, 3, table_item)
            table_item = QtWidgets.QTableWidgetItem()
            table_item.setText("Yes" if value.used else "No")
            table_item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.tableWidget.setItem(index, 4, table_item)
            table_item = QtWidgets.QTableWidgetItem()
            table_item.setText(value.cond)
            table_item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.tableWidget.setItem(index, 5, table_item)
            table_item = QtWidgets.QTableWidgetItem()
            table_item.setText(value.seller)
            table_item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.tableWidget.setItem(index, 6, table_item)
            table_item = QtWidgets.QTableWidgetItem()
            table_item.setText(value.link)
            table_item.setForeground(QtGui.QColor("blue"))
            table_item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.tableWidget.itemClicked.connect(self.open_link)
            self.tableWidget.setItem(index, 7, table_item)


    def delete_table(self):
        self.tableWidget.setRowCount(0)

    def open_link(self, item : QtWidgets.QTableWidgetItem):
        if item.column() == 7 and item.text() != "" and self.linkQueue == True:
            self.linkQueue = False
            self.counter.start()
            webbrowser.open(item.text())

    def toggle_sorting(self, toggle: bool):
        self.tableWidget.setSortingEnabled(toggle)

    def reset_timer(self):
        self.counter.stop()
        self.linkQueue = True

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

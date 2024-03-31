from PyQt5 import QtCore, QtGui, QtWidgets
import webbrowser

#  Custom table widget for displaying data

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(10, 100, 1480, 680))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setSortingEnabled(False)   # Disable table sorting without data to prevent corruption bug
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(7, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.itemClicked.connect(self.open_link)  # Opening website and product links

        self.linkQueue = True  # Link wait time of 0.5 s used to prevent bug where website opens dozens of times
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
        item.setText(_translate("Form", "Min. Price (CAD)"))
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

    # Called at the end of successful scrape threads to update all cells in the table
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
            table_item.setForeground(QtGui.QColor("blue"))
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
            table_item.setText(value.cond if value.used else "New")
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
            self.tableWidget.setItem(index, 7, table_item)

    # Getter used for outside access to the table widget
    def get_table(self):
        return self.tableWidget

    # Remove all non-label components
    def delete_table(self):
        self.tableWidget.setRowCount(0)

    # Only allow for websites and products
    def open_link(self, item : QtWidgets.QTableWidgetItem):
        if (item.column() == 7 or item.column() == 0) and item.text() != "" and self.linkQueue == True:
            self.linkQueue = False
            self.counter.start()
            webbrowser.open(item.text())

    # Used for outside access to "setSortingEnabled(bool)" method
    def toggle_sorting(self, toggle: bool):
        self.tableWidget.setSortingEnabled(toggle)

    # re-toggling link clicks
    def reset_timer(self):
        self.counter.stop()
        self.linkQueue = True

# Not used
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

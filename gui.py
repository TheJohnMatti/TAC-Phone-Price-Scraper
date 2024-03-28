from PyQt5 import QtCore, QtGui, QtWidgets
from playwright.sync_api import sync_playwright
import os
import table_widget
import tac_mapper
import process
import amazon_scraper
import ebay_scraper
import walmart_scraper
import bestbuy_scraper
import pyqtspinner


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(270, 10, 81, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.pressed.connect(self.start_scrape_thread)
        self.textInput = QtWidgets.QLineEdit(MainWindow)
        self.textInput.setGeometry(QtCore.QRect(10, 10, 260, 50))
        self.textInput.setPlaceholderText("Enter TAC code...")
        self.textInput.setValidator(QtGui.QIntValidator(0, 99999999))
        self.brandLabel = QtWidgets.QLabel(self.centralwidget)
        self.brandLabel.setText("Brand: ")
        self.nameLabel = QtWidgets.QLabel(self.centralwidget)
        self.nameLabel.setText("Name: ")
        self.modelLabel = QtWidgets.QLabel(self.centralwidget)
        self.modelLabel.setText("Model: ")
        self.table = table_widget.Ui_Form()
        self.table.setupUi(self.centralwidget)
        self.table.toggle_sorting(False)
        self.tableLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        x = QtWidgets.QHBoxLayout(self.centralwidget)
        x.addWidget(self.textInput)
        x.addWidget(self.pushButton)
        self.tableLayout.addLayout(x)
        self.tableLayout.addWidget(self.brandLabel)
        self.tableLayout.addWidget(self.nameLabel)
        self.tableLayout.addWidget(self.modelLabel)
        self.tableLayout.addWidget(self.table.get_table())
        self.products = []
        self.spinner = pyqtspinner.WaitingSpinner(MainWindow)
        self.loadingLabel = QtWidgets.QLabel(self.centralwidget)
        self.loadingLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.loadingLabel.setGeometry(0, 0, MainWindow.width(), 25)
        self.loadingLabel.setVisible(False)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.start_playwright_install_thread()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tac Phone Price Scraper"))
        self.pushButton.setText(_translate("MainWindow", "Enter"))
        self.pushButton.setShortcut(_translate("MainWindow", "Return"))

    def start_scrape_thread(self):
        self.spinner.start()
        self.pushButton.setEnabled(False)
        self.tableLayout.addWidget(self.loadingLabel)
        self.loadingLabel.setVisible(True)
        self.brandLabel.setText("Brand: ")
        self.nameLabel.setText("Name: ")
        self.modelLabel.setText("Model: ")
        self.table.delete_table()
        self.table.toggle_sorting(False)
        self.products = []
        self.scrapeThread = QtCore.QThread()
        self.worker = ScraperWorker(self.textInput.text())
        self.worker.moveToThread(self.scrapeThread)
        self.scrapeThread.started.connect(self.worker.run)
        self.worker.finished.connect(self.scrapeThread.quit)
        self.worker.finished.connect(self.end_scrape_thread)
        self.worker.processChanged.connect(self.loadingLabel.setText)
        self.scrapeThread.start()

    def end_scrape_thread(self):
        self.spinner.stop()
        self.pushButton.setEnabled(True)
        self.tableLayout.removeWidget(self.loadingLabel)
        self.loadingLabel.setVisible(False)
        error = self.worker.error
        if error == 0:
            self.brandLabel.setText("Brand: " + self.worker.brand)
            self.nameLabel.setText("Name: " + self.worker.name)
            self.modelLabel.setText("Model: " + self.worker.model)
            self.table.update_table(self.worker.products)
            self.table.toggle_sorting(True)
        elif error == 1:
            dlg = CustomDialog("The TAC entered must be 8 digits long!")
            dlg.exec_()
        elif error == 2:
            dlg = CustomDialog("The TAC entered does not correspond to a known phone model!")
            dlg.exec_()

    def start_playwright_install_thread(self):
        self.spinner.start()
        self.pushButton.setEnabled(False)
        self.tableLayout.addWidget(self.loadingLabel)
        self.loadingLabel.setVisible(True)
        self.loadingLabel.setText("Setting up Playwright...")
        self.playwrightInstallThread = QtCore.QThread()
        self.playwrightInstallWorker = PlaywrightInstallWorker()
        self.playwrightInstallWorker.moveToThread(self.playwrightInstallThread)
        self.playwrightInstallThread.started.connect(self.playwrightInstallWorker.run)
        self.playwrightInstallWorker.finished.connect(self.end_playwright_install_thread)
        self.playwrightInstallThread.start()

    def end_playwright_install_thread(self):
        self.playwrightInstallThread.quit()
        self.spinner.stop()
        self.pushButton.setEnabled(True)
        self.loadingLabel.clear()
        self.tableLayout.removeWidget(self.loadingLabel)

class CustomDialog(QtWidgets.QDialog):
    def __init__(self, str):
        super().__init__()

        self.setWindowTitle("Warning")

        QBtn = QtWidgets.QDialogButtonBox.Ok

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel(str)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class ScraperWorker(QtCore.QObject):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.products = []
        self.brand = ""
        self.task = ""
        self.name = ""
        self.model = ""
        self.error = 0

    processChanged = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal()

    def run(self):
        self.processChanged.emit("Processing TAC...")
        self.initialize_playwright()
        self.process_tac_code_helper()
        self.close_playwright()
        self.processChanged.emit("")
        self.finished.emit()

    def initialize_playwright(self):
        self.pw = sync_playwright().start()
        self.browser = self.pw.firefox.launch()
        self.page = self.browser.new_page()

    def close_playwright(self):
        self.page.close()
        self.browser.close()
        self.pw.stop()

    def process_tac_code_helper(self):
        # set loading text
        if len(self.text) != 8:
            self.error = 1
            return
        res = tac_mapper.process_tac_code(self.text)
        match res:
            case "-2":
                self.error = 2
            case _:
                self.scraper_helper(res, self.page)

    def scraper_helper(self, doc, page):
        self.brand = doc['object']['brand']
        self.name = doc['object']['name']
        self.model = doc['object']['model']
        query = self.produce_search_query(doc)
        self.processChanged.emit("Scraping Amazon...")
        self.products += amazon_scraper.run(query, page)
        self.processChanged.emit("Scraping eBay...")
        self.products += ebay_scraper.run(query, page)
        self.processChanged.emit("Scraping Walmart...")
        self.products += walmart_scraper.run(query, page)
        self.processChanged.emit("Scraping Best Buy...")
        self.products += bestbuy_scraper.run(query, page)
        self.products = process.process_data(self.products, self.query_words)
        return

    def produce_search_query(self, doc):
        query = ""
        name: str = doc['object']['name']
        self.query_words: list = name.split()
        for i in self.query_words:
            query += i + "+"
        return query[:-1]


class PlaywrightInstallWorker(QtCore.QObject):

    def __init__(self):
        super().__init__()

    finished = QtCore.pyqtSignal()

    def run(self):
        os.system("py -m playwright install")
        self.finished.emit()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

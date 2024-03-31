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
import canadacomputers_scraper
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
        self.pushButton.pressed.connect(self.start_scrape_thread)  # Configure button
        self.textInput = QtWidgets.QLineEdit(MainWindow)  # TAC input
        self.textInput.setGeometry(QtCore.QRect(10, 10, 260, 50))
        self.textInput.setPlaceholderText("Enter TAC code...")
        self.textInput.setValidator(QtGui.QIntValidator(0, 99999999))  # Limit inputs to only ints and 8 digits max
        self.brandLabel = QtWidgets.QLabel(self.centralwidget)  # Product information labels
        self.brandLabel.setText("Brand: ")
        self.nameLabel = QtWidgets.QLabel(self.centralwidget)
        self.nameLabel.setText("Name: ")
        self.modelLabel = QtWidgets.QLabel(self.centralwidget)
        self.modelLabel.setText("Model: ")
        self.table = table_widget.Ui_Form()  # Instantiate custom table widget
        self.table.setupUi(self.centralwidget)
        self.table.toggle_sorting(False)
        self.tableLayout = QtWidgets.QVBoxLayout(self.centralwidget) # Create main page layout
        x = QtWidgets.QHBoxLayout(self.centralwidget)
        x.addWidget(self.textInput)
        x.addWidget(self.pushButton)
        self.tableLayout.addLayout(x)  # Horizontally align text input and push button
        self.tableLayout.addWidget(self.brandLabel)  # Add 3 vertical labels to layout
        self.tableLayout.addWidget(self.nameLabel)
        self.tableLayout.addWidget(self.modelLabel)
        self.tableLayout.addWidget(self.table.get_table())  # Add table widget to layout
        self.spinner = pyqtspinner.WaitingSpinner(MainWindow)  # Loading spinner used during threads
        self.loadingLabel = QtWidgets.QLabel(self.centralwidget)  # Label at bottom used to track threads
        self.loadingLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.loadingLabel.setGeometry(0, 0, MainWindow.width(), 25)
        self.loadingLabel.setVisible(False)
        self.products = []  # Array of products scraped

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
        self.start_playwright_install_thread()  # On launch, always run 'python3 -m playwright install' for browsers

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TAC Phone Price Scraper"))
        self.pushButton.setText(_translate("MainWindow", "Enter"))
        self.pushButton.setShortcut(_translate("MainWindow", "Return"))

    # Adjust UI and prepare scrape thread
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

    # Called at the end of scrape thread
    def end_scrape_thread(self):
        self.spinner.stop()
        self.pushButton.setEnabled(True)
        self.tableLayout.removeWidget(self.loadingLabel)
        self.loadingLabel.setVisible(False)
        error = self.worker.error
        match error:
            case 0:  # Only if scrape was successful
                self.brandLabel.setText("Brand: " + self.worker.brand)
                self.nameLabel.setText("Name: " + self.worker.name)
                self.modelLabel.setText("Model: " + self.worker.model)
                self.table.update_table(self.worker.products)
                self.table.toggle_sorting(True)
            # Create error messages for 3 cases
            case 1:
                dlg = CustomDialog("The TAC entered must be 8 digits long!")
                dlg.exec_()
            case 2:
                dlg = CustomDialog("The TAC entered does not correspond to a known phone model!")
                dlg.exec_()
            case 3:
                dlg = CustomDialog("No results are available for the TAC entered")
                dlg.exec_()

    # Disable GUI while installing playwright browsers
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

# Custom dialog used for handling input or scraping errors
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

# Long-running scrape thread
class ScraperWorker(QtCore.QObject):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.products = []
        self.brand = ""
        self.task = ""
        self.name = ""
        self.model = ""
        self.error = 0  # 0 = Good, 1 = TAC length error, 2 = TAC not found in database, 3 = No valid results scraped

    processChanged = QtCore.pyqtSignal(str)  # Signal to update loading label
    finished = QtCore.pyqtSignal()  # Signal to end thread

    # Main thread function
    def run(self):
        self.processChanged.emit("Processing TAC...")
        self.initialize_playwright()
        self.process_tac_code_helper()
        self.close_playwright()
        self.processChanged.emit("")  # Clear loading label
        self.finished.emit()  # End scraping thread

    # Start a playwright firefox instance
    def initialize_playwright(self):
        self.pw = sync_playwright().start()
        self.browser = self.pw.firefox.launch()
        self.page = self.browser.new_page()

    # Close playwright instance
    def close_playwright(self):
        self.page.close()
        self.browser.close()
        self.pw.stop()

    # Send the code to tac_mapper to connect to the IMEI checker API
    def process_tac_code_helper(self):
        # Do not accept lengths other than 8
        if len(self.text) != 8:
            self.error = 1  # TAC length error
            return
        res = tac_mapper.process_tac_code(self.text)
        match res:
            case "-2":
                self.error = 2  # TAC validity error
                return
            case _:
                self.scraper_helper(res, self.page)  # Proceed with scraping
                return

    # Helper function connecting all individual scrapers
    def scraper_helper(self, doc, page):
        # Update device info labels
        self.brand = doc['object']['brand']
        self.name = doc['object']['name']
        self.model = doc['object']['model']
        # Get search query
        query = self.produce_search_query(doc)
        # Scrape websites and update loading label
        self.processChanged.emit("Scraping Amazon...")
        self.products += amazon_scraper.run(query, page)
        self.processChanged.emit("Scraping eBay...")
        self.products += ebay_scraper.run(query, page)
        self.processChanged.emit("Scraping Walmart...")
        self.products += walmart_scraper.run(query, page)
        self.processChanged.emit("Scraping Best Buy...")
        self.products += bestbuy_scraper.run(query, page)
        self.processChanged.emit("Scraping Canada Computers...")
        self.products += canadacomputers_scraper.run(query, page)
        # Process data
        self.products = process.process_data(self.products, self.query_words)
        if len(self.products) == 0:
            self.error = 3  # No products found error
            return
        # Unnecessary but being extra sure that the error is set to 0 so that the data is displayed
        self.error = 0
        return

    # Produce query by adding +'s between each word of the device name
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

    # Run to install browsers if not present. Takes long so it is asynchronous to prevent frozen GUI
    def run(self):
        os.system(".\\Scripts\\playwright.exe install")
        self.finished.emit()

# Main script that initializes GUI
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

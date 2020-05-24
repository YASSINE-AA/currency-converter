from PySide2.QtWidgets import QMainWindow, QLabel, QPushButton, QLineEdit, QComboBox, QMenuBar
from PySide2.QtGui import QFont, QDoubleValidator
from bs4 import BeautifulSoup
import requests
# Author Yassine Ahmed Ali


class ExchangeRates(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window_init()

    def window_init(self):
        self.setWindowTitle("Check Exchange Rates")
        self.resize(300, 145)
        self.setFixedSize(self.size())
        self.ui_components()

    def ui_components(self):
        font = QFont("Roboto", 16)
        title_label = QLabel("Current exchange rates are:", self)
        title_label.setFont(font)
        title_label.move(10, 2)
        title_label.setStyleSheet("color: blue")
        title_label.adjustSize()

        rate_usd_tnd = Exchanges().usd_tnd()
        rate_usd_eur = Exchanges().usd_eur()
        rate_tnd_eur = Exchanges().tnd_eur()
        usd_tnd_label = QLabel(f"1 USD is {rate_usd_tnd} TND.", self)
        usd_tnd_label.setFont(font)
        usd_tnd_label.move(10, 40)
        usd_tnd_label.adjustSize()
        usd_eur_label = QLabel(f"1 USD is {rate_usd_eur} EUR.", self)
        usd_eur_label.setFont(font)
        usd_eur_label.move(10, 67)
        usd_eur_label.adjustSize()
        tnd_eur_label = QLabel(f"1 TND is {rate_tnd_eur} EUR.", self)
        tnd_eur_label.setFont(font)
        tnd_eur_label.move(10, 93)
        tnd_eur_label.adjustSize()


class Exchanges():

    # Gets exchange rate for usd and tnd
    def usd_tnd(self):
        result_usd_tnd = requests.get(
            "https://transferwise.com/gb/currency-converter/usd-to-tnd-rate")
        src_usd_tnd = result_usd_tnd.content
        soup_usd_tnd = BeautifulSoup(
            src_usd_tnd, features="html.parser")
        rate_text = soup_usd_tnd.find_all(
            "span", class_="text-success")
        rate_usd_tnd = float(str(rate_text[0]).replace(
            '<span class="text-success">', '').replace("</span>", ""))
        return rate_usd_tnd

    # Gets exchange rate for usd and eur
    def usd_eur(self):
        result_usd_eur = requests.get(
            "https://transferwise.com/gb/currency-converter/usd-to-eur-rate")
        src_usd_eur = result_usd_eur.content
        soup_usd_eur = BeautifulSoup(
            src_usd_eur, features="html.parser")
        rate_text = soup_usd_eur.find_all(
            "span", class_="text-success")
        rate_usd_eur = float(str(rate_text[0]).replace(
            '<span class="text-success">', '').replace("</span>", ""))
        return rate_usd_eur

    # Gets exchange rate for tnd and eur
    def tnd_eur(self):
        result_tnd_eur = requests.get(
            "https://transferwise.com/gb/currency-converter/tnd-to-eur-rate")
        src_tnd_eur = result_tnd_eur.content
        soup_tnd_eur = BeautifulSoup(
            src_tnd_eur, features="html.parser")
        rate_text = soup_tnd_eur.find_all(
            "span", class_="text-success")
        rate_tnd_eur = float(str(rate_text[0]).replace(
            '<span class="text-success">', '').replace("</span>", ""))
        return rate_tnd_eur


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window_init()

    def window_init(self):
        self.setWindowTitle("Currency Convertor")
        self.resize(370, 190)
        self.setFixedSize(self.size())
        self.ui_components()
        self.show()

    def open_exchange_rates(self):
        self.exchange = ExchangeRates()

        self.exchange.show()

    def ui_components(self):

        font = QFont("Roboto", 16)
        title_label = QLabel("Convert currency:", self)
        title_label.move(7, 27)
        title_label.setFont(font)
        title_label.adjustSize()
        to_be_converted = QLineEdit(self)
        to_be_converted.setPlaceholderText("Amount")
        to_be_converted.setFont(font)
        to_be_converted.move(7, 67)
        to_be_converted.setFixedWidth(230)
        valid = QDoubleValidator()
        to_be_converted.setValidator(valid)
        converted = QLineEdit(self)
        converted.setPlaceholderText("Converted Amount")
        converted.isEnabled = False
        converted.move(7, 107)
        converted.setFixedWidth(230)
        converted.setFont(font)
        converted.setValidator(valid)
        currency_list_1 = QComboBox(self)
        currency_list_1.addItem("USD")
        currency_list_1.addItem("TND")
        currency_list_1.addItem("EUR")
        currency_list_1.move(260, 66)
        currency_list_2 = QComboBox(self)
        currency_list_2.addItem("USD")
        currency_list_2.addItem("TND")
        currency_list_2.addItem("EUR")
        currency_list_2.move(260, 100)
        convert_btn = QPushButton("Convert", self)
        convert_btn.move(260, 140)
        menubar = QMenuBar(self)
        Info = menubar.addMenu("Info")
        exchange = Info.addAction("Exchange rates")
        exchange.triggered.connect(self.open_exchange_rates)

        def convertor():

            if str(currency_list_1.currentText()) == "USD" or str(currency_list_2.currentText()) == "USD":
                # ============== USD AND TND ==================
                if str(currency_list_2.currentText()) == "TND":
                    rate_usd_tnd = Exchanges().usd_tnd()
                    converted_amount = float(
                        to_be_converted.text()) * float(rate_usd_tnd)
                    if to_be_converted != '':
                        converted.setText(str(converted_amount))

                if str(currency_list_1.currentText()) == "TND":
                    rate_usd_tnd = Exchanges().usd_tnd()
                    converted_amount = float(
                        to_be_converted.text()) * float(1 / rate_usd_tnd)
                    if to_be_converted != '':
                        converted.setText(str(converted_amount))

                # =============== EUR AND USD =================

                if str(currency_list_2.currentText()) == "EUR":
                    rate_usd_eur = Exchanges().usd_eur()
                    converted_amount = float(
                        to_be_converted.text()) * float(rate_usd_eur)
                    if to_be_converted != '':
                        converted.setText(str(converted_amount))

                if str(currency_list_1.currentText()) == "EUR":
                    rate_usd_eur = Exchanges().usd_eur()
                    converted_amount = float(
                        to_be_converted.text()) * float(1/rate_usd_eur)
                    if to_be_converted != '':
                        converted.setText(str(converted_amount))
            if (currency_list_1.currentText()) == "TND" or (currency_list_2.currentText()) == "TND":

                if str(currency_list_2.currentText()) == "EUR":
                    rate_tnd_eur = Exchanges().tnd_eur()
                    converted_amount = float(
                        to_be_converted.text()) * float(rate_tnd_eur)
                    if to_be_converted != '':
                        converted.setText(str(converted_amount))

                if str(currency_list_1.currentText()) == "EUR":
                    rate_tnd_eur = Exchanges().tnd_eur()
                    converted_amount = float(
                        to_be_converted.text()) * float(1/rate_tnd_eur)
                    if to_be_converted != '':
                        converted.setText(str(converted_amount))
        convert_btn.clicked.connect(convertor)

from PySide2.QtWidgets import QMainWindow, QLabel, QPushButton, QLineEdit, QComboBox
from PySide2.QtGui import QFont, QDoubleValidator
from bs4 import BeautifulSoup
import requests
# Author Yassine Ahmed Ali


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window_init()
        
    def window_init(self):
        self.setWindowTitle("Currency Convertor")
        self.resize(370, 180)
        self.setFixedSize(self.size())
        self.ui_components()
        self.show()
        
        
    def ui_components(self):
        font = QFont("Roboto", 16)
        title_label = QLabel("Convert currency:", self)
        title_label.move(7, 7)
        title_label.setFont(font)
        title_label.adjustSize()
        to_be_converted = QLineEdit(self)
        to_be_converted.setPlaceholderText("Amount")
        to_be_converted.setFont(font)
        to_be_converted.move(7, 47)
        to_be_converted.setFixedWidth(230)
        valid = QDoubleValidator()
        to_be_converted.setValidator(valid)
        converted = QLineEdit(self)
        converted.setPlaceholderText("Converted Amount")
        converted.isEnabled = False
        converted.move(7, 87)
        converted.setFixedWidth(230)
        converted.setFont(font)
        converted.setValidator(valid)
        currency_list_1 = QComboBox(self)
        currency_list_1.addItem("USD")
        currency_list_1.addItem("TND")
        currency_list_1.move(260, 46)
        currency_list_2 = QComboBox(self)
        currency_list_2.addItem("USD")
        currency_list_2.addItem("TND")
        currency_list_2.move(260, 80)
        convert_btn = QPushButton("Convert", self)
        convert_btn.move(260, 120)
        running = True
        
        def printing():
            # Converts USD TO TND
            # Gets Current Data
            result_usd_tnd = requests.get(
                "https://transferwise.com/gb/currency-converter/usd-to-tnd-rate")
            src_usd_tnd = result_usd_tnd.content
            soup_usd_tnd = BeautifulSoup(
                src_usd_tnd, features="html.parser")
            rate_text = soup_usd_tnd.find_all(
                "span", class_="text-success")
            rate_usd_tnd = float(str(rate_text[0]).replace(
                '<span class="text-success">', '').replace("</span>", ""))
            if str(currency_list_1.currentText()) == "USD" and str(currency_list_2.currentText()) == "TND":
                converted_amount = float(to_be_converted.text()) * float(rate_usd_tnd)
            
            if str(currency_list_1.currentText()) == "TND" and str(currency_list_2.currentText()) == "USD":
                converted_amount = float(to_be_converted.text()) * float(1 / rate_usd_tnd)
                
            if to_be_converted != '':
                converted.setText(str(converted_amount))
        convert_btn.clicked.connect(printing)
       
    

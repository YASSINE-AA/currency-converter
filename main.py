from PySide2.QtWidgets import QApplication
from app_class import *
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
    
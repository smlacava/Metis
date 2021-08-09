import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import  QFileDialog
from pathlib import Path
import webbrowser as wb
import numpy as np
from data_loader import *

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metis_path = Path(os.path.dirname(__file__))
        graphics_path = self.metis_path / 'Graphics'
        gui_name = str(graphics_path / "problem.ui")
        uic.loadUi(gui_name, self)

        if len(sys.argv) > 1:
            self.text.setText(sys.argv[1])

        self.ok_button.clicked.connect(self.ok_interface)

    def ok_interface(self):
        self.exit()

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

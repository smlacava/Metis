import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import  QFileDialog
import metis_study as ms
from pathlib import Path
import webbrowser as wb
import os
import numpy as np
from data_loader import *

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metis_path = Path(os.path.dirname(__file__))
        graphics_path = self.metis_path / 'Graphics'
        gui_name = str(graphics_path / "Input_request.ui")
        uic.loadUi(gui_name, self)

        L = len(sys.argv)
        d = int(sys.argv[L-1])
        if d == 0:
            self.gui_call = "python " + str(self.metis_path / "Single_analysis.py")
            d = 1
        else:
            self.gui_call = "python " + str(self.metis_path / "Double_analysis.py")

        if L > 1:
            for i in range(1, L-1): #the final number is not considered
                self.gui_call += " " + sys.argv[i]

        images_path = self.metis_path / 'Images'
        self.file_title.setText("2D matrix detected in " + sys.argv[d])
        self.exit_button.clicked.connect(self.previous_interface)
        self.data_file_search.clicked.connect(self.file_search)
        self.run_button.clicked.connect(self.ok)
        self.loader = data_loader()

    def previous_interface(self):
        gui_call = self.gui_call
        self.exit()
        os.system(gui_call)

    def open_wiki(self):
        wb.open_new('https://github.com/smlacava/Metis/wiki/Single-analysis')


    def ok(self):
        self.gui_call = self.gui_call + " " + self.labels_file_text.text()
        self.previous_interface()


    def exit(self):
        self.close()

    def file_search(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                      "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.labels_file_text.setText(fileName)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import  QFileDialog
import metis_study as ms
from pathlib import Path
import webbrowser as wb
import os
import Double_analysis

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metis_path = Path(os.path.dirname(__file__))
        graphics_path = self.metis_path / 'Graphics'
        gui_name = str(graphics_path / "Metis.ui")
        uic.loadUi(gui_name, self)
        images_path = self.metis_path / 'Images'
        self.help_button.setIcon(QtGui.QIcon(str(images_path / "jar_logo.png")))
        self.help_button.clicked.connect(self.open_wiki)
        self.single_button.clicked.connect(self.single_analysis)
        self.double_button.clicked.connect(self.double_analysis)

    def single_analysis(self):
        self.exit()
        os.system("python " + str(self.metis_path / "Single_analysis.py"))

    def double_analysis(self):
        self.exit()
        os.system("python "+str(self.metis_path / "Double_analysis.py"))

    def open_wiki(self):
        wb.open_new('https://github.com/smlacava/Metis/wiki')

    def exit(self):
        self.close()

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

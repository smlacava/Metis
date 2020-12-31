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
        gui_name = str(graphics_path / "Single_analysis.ui")
        uic.loadUi(gui_name, self)

        ## Labels file management
        self.first_labels_file = None
        L = len(sys.argv)
        if L > 1:
            self.data_file.setText(sys.argv[1])
            if L > 2:
                self.report_directory_name.setText(sys.argv[2])
                if L > 3:
                    self.report_file_name.setText(sys.argv[3])
                    if L > 4:
                        self.first_labels_file = sys.argv[4]

        images_path = self.metis_path / 'Images'
        self.help_button.setIcon(QtGui.QIcon(str(images_path / "jar_logo.png")))
        self.data_file_search.clicked.connect(self.file_search)
        self.run_button.clicked.connect(self.first_labels_check)
        self.directory_search.clicked.connect(self.report_directory_search)
        self.help_button.clicked.connect(self.open_wiki)
        self.previous_button.clicked.connect(self.previous_interface)
        self.next_button.clicked.connect(self.next_interface)
        self.check_states = {0:False, 2:True}
        self.loader = data_loader()

    def previous_interface(self):
        self.exit()
        os.system("python " + str(self.metis_path / "Metis.py"))

    def open_wiki(self):
        wb.open_new('https://github.com/smlacava/Metis/wiki/Single-analysis')

    def first_labels_check(self):
        first_file = self.data_file.text()
        first = np.array(self.loader.load_data(first_file))
        if len(np.shape(first)) == 2 and self.first_labels_file is None:
            #send each parameter and then the number of file of which require the labels
            gui_call = "python " + str(self.metis_path / "Labels_request.py") + " " + first_file
            gui_call += " "  + self.report_directory_name.text() + " " + self.report_file_name.text() + " 0"
            self.exit()
            os.system(gui_call)
        else:
            self.run_analysis(first)

    def run_analysis(self, first):
        report_file = str(Path(self.report_directory_name.text()) / self.report_file_name.text())
        x = ms.metis_study()
        report_state = self.check_states[self.export_report.checkState()]
        if len(np.shape(first)) == 3:
            lbl = None
        else:
            lbl = self.loader.load_data(self.first_labels_file)
        x.data_analysis(first, view_analysis=True, generate_pdf=report_state, distance='euclidean',
                        report_name=report_file, labels=lbl)
        if report_state is True:
            wb.open_new(report_file)

    def next_interface(self):
        first_file = self.data_file.text()
        first = np.array(self.loader.load_data(first_file))
        if len(np.shape(first)) == 2 and self.first_labels_file is None:
            self.first_labels_check()
            return
        gui_call = "python "+str(self.metis_path / "Single_analysis_parameters.py")+" "+first_file+" "
        gui_call = gui_call+self.report_directory_name.text()+" "+self.report_file_name.text()+" "+self.first_labels_file
        self.exit()
        print('Opening Single Analysis parameters interface')
        os.system(gui_call)

    def exit(self):
        self.close()

    def report_directory_search(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dirName = QFileDialog.getExistingDirectory(self)
        if dirName:
            self.report_directory_name.setText(dirName)

    def file_search(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                      "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.data_file.setText(fileName)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

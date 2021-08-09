import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import  QFileDialog
import metis_study as ms
from pathlib import Path
import webbrowser as wb
from data_loader import *

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metis_path = Path(os.path.dirname(__file__))
        graphics_path = self.metis_path / 'Graphics'
        gui_name = str(graphics_path / "Double_analysis.ui")
        uic.loadUi(gui_name, self)

        ## Labels file management
        self.first_labels_file = "None"
        self.second_labels_file = "None"
        L = len(sys.argv)
        if L > 1:
            self.first_file.setText(sys.argv[1])
            if L > 2:
                self.second_file.setText(sys.argv[2])
                if L > 3:
                    self.report_directory_name.setText(sys.argv[3])
                    if L > 4:
                        self.report_file_name.setText(sys.argv[4])
                        if L > 5:
                            self.first_labels_file = sys.argv[5]
                            if L > 6:
                                self.second_labels_file = sys.argv[6]

        images_path = self.metis_path / 'Images'
        self.help_button.setIcon(QtGui.QIcon(str(images_path / "owl_logo.png")))
        self.first_search.clicked.connect(self.first_file_search)
        self.second_search.clicked.connect(self.second_file_search)
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

    def next_interface(self):
        try:
            first_file = self.first_file.text()
            first = np.array(self.loader.load_data(first_file))
            if len(np.shape(first)) == 2 and self.first_labels_file is "None":
                self.first_labels_check()
                return
            second_file = self.second_file.text()
            second = np.array(self.loader.load_data(second_file))
            if len(np.shape(second)) == 2 and self.second_labels_file is "None":
                self.second_labels_check(first)
                return
            gui_call = "python " + str(self.metis_path / "Double_analysis_parameters.py") + " " + self.first_file.text()
            gui_call = gui_call + " " + self.second_file.text() + " " + self.report_directory_name.text() + " "
            gui_call = gui_call + self.report_file_name.text() + " " + self.first_labels_file + " " +self.second_labels_file
            print(gui_call)
            self.exit()
            print('Opening Double Analysis parameters interface')
            os.system(gui_call)
        except:
            os.system("python " + str(self.metis_path / "problem.py"))


    def open_wiki(self):
        wb.open_new('https://github.com/smlacava/Metis/wiki/Double-analysis')


    def first_labels_check(self):
        try:
            first_file = self.first_file.text()
            first = np.array(self.loader.load_data(first_file))
            if len(np.shape(first)) == 2 and self.first_labels_file is "None":
                second_file = self.second_file.text()
                #send each parameter and then the number of file of which require the labels
                gui_call = "python " + str(self.metis_path / "Labels_request.py") + " " + first_file + " "
                gui_call += second_file + " "  + self.report_directory_name.text() + " " + self.report_file_name.text()
                gui_call += " 1"
                self.exit()
                os.system(gui_call)
            else:
                self.second_labels_check(first)
        except:
            os.system("python " + str(self.metis_path / "problem.py"))


    def second_labels_check(self, first):
        try:
            second_file = self.second_file.text()
            second = np.array(self.loader.load_data(second_file))
            if len(np.shape(second)) == 2 and self.second_labels_file is "None":
                first_file = self.first_file.text()
                #send each parameter and then the number of file of which require the labels
                gui_call = "python " + str(self.metis_path / "Labels_request.py") + " " + first_file + " "
                gui_call += second_file + " "  + self.report_directory_name.text() + " " + self.report_file_name.text()
                gui_call += " " + self.first_labels_file + " 2"
                self.exit()
                os.system(gui_call)
            else:
                self.run_analysis(first, second)
        except:
            os.system("python " + str(self.metis_path / "problem.py"))


    def run_analysis(self, first, second):
        try:
            report_file = str(Path(self.report_directory_name.text()) / self.report_file_name.text())
            x = ms.metis_study()
            report_state = self.check_states[self.export_report.checkState()]
            if len(np.shape(first)) == 3:
                first_lbl = None
            else:
                first_lbl = self.loader.load_data(self.first_labels_file)
            if len(np.shape(second)) == 3:
                second_lbl = None
            else:
                second_lbl = self.loader.load_data(self.second_labels_file)
            x.groups_comparison(first, second, view_analysis=True, generate_pdf=report_state,
                                distance='euclidean', first_labels=first_lbl,
                                second_labels=second_lbl, report_name=report_file, threshold=0.01)
            if report_state is True:
                wb.open_new(report_file)
        except:
            os.system("python " + str(self.metis_path / "problem.py"))


    def exit(self):
        self.close()

    def first_file_search(self):
        fileName = self.file_search()
        if not(fileName is False):
            self.first_file.setText(fileName)

    def second_file_search(self):
        fileName = self.file_search()
        if not(fileName is False):
            self.second_file.setText(fileName)

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
            return fileName
        else:
            return False

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

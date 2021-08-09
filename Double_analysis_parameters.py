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
        gui_name = str(graphics_path / "Double_analysis_parameters.ui")
        uic.loadUi(gui_name, self)

        ## Labels file management
        self.first_labels_file = "None"
        self.second_labels_file = "None"
        L = len(sys.argv)
        if L > 1:
            self.first_file = sys.argv[1]
            if L > 2:
                self.second_file = sys.argv[2]
                if L > 3:
                    self.report_directory_name = sys.argv[3]
                    if L > 4:
                        self.report_file_name = sys.argv[4]
                        if L > 5:
                            self.first_labels_file = sys.argv[5]
                            if L > 6:
                                self.second_labels_file = sys.argv[6]

        images_path = self.metis_path / 'Images'
        self.help_button.setIcon(QtGui.QIcon(str(images_path / "owl_logo.png")))
        self.run_button.clicked.connect(self.run_analysis)
        self.help_button.clicked.connect(self.open_wiki)
        self.previous_button.clicked.connect(self.previous_interface)
        self.check_states = {0:False, 2:True}
        self.loader = data_loader()

    def previous_interface(self):
        self.exit()
        gui_call = "python " + str(self.metis_path / "Double_analysis.py") + " " + self.first_file + " "
        gui_call += self.second_file + " " + self.report_directory_name + " " + self.report_file_name + " "
        gui_call += self.first_labels_file + " " + self.second_labels_file
        print('Opening Double Analysis interface')
        os.system(gui_call)

    def open_wiki(self):
        wb.open_new('https://github.com/smlacava/Metis/wiki/Double-analysis')

    def selected_distance(self):
        if self.Euclidean.isChecked() is True:
            return 'euclidean'
        elif self.Manhattan.isChecked() is True:
            return 'manhattan'
        if self.Minkowski.isChecked() is True:
            return 'minkowski'
        if self.Mahalanobis.isChecked() is True:
            return 'mahalanobis'

    def selected_algorithm(self):
        if self.No.isChecked() is True:
            return None
        elif self.Columns.isChecked() is True:
            return 'columns'
        elif self.PCA.isChecked() is True:
            return 'pca'
        elif self.ICA.isChecked() is True:
            return 'ica'

    def chosen_features(self):
        algorithm = self.selected_algorithm()
        if algorithm is None:
            features = None
        elif 'columns' in algorithm:
            aux_features = str(self.features.text())
            if ',' in aux_features:
                divisor = ','
            else:
                divisor = " "
            f_list = aux_features.split(divisor)
            map_object = map(int, f_list)
            features = list(map_object)
            if isinstance(features, int):
                features = [features]
        else:
            features = int(self.features.text())
        return features

    def run_analysis(self):
        try:
            first = np.array(self.loader.load_data(self.first_file))
            second = np.array(self.loader.load_data(self.second_file))
            report_file = str(Path(self.report_directory_name) / self.report_file_name)
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
            features = self.chosen_features()
            x.groups_comparison(first, second, view_analysis=True, generate_pdf=report_state,
                                distance=self.selected_distance(), first_labels=first_lbl,
                                second_labels=second_lbl, report_name=report_file, first_name=self.first_name.text(),
                                second_name=self.second_name.text(), features_selection_algorithm=self.selected_algorithm(),
                                selected_features=features)
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

import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import  QFileDialog
import metis_study as ms
from pathlib import Path
import webbrowser as wb
import os

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        metis_path = Path(os.path.dirname(__file__))
        graphics_path = metis_path / 'Graphics'
        gui_name = str(graphics_path / "mainwindow.ui")
        uic.loadUi(gui_name, self)
        images_path = metis_path / 'Images'
        self.help_button.setIcon(QtGui.QIcon(str(images_path / "jar_logo.png")))
        self.exit_button.clicked.connect(self.exit)
        self.first_search.clicked.connect(self.first_file_search)
        self.second_search.clicked.connect(self.second_file_search)
        self.run_button.clicked.connect(self.run_analysis)
        self.directory_search.clicked.connect(self.report_directory_search)
        self.help_button.clicked.connect(self.open_wiki)

    def open_wiki(self):
        wb.open_new('https://github.com/smlacava/Metis/wiki')


    def run_analysis(self):
        first = [[1, 2, 3, 4, 2, 3, 4, 5, 2, 3, 4, 5], [4, 5, 6, 7, 5, 6, 7, 8, 2, 3, 4, 5],
                 [2, 3, 4, 5, 3, 4, 5, 6, 2, 3, 4, 5], [2, 5, 6, 7, 5, 2, 7, 2, 2, 3, 4, 5]]
        second = [[1, 2, 3, 4, 2, 3, 3, 5, 2, 3, 4, 5], [2, 5, 6, 7, 5, 2, 7, 2, 2, 3, 4, 5],
                  [3, 4, 2, 4, 3, 6, 1, 2, 2, 3, 4, 5], [2, 5, 6, 7, 5, 2, 7, 2, 2, 3, 4, 5]]
        report_file = str(Path(self.report_directory_name.text()) / self.report_file_name.text())
        x = ms.metis_study()
        x.groups_comparison(first, second, view_analysis=True, generate_pdf=True,
                            distance='euclidean', first_labels=[1, 0, 1, 0],
                            second_labels=[0, 1, 1, 0], report_name=report_file,
                            features_selection_algorithm='pca',
                            selected_features=0.99)
        wb.open_new(report_file)

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

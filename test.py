import sys
import os
import metis_study as ms
from pathlib import Path
import webbrowser as wb
import os
from data_loader import *

report_file = str(Path(r'D:\Ricerca\report.pdf'))
first_file = r'D:\Ricerca\Metis_data.mat'
second_file = first_file
labels_file = r'D:\Ricerca\Metis_labels.mat'

loader = data_loader()
first = np.array(loader.load_data(first_file))
second = np.array(loader.load_data(second_file))
lbl = np.array(loader.load_data(labels_file))

x = ms.metis_study()
x.data_analysis(first, view_analysis=True, generate_pdf=True, distance='euclidean',
                report_name=report_file, labels=lbl,
                features_selection_algorithm='columns', selected_features=[1, 2])
x.groups_comparison(first, second, view_analysis=True, generate_pdf=True,
                    distance='euclidean', first_labels=lbl,
                    second_labels=lbl, report_name=report_file,
                    features_selection_algorithm='pca',
                    selected_features=3)

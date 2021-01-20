import sys
import os
import metis_study as ms
from pathlib import Path
import webbrowser as wb
import os
from data_loader import *
from clustering import *
import webbrowser as wb
from data_manager import *

class tester():
    def __init__(self):
        self.outPath = r'D:\Ricerca'
        self.report_file = 'report.pdf'
        first_file = r'D:\Ricerca\Metis_data.mat'
        second_file = r'D:\Ricerca\Metis_data2.mat'
        all_file = r'D:\Ricerca\Metis_data_all.mat'
        all_labels_file = r'D:\Ricerca\Metis_labels_all.mat'
        labels_file = r'D:\Ricerca\Metis_labels.mat'

        self.loader = data_loader()
        self.first = np.array(self.loader.load_data(first_file))
        self.second = np.array(self.loader.load_data(second_file))
        self.all = np.array(self.loader.load_data(all_file))
        self.lbl = np.array(self.loader.load_data(labels_file))
        self.lbl_all = np.array(self.loader.load_data(all_labels_file))
        self.data_manager = data_manager()

        self.metis = ms.metis_study()
        self.clustering = clustering()

    def data_analysis(self, view=True, pdf=True, dist='euclidean', selection='columns', selected=[1,2], thr=None, biometric=True):
        if len(np.shape(self.first)) == 3:
            [self.first, self.lbl] = self.data_manager.data_management(self.first)
        self.metis.data_analysis(self.first, view_analysis=view, generate_pdf=pdf, distance=dist, threshold=thr,
                                 report_name=self.report_file, outPath=self.outPath, labels=self.lbl,
                                 features_selection_algorithm=selection,
                                 selected_features=selected, biometric_analysis=biometric)
        if pdf is True:
            wb.open_new(str(Path(self.outPath) / self.report_file))

    def groups_comparison(self, view=True, pdf=True, dist='euclidean', selection='columns', selected=[1,2],
                          thr=None, biometric=True, statistical=True, permutation=False, perm_method='approximate'):
        if len(np.shape(self.first)) == 3:
            [self.first, self.lbl] = self.data_manager.data_management(self.first)
        if len(np.shape(self.second)) == 3:
            [self.second, self.lbl2] = self.data_manager.data_management(self.second)
        self.metis.groups_comparison(self.first, self.second, view_analysis=view, generate_pdf=pdf, distance=dist,
                                     first_labels=self.lbl, second_labels=self.lbl2, report_name=self.report_file,
                                     outPath=self.outPath, features_selection_algorithm=selection,
                                     selected_features=selected, permutation_test=permutation,
                                     permutation_method=perm_method,
                                     biometric_analysis=biometric, statistical_analysis=statistical, threshold=thr)
        if pdf is True:
            wb.open_new(str(Path(self.outPath) / self.report_file))

    def clustering_analysis(self, clusters=2, view=True, save=False, group_name=""):
        data_delta = np.squeeze(self.all[:, 0, 1:10])
        [data, labels] = self.data_manager.data_management(self.all[:, 0, 1:10])
        self.metis.clustering_analysis(data, clusters, view, save, self.outPath, group_name)
        if save is True:
            wb.open_new(str(Path(self.outPath) / (group_name+"clustering.png")))

t = tester()
#t.data_analysis(selection=None)
t.groups_comparison(statistical=False, biometric=False, selected=[0,1, 3, 5], permutation=True, perm_method='approximate')
#t.clustering_analysis(save=True)
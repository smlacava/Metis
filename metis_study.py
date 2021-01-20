import numpy as np
from distances import *
from statistical_analysis import *
from data_manager import *
from biometric_performance import *
from report import *
from feature_selector import *
from data_loader import *
from clustering import *
from permutation_test import *
from utils import *

class metis_study():
    def __init__(self, data=None, distance=euclidean_distance()):
        """
        The __init__ method is the initializer of the class.

        :param data:     is the data matrix as to analyze (optional, it can be 3D or 2D)
        :param distance: it is the function (or one string between 'euclidean', 'manhattan', 'mahalanobis' and
                         'minkowski', representing the homonymous distances) which is used in order to evaluate the
                         distance in the genuine and impostor scores computation (optional, euclidean distance by
                         default)
        """
        self._set_parameters(data, distance)
        self._utils = utils()
        self._statan = statistical_analysis()
        self._data_manager = data_manager()
        self._biom = biometric_performance()
        self._report_generator = report()
        self._features_selector = features_selector()
        self._data_loader = data_loader()
        self._clustering = clustering()
        self._perm_test = permutation_test()


    def set_data(self, data):
        """
        The set_data method allows to insert the 3D-matrix which has to be analyzed.

        :param data: is the (subjects*repetitions*features) 3D-matrix or the (samples*features) 2D-matrix which has to
                     be analyzed
        """
        if isinstance(data, str):
            data = self._data_loader.load_data(data)
        self.data, self.first_labels = self._data_manager.data_management(data)


    def set_distance(self, distance):
        """
        The set_distance method allows set the distance function which has to be
        used in computing the genuine and impostor scores.

        :param distance: is the distance function, or a string between 'euclidean', 'manhattan', 'mahalanobis' and
                         'minkowski', representing the homonymous functions.
        """
        if type(distance) is str:
            available_dist = {'euclidean': euclidean_distance(), 'manhattan': manhattan_distance(),
                              'minkowski': minkowski_distance(), 'mahalanobis': mahalanobis_distance()}
            self.distance = available_dist[distance]
        else:
            self.distance = distance


    def compute_scores(self, data=None, distance=None):
        """
        The compute_scores method computes the scores related to data.

        :param data:     is the (subjects*repetitions*features) 3D-matrix or (samples*features) 2D-matrix which has to
                         be analyzed (None by default, the previous data will be used if None)
        :param distance: is the function (or one string between 'euclidean', 'manhattan', 'mahalanobis' and
                         'minkowski', representing the homonymous distances) which is used in order to evaluate the
                         distance in the genuine and impostor scores computation (None by default, the previously
                         inserted data if None)

        :return:         the 1D-array representing the genuine scores (genuine_scores) and the impostor scores
                         (impostor_scores)
        """
        self._set_parameters(data, distance)
        self.distance.set_parameters(self.data)
        return self._biom.compute_scores(self.data, self.distance)


    def genuines_and_impostors(self, scores, labels):
        """
        The genuines_and_impostors method computes the genuine and impostor scores.

        :param scores: it is the 2D data matrix representing the scores between the
                       repetitions related to the subjects
        :param labels: it is the list of labels associated to each sample (equal labels identify the same subject)

        :return:       the genuine and the impostor scores, and the thresholds representing the unique value shown by
                       the scores, represented as three 1D arrays
        """
        genuine_score, impostor_score, thresholds = self._biom.genuines_and_impostors(scores, labels)
        return genuine_score, impostor_score, thresholds


    def _set_parameters(self, data=None, distance=None):
        """
        The _set_parameters method updates the data and/or distance function to analyze (FOR INTERNAL USE ONLY).

        :param data:     is the (subjects*repetitions*features) 3D-matrix or the (samples*features) 2D-matrix which has
                         to be analyzed (None by default, the previous data will be used if None)
        :param distance: is the function (or one string between 'euclidean', 'manhattan', 'mahalanobis' and 'minkowski',
                         representing the homonymous distances) which is used in order to evaluate the distance in the
                         genuine and impostor scores computation (None by default, the previously inserted data if None)
        """
        if not (data is None):
            self.set_data(data)
        if not (distance is None):
            self.set_distance(distance)


    def groups_comparison(self, first_data, second_data=None, first_labels=None, second_labels=None,
                          distance=euclidean_distance(), threshold=None, view_analysis=False, generate_pdf=False,
                          first_name="first", second_name="second", bins=None, report_name="report.pdf", outPath=None,
                          features_selection_algorithm=None, selected_features=None, biometric_analysis=True,
                          statistical_analysis=True, permutation_test=True, permutation_method='approximate',
                          permutation_assumption='different', permutation_repetitions=100):
        """
        The groups_comparison method computes an analysis between two groups, represented as two different 3D
        (subjects*repetitions*features) data matrices or 2D (subjects*features) data matrices (in this case the labels
        related to each file is also required), eventually reporting it on a pdf file.

        :param first_data:                  it is the first 3D (subjects*repetitions*features) or 2D (subjects*features)
                                            data matrix
        :param second_data:                 it is the second 3D (subjects*repetitions*features) or 2D
                                            (subjects*features) data matrix (None by default, a previously inserted
                                            matrix will be used if it is None)
        :param first_labels:                it is the list of labels related to the first data matrix (required in case
                                            of 2D matrix)
        :param second_labels:               it is the list of labels related to the second data matrix (required in case
                                            of 2D matrix)
        :param distance:                    it is the function (or one string between 'euclidean', 'manhattan',
                                            'mahalanobis' and 'minkowski', representing the homonymous distances) which
                                            is used in order to evaluate the distance in the genuine and impostor scores
                                            computation (optional, euclidean distance by default)
        :param view_analysis:               it has to be True in order to print the results of the analysis, False
                                            otherwise (False by default)
        :param generate_pdf:                it has to be True in order to create the pdf of the analysis report, False
                                            otherwise (False by default)
        :param first_name:                  it is the name of the first group ("first" by default)
        :param second_name:                 it is the name of the second group ("second" by default)
        :param bins:                        it is the number of bins which has to be used (None by default, if None it
                                            will be computed automatically)
        :param report_name:                 it is the name of the eventually generated pdf ("report.pdf" by default)
        :param outPath:                     it is the directory in which export the report and the related figures
                                            (None by default)
        :param feature_selection_algorithm: it is the feature selection algorithm between 'pca' (for Principal Component
                                            Analysis), 'ica' (for Independent Component Analysis) 'columns' (for
                                            selecting the features by their indexes) or None for avoiding the feature
                                            selection step (None by default)
        :param selected_features:           it is the list of feature indexes if feature_selection_algorithm has value
                                            'columns', or the number of features in other case (even the contribution in
                                            the 'pca' case) or None for avoiding the feature selection step (None by
                                            default)
        :param biometric_analysis:          it has to be True for executing the biometric analysis, False otherwise
                                            (True by default)
        :param statistical_analysis:        it has to be True for executing the statistical analysis, False otherwise
                                            (True by default)
        :param permutation_test:            it has to be True for executing the permutation test, False otherwise
                                            (True by default)
        :param permutation_method:          it is the method applied for executing the permutation test between
                                            'approximate' and 'exact' ('approximate by default)
        :param permutation_assumption:      it is the assumption used in the permutation test, between 'lower' (or
                                            'first_lower'), 'higher' (or 'first_higher') or 'different' ('different' by
                                            default)
        :param permutation_repetitions:     it is the number of permutation test repetitions in the approximate case
                                            (100 by default)
        """
        if second_data is None and not (self.data is None):
            second_data = first_data
            first_data = self.data
        if isinstance(first_data, str):
            first_data = self._data_loader.load_data(first_data)
        if isinstance(second_data, str):
            second_data = self._data_loader.load_data(second_data)
        self.set_distance(distance)
        first_data, second_data = self._statan.statistics_settings(first_data, second_data)
        self._report_generator.groups_comparison(self._data_manager,
                                                 self._statan, self._biom, self._features_selector, self._perm_test,
                                                 first_data, second_data, first_labels, second_labels,
                                                 self.distance, threshold, view_analysis, generate_pdf, first_name,
                                                 second_name, bins, report_name, outPath,
                                                 features_selection_algorithm, selected_features,
                                                 statistical_analysis=statistical_analysis,
                                                 biometric_analysis=biometric_analysis,
                                                 permutation_test=permutation_test,
                                                 permutation_method=permutation_method,
                                                 permutation_assumption=permutation_assumption,
                                                 permutation_repetitions=permutation_repetitions)


    def data_analysis(self, data, labels=None, distance=euclidean_distance(), threshold=None, view_analysis=False,
                      generate_pdf=False, name="first", bins=None, report_name="report.pdf", outPath=None,
                      features_selection_algorithm=None, selected_features=None, biometric_analysis=True):
        """
        The groups_comparison method computes an analysis between two groups, represented as two different 3D
        (subjects*repetitions*features) data matrices or 2D (subjects*features) data matrices (in this case the labels
        related to each file is also required), eventually reporting it on a pdf file.

        :param data:                        it is the 3D (subjects*repetitions*features) or 2D (subjects*features) data
                                            matrix
        :param labels:                      it is the list of labels related to the data matrix (required in case of 2D
                                            matrix)
        :param distance:                    it is the function (or one string between 'euclidean', 'manhattan',
                                            'mahalanobis' and 'minkowski', representing the homonymous distances) which
                                            is used in order to evaluate the distance in the genuine and impostor scores
                                            computation (optional, euclidean distance by default)
        :param view_analysis:               it has to be True in order to print the results of the analysis, False
                                            otherwise (False by default)
        :param generate_pdf:                it has to be True in order to create the pdf of the analysis report, False
                                            otherwise (False by default)
        :param name:                        it is the name of the first group ("first" by default)
        :param bins:                        it is the number of bins which has to be used (None by default, if None it
                                            will be computed automatically)
        :param report_name:                 it is the name of the eventually generated pdf ("report.pdf" by default)
        :param outPath:                     it is the directory in which export the report and the related figures
                                            (None by default)
        :param feature_selection_algorithm: it is the feature selection algorithm between 'pca' (for Principal Component
                                            Analysis), 'ica' (for Independent Component Analysis) 'columns' (for
                                            selecting the features by their indexes) or None for avoiding the feature
                                            selection step (None by default)
        :param selected_features:           it is the list of feature indexes if feature_selection_algorithm has value
                                            'columns', or the number of features in other case (even the contribution in
                                            the 'pca' case) or None for avoiding the feature selection step (None by
                                            default)
        :param biometric_analysis:          it has to be True for executing the biometric analysis, False otherwise
                                            (True by default)
        """
        if data is None:
            data = self.data
        if isinstance(data, str):
            data = self._data_loader.load_data(data)
        self.set_distance(distance)
        self._report_generator.single_analysis(self._data_manager, self._statan, self._biom, self._features_selector,
                                               self._perm_test, data, labels, self.distance, threshold,
                                               view_analysis, generate_pdf, name, bins, report_name, outPath,
                                               features_selection_algorithm, selected_features,
                                               biometric_analysis=biometric_analysis)

    def clustering_analysis(self, data=None, clusters=None, view=True, save=False, outPath=None, group_name=""):
        """
        The clustering_analysis method performs the whole clustering analysis, from the clustering searching to the
        final plots.

        :param data:       it is the 2D (samples*features) data matrix
        :param clusters:   it is the number of cluster to evaluate, or None to use the previously inserted clusters
                           (None by default)
        :param view:       it has to be True in order to show the resulting plots, False otherwise (True by default)
        :param save:       it has to be True in order to save the resulting figure as clustering.png, False othersise
                           (False by default)
        :param outPath:    it is the directory in which eventually store the resulting figure (None by default)
        :param group_name: it is the name of the group related to the data matrix (optional)
        """
        if data is None:
            data = self.data
        if isinstance(data, str):
            data = self._data_loader.load_data(data)
        [data, labels] = self._data_manager.data_management(data)
        self._clustering.cluster_analysis(data, clusters, view, save, outPath, group_name)

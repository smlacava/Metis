import numpy as np


from distances import *
from statistical_analysis import *
from data_manager import *
from biometric_performance import *
from report import *
from feature_selector import *
from data_loader import *

class metis_study():
    def __init__(self, data=None, distance=euclidean_distance()):
        """
        The __init__ method is the initializer of the class.

        :param data:     it is the (subjects*repetitions*features) 3D-matrix as
                         to analyze (optional)
        :param distance: it is the function (or one string between 'euclidean',
                         'manhattan' and 'minkowski', representing the homonymous
                         distances) which is used in order to evaluate the distance
                         in the genuine and impostor scores computation (optional,
                         euclidean distance by default)
        """
        self._set_parameters(data, distance)
        self._statan = statistical_analysis()
        # self._statan = statan.statistical_analysis()
        self._data_manager = data_manager()
        # self._data_manager = man.data_manager()
        self._biom = biometric_performance()
        # self._biom = biom.biometric_performance()
        self._report_generator = report()
        # self._report_generator = rep.report()
        self._features_selector = features_selector()
        # self._features_selector = sel.features_selector()
        self._data_loader = data_loader()

    def set_data(self, data):
        """
        The set_data method allows to insert the 3D-matrix which has to be analyzed.

        :param data:     it is the (subjects*repetitions*features) 3D-matrix as
                         to analyze
        """
        if isinstance(data, str):
            data = self._data_loader.load_data(data)
        self.data, self.first_labels = self._data_manager.data_management(data)

    def set_distance(self, distance):
        """
        The set_distance method allows set the distance function which has to be
        used in computing the genuine and impostor scores.

        :param distance: it is the distance function, or a string between
                         'euclidean', 'manhattan' and 'minkowski', representing the
                         homonymous functions.
        """
        if type(distance) is str:
            available_dist = {'euclidean': euclidean_distance(), 'manhattan': manhattan_distance(),
                              'minkowski': minkowski_distance(), 'mahalanobis': mahalanobis_distance()}
            # available_dist = {'euclidean':dst.euclidean_distance(), 'manhattan':dst.manhattan_distance(), 'minkowski':dst.minkowski_distance(), 'mahalanobis':dst.mahalanobis_distance()}
            self.distance = available_dist[distance]
        else:
            self.distance = distance

    def compute_scores(self, data=None, distance=None):
        """
        The compute_scores method computes the scores related to data.

        :param data:     it is the (subjects*repetitions*features) 3D-matrix as
                         to analyze (None by default, the previous data will be used
                         if None)
        :param distance: it is the function (or one string between 'euclidean',
                         'manhattan' and 'minkowski', representing the homonymous
                         distances) which is used in order to evaluate the distance
                         in the genuine and impostor scores computation (None by
                         default, the previously inserted data if None)

        :return:         the 1D-array representing the genuine scores
                         (genuine_scores) and the impostor scores (impostor_scores)
        """
        self._set_parameters(data, distance)
        self.distance.set_parameters(self.data)
        return self._biom.compute_scores(self.data, self.distance)

    def genuines_and_impostors(self, scores, labels):
        """
        The genuines_and_impostors method computes the genuine and impostor scores.

        :param scores: it is the 2D data matrix representing the scores between the
                       repetitions related to the subjects

        :return:       the genuine and the impostor scores, and the thresholds
                       representing the unique value shown by the scores,
                       represented as three 1D arrays
        """
        genuine_score, impostor_score, thresholds = self._biom.genuines_and_impostors(scores, labels)
        return genuine_score, impostor_score, thresholds

    def _set_parameters(self, data=None, distance=None):
        """
        The _set_parameters method updates the data and/or distance function to
        analyze (FOR INTERNAL USE ONLY).

        :param data:     it is the (subjects*repetitions*features) 3D-matrix as
                         to analyze (None by default, the previous data will be used
                         if None)
        :param distance: it is the function (or one string between 'euclidean',
                         'manhattan' and 'minkowski', representing the homonymous
                         distances) which is used in order to evaluate the distance
                         in the genuine and impostor scores computation (None by
                         default, the previously inserted data if None)
        """
        if not (data is None):
            self.set_data(data)
        if not (distance is None):
            self.set_distance(distance)

    def groups_comparison(self, first_data, second_data=None, first_labels=None,
                          second_labels=None, distance=euclidean_distance(),
                          view_analysis=False, generate_pdf=False,
                          first_name="first", second_name="second", bins=None,
                          report_name="report.pdf",
                          features_selection_algorithm=None,
                          selected_features=None):

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
                                                 self._statan, self._biom, self._features_selector,
                                                 first_data, second_data, first_labels, second_labels,
                                                 self.distance, view_analysis, generate_pdf, first_name,
                                                 second_name, bins, report_name,
                                                 features_selection_algorithm, selected_features)

    def data_analysis(self, data, labels=None, distance=euclidean_distance(),
                      view_analysis=False, generate_pdf=False, name="first",
                      bins=None, report_name="report.pdf",
                      features_selection_algorithm=None,
                      selected_features=None):
        if data is None:
            data = self.data
        if isinstance(data, str):
            data = self._data_loader.load_data(data)
        self.set_distance(distance)
        self._report_generator.single_analysis(self._data_manager, self._statan,
                                               self._biom, self._features_selector,
                                               data, labels, self.distance,
                                               view_analysis, generate_pdf, name,
                                               bins, report_name,
                                               features_selection_algorithm, selected_features)


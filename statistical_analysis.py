import numpy as np
from data_manager import *
from scipy.stats import ranksums
from utils import *

class statistical_analysis():
    def __init__(self):
        """
        The __init__ method is the initiaized, and sets the values for the initial attributes.
        """
        self._data_manager = data_manager()
        self._utils = utils()


    def compute_cohen_d(self, first_data, second_data):
        """
        The compute_cohen_d method computes the effects size between two array as the difference between two means
        divided by the pooled standard deviation (Cohen's d).

        :param first_data:  it is the first 1D-array
        :param second_fata: it is the second 1D-array

        :return:            the Cohen's d value
        """
        first_N = np.shape(first_data)[0]
        second_N = np.shape(second_data)[0]
        first_var = np.var(first_data, ddof=1)
        second_var = np.var(second_data, ddof=1)
        first_mean = np.mean(first_data)
        second_mean = np.mean(second_data)
        pooled_std = np.sqrt(((first_N - 1) * first_var + (second_N - 1) * second_var) / (
                    first_N + second_N - 2 + np.finfo(float).eps)) + np.finfo(float).eps
        return (first_mean - second_mean) / pooled_std


    def compute_features_statistics(self, first_data, second_data=None, first_labels=None, second_labels=None):
        """
        The compute_features_statistics method computes the Wilcoxon p-value and the Cohen's d effect size on the
        features between two data matrices.

        :param first_data:    it is the first (subjects*repetitions*features) matrix
        :param second_data:   it is the second (subjects*repetitions*features) matrix
                              (None by default, a previously inserted matrix will be used if it is None)
        :param first_labels:  it is the list of labels identifying each subject in the first dataset (None by default)
        :param second_labels: it is the list of labels identifying each subject in the second dataset (None by default)

        :return:              the (repetitions*features) pvalue and Cohen's d matrices, in order
        """
        [first, second] = self.statistics_settings(first_data, second_data)
        first_L, first_subjects, first_repetitions, first_features = self._utils._dimensions(first, first_labels)
        second_L, second_subjects, second_repetitions, second_features = self._utils._dimensions(second, second_labels)
        first, second = self._utils._same_format_3D(first, second, first_labels, second_labels)
        repetitions = np.min([first_repetitions, second_repetitions])
        features = np.min([first_features, second_features])
        pvalue = np.zeros(shape=(repetitions, features))
        d = np.zeros(shape=(repetitions, features))
        for r in range(repetitions):
            for f in range(features):
                [stat, p] = ranksums(np.squeeze(first[0:, r, f]),
                                     np.squeeze(second[0:, r, f]))
                d[r, f] = self.compute_cohen_d(np.squeeze(first[0:, r, f]),
                                               np.squeeze(second[0:, r, f]))
        return pvalue, d


    def compute_scores_statistics(self, first_data, second_data):
        """
        The compute_scores_statistics method computes the Wilcoxon p-value and the Cohen's d effect size on the features
        between two arrays.

        :param first_data:  it is the first 1D-array of scores
        :param second_data: it is the second 1D-array of scores

        :return:            the pvalue and Cohen's d value, in order
        """
        [stat, pvalue] = ranksums(np.squeeze(first_data), np.squeeze(second_data))
        d = self.compute_cohen_d(np.squeeze(first_data), np.squeeze(second_data))
        return pvalue, d


    def statistics_settings(self, first_data, second_data):
        """
        The statistics_settings method set the data which has to be used for some statistical analysis.

        :param first_data:  it is a data matrix
        :param second_data: it is another data matrix

        :return:            the two data matrices
        """
        first_data = np.array(first_data)
        second_data = np.array(second_data)
        return first_data, second_data
import numpy as np
from data_manager import *
from scipy.stats import ranksums, ks_2samp
from utils import *
import copy

class statistical_analysis():
    """
    The statistical_analysis class provides some statistical analysis or raw data and on the similarity scores.

    Methods:
        compute_cohen_d:             computes the effect size between two arrays as the Cohen's d
        compute_features_statistics: computes the Ranksum p-values and the Cohen's d values related to the comparison of
                                     two raw datasets
        compute_scores_statistics:   computes the Ranksum p-values and the Cohen's d values related to the comparison of
                                     two similarity score distributions
        compute_permutation_test:    TO ADD
    """


    def __init__(self):
        """
        The __init__ method is the initiaized, and sets the values for the initial attributes.
        """
        self._data_manager = data_manager()
        self._utils = utils()


    def compute_cohen_d(self, first_data, second_data):
        """
        The compute_cohen_d method computes the effect size between two array as the difference between two means
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
        return abs((first_mean - second_mean) / pooled_std)


    def compute_features_statistics(self, first_data, second_data, first_labels=None, second_labels=None):
        """
        The compute_features_statistics method computes the Wilcoxon p-value and the Cohen's d effect size on the
        features between two data matrices.

        :param first_data:    it is the first (subjects*repetitions*features) matrix
        :param second_data:   it is the second (subjects*repetitions*features) matrix
        :param first_labels:  it is the list of labels identifying each subject in the first dataset (None by default)
        :param second_labels: it is the list of labels identifying each subject in the second dataset (None by default)

        :return:              the (repetitions*features) pvalue and Cohen's d matrices, in order
        """
        [first, second, features] = self.statistics_settings(first_data, second_data, first_labels, second_labels)
        repetitions = 1
        pvalue = np.zeros(shape=(features,))
        d = np.zeros(shape=(features, ))
        for f in range(features):
            [stat, p] = ranksums(np.squeeze(first[0:, f]), np.squeeze(second[0:, f]))
            pvalue[f] = p
            d[f] = self.compute_cohen_d(np.squeeze(first[0:, f]), np.squeeze(second[0:, f]))
        return pvalue, d


    def compute_scores_statistics(self, first_data, second_data):
        """
        The compute_scores_statistics method computes the p-value through the two-sample Kolmogorov-Smirnov test and the
        Cohen's d effect size on the features between two arrays.

        :param first_data:  it is the first 1D-array of scores
        :param second_data: it is the second 1D-array of scores

        :return:            the pvalue and Cohen's d value, in order
        """
        first, second, first_features = self.statistics_settings(first_data, second_data)
        [stat, pvalue] = ks_2samp(np.squeeze(first), np.squeeze(second))
        d = self.compute_cohen_d(np.squeeze(first), np.squeeze(second))
        return pvalue, d


    def statistics_settings(self, first_data, second_data, first_labels=False, second_labels=False):
        """
        The statistics_settings method set the data which has to be used for some statistical analysis.

        :param first_data:    it is a data matrix
        :param second_data:   it is another data matrix
        :param first_labels:  it is the list of labels identifying each subject in the first dataset
        :param second_labels: it is the list of labels identifying each subject in the second dataset

        :return:            the two 2D data matrices, and the number of features
        """
        first = np.array(copy.deepcopy(first_data))
        second = np.array(copy.deepcopy(second_data))
        if first_labels is False or second_labels is False:
            aux_first = first
            aux_second = second
            first_features = 1
        else:
            first_L, first_subjects, first_repetitions, first_features = self._utils._dimensions(first, first_labels)
            second_L, second_subjects, second_repetitions, second_features = self._utils._dimensions(second, second_labels)
            first, second = self._utils._same_format_3D(first, second, first_labels, second_labels)
            nSamples_first = first_repetitions*first_subjects
            nSamples_second = second_repetitions*second_subjects
            aux_first = np.zeros(shape=(nSamples_first, first_features))
            aux_second = np.zeros(shape=(nSamples_second, first_features))
            for f in range(first_features):
                aux_first[:, f] = np.reshape(np.squeeze(first[0:, 0:, f]), (nSamples_first,))
                aux_second[:, f] = np.reshape(np.squeeze(second[0:, 0:, f]), (nSamples_second,))

        return aux_first, aux_second, first_features
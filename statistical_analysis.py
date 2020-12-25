import numpy as np
import data_manager as man
from scipy.stats import ranksums

class statistical_analysis():
    def __init__(self):
        #self._data_manager = data_manager()
        self._data_manager = man.data_manager()

    def compute_cohen_d(self, first_data, second_data):
        """
        The compute_cohen_d method computes the effects size between two array as
        the difference between two means divided by the pooled standard deviation
        (Cohen's d).

        :param first_data:  it is the first 1D-array
        :param second_fata: it is the second 1D-array

        :return: the Cohen's d value
        """
        first_N = len(first_data)
        second_N = len(second_data)
        first_var = np.var(first_data, ddof=1)
        second_var = np.var(second_data, ddof=1)
        first_mean = np.mean(first_data)
        second_mean = np.mean(second_data)
        pooled_std = np.sqrt(((first_N - 1) * first_var + (second_N - 1) * second_var) / (
                    first_N + second_N - 2 + np.finfo(float).eps)) + np.finfo(float).eps
        return (first_mean - second_mean) / pooled_std

    def _repetitions_check(self, data, labels):
        """
        The _repetitions_check method is used to check if the number of repetitions
        is equal all the subjects, and eventually compute that number (FOR INTERNAL
        USE ONLY).

        :param data:   it is the 2D data matrix
        :param labels: it is the array or the list representing the labels

        :return:       the number of repetitions, if it is equal for all the
                       subjects, -1 otherwise
        """
        names = np.unique(labels)
        repetitions = 0
        for name in names:
            count = 0
            for lbl in labels:
                if name == lbl:
                    count += 1
            if count != repetitions and repetitions != 0:
                return -1
            repetitions = count
        return repetitions

    def _stat_reshape(self, data, subjects, repetitions, features):
        aux_data = np.zeros((subjects, repetitions, features))
        for s in range(subjects):
            for r in range(repetitions):
                aux_data[s, r, :] = data[(s * repetitions) + r, 0:features]
        return aux_data

    def compute_features_statistics(self, first_data, second_data=None,
                                    first_labels=None, second_labels=None):
        """
        The compute_features_statistics method computes the Wilcoxon p-value and the
        Cohen's d effect size on the features between two data matrices.

        :param first_data:  it is the first (subjects*repetitions*features) matrix
        :param second_data: it is the second (subjects*repetitions*features) matrix
                            (None by default, a previously inserted matrix will be
                            used if it is None)

        :return: the (repetitions*features) pvalue and Cohen's d matrices, in order
        """
        [first, second] = self.statistics_settings(first_data, second_data)
        size = np.shape(first)
        L = len(size)
        subjects = size[0]
        features = size[L - 1]
        if L == 2:
            repetitions = 1
            if not (first_labels is None or second_labels is None):
                repetitions = self._repetitions_check(first, first_labels)
                if repetitions != -1 and self._repetitions_check(second, second_labels) == repetitions:
                    subjects = int(subjects / repetitions)
                    [first, first_labels] = self._data_manager._labeled_2d(first,
                                                                           first_labels)
                    [second, second_labels] = self._data_manager._labeled_2d(second,
                                                                             second_labels)
                    first = self._stat_reshape(first, subjects, repetitions, features)
                    second = self._stat_reshape(second, subjects, repetitions, features)
        else:
            repetitions = size[1]
        first = np.reshape(first, (subjects, repetitions, features))
        second = np.reshape(second, (subjects, repetitions, features))
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
        The compute_scores_statistics method computes the Wilcoxon p-value and the
        Cohen's d effect size on the features between two arrays.

        :param first_data:  it is the first 1D-array of scores
        :param second_data: it is the second 1D-array of scores

        :return: the pvalue and Cohen's d value, in order
        """
        [stat, pvalue] = ranksums(np.squeeze(first_data), np.squeeze(second_data))
        d = self.compute_cohen_d(np.squeeze(first_data), np.squeeze(second_data))
        return pvalue, d

    def statistics_settings(self, first_data, second_data):
        """
        The statistics_settings method set the data which has to be used for
        some statistical analysis.

        :param first_data:  it is a data matrix
        :param second_data: it is another data matrix

        :return: the two data matrices
        """
        first_data = np.array(first_data)
        second_data = np.array(second_data)
        return first_data, second_data
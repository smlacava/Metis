import numpy as np
from data_manager import *

class utils():
    def __init__(self):
        self._data_manager = data_manager()


    def _to3D(self, data, subjects, repetitions, features):
        """
        The _to3D methos is used to reshape a 2D data matrix into a 3D data matrix (FOR INTERNAL USE ONLY).

        :param data:        it is the 2D ([subjects*repetitions]*features) data matrix
        :param subjects:    it is the number of subjects
        :param repetitions: it is the number of repetitions
        :param features:    it is the number of features

        :return:            the 3D (subjects*repetitions*features) data matrix
        """
        data = np.array(data)
        if len(np.shape(data)) == 2:
            print('Data reshaping from ' + str(np.shape(data)) + ' to ', end="")
            print((subjects, repetitions, features))
            aux_data = np.zeros((subjects, repetitions, features))
            for s in range(subjects):
                for r in range(repetitions):
                    aux_data[s, r, :] = data[(s * repetitions) + r, 0:features]
            return aux_data
        else:
            return data


    def _dimensions(self, data, labels):
        """
        The _dimensions method returns the number of subjects, repetitions and features related to the data matrix (FOR
        INTERNAL USE ONLY).

        :param data:   is the data matrix
        :param labels: is the list of labels

        :return:       the number of dimensions of the data matrix, the number of subjects, the number of repetitions
                       ad the number of features
        """
        size = np.shape(data)
        L = len(size)
        subjects = size[0]
        features = size[L - 1]
        if L == 2:
            repetitions = self._repetitions_check(data, labels)
        else:
            repetitions = size[1]
        subjects = int(subjects / repetitions)

        return L, subjects, repetitions, features


    def _repetitions_check(self, data, labels):
        """
        The _repetitions_check method is used to check if the number of repetitions is equal all the subjects, and
        eventually compute that number (FOR INTERNAL USE ONLY).

        :param data:   it is the 2D data matrix
        :param labels: it is the array or the list representing the labels

        :return:       the number of repetitions, if it is equal for all the subjects, 1 otherwise
        """
        names = np.unique(labels)
        repetitions = 0
        for name in names:
            count = 0
            for lbl in labels:
                if name == lbl:
                    count += 1
            if count != repetitions and repetitions != 0:
                return 1
            repetitions = count
        return repetitions


    def _same_format_3D(self, first, second, first_labels, second_labels):
        """
        The _same_format_3D method manages two data matrices in order to return them in the same 3D
        (subjects*repetitions*features) format (FOR INTERNAL USE ONLY).

        :param first:         it is the first 2D (samples*features) or 3D (subjects*repetitions*features) data matrix
        :param second:        it is the second 2D (samples*features) or 3D (subjects*repetitions*features) data matrix
        :param first_labels:  it is the list of labels related to the samples of the first data matrix (used in the 2D
                              case)
        :param second_labels: it is the list of labels related to the samples of the second data matrix (used in the 2D
                              case)
        :return:              the two 3D (subjects*repetitions*features) data matrices
        """
        first_L, first_subjects, first_repetitions, first_features = self._dimensions(first, first_labels)
        second_L, second_subjects, second_repetitions, second_features = self._dimensions(second, second_labels)
        if first_L == 2 or second_L == 2:
            first_repetitions = 1
            if not (first_labels is None or second_labels is None):
                first_repetitions = self._repetitions_check(first, first_labels)
                if first_repetitions != -1 and self._repetitions_check(second, second_labels) == first_repetitions:
                    [first, first_labels] = self._data_manager._labeled_2d(first, first_labels)
                    [second, second_labels] = self._data_manager._labeled_2d(second, second_labels)
                    first = self._to3D(first, first_subjects, first_repetitions, first_features)
                    second = self._to3D(second, second_subjects, second_repetitions, second_features)
        first = np.reshape(first, (first_subjects, first_repetitions, first_features))
        second = np.reshape(second, (second_subjects, second_repetitions, second_features))
        return first, second
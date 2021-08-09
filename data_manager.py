import numpy as np


class data_manager():
    """
    The data_manager class allows to manage the analyzed data in order to be usable by the toolbox, automatically
    managing the differences between 3D (subjects*repetitions*features) unlabeled data and 2D (samples*features) labeled
    data, in which the labels identify to which subject each sample belongs.

    Methods:
        data_management: provides the managed 2D (samples*features) data matrix and the related list of labels, from the
                         3D (subjects*repetitions*features) or 2D (samples*features) raw data, and the list of labels in
                         the second case
    """


    def data_management(self, data, labels=None):
        """
        The data_management method manages the input data matrix in order to be used for the following analysis.

        :param data:   is the 2D (subjects*features) or 3D (subjects*repetitions*features) data matrix
        :param labels: is the list of labels associated to the subjects (used in the 2D case)

        :return:       the managed 2D data matrix and the list of labels
        """
        if isinstance(data, list):
            data = np.array(data)
        dim = len(np.shape(data))
        if labels is None and dim == 3:
            data, labels = self._unlabeled_3d(data)
        elif not (labels is None) and dim == 2:
            data, labels = self._labeled_2d(data, labels)
        return data, labels


    def _unlabeled_3d(self, data):
        """
        The _unlabeled_3d method manages the 3D input data matrix in order to be used for the following analysis (FOR
        INTERNAL USE ONLY).

        :param data: is the 3D (subjects*repetitions*features) data matrix

        :return:     the managed 2D data matrix and the list of labels
        """
        [n_subjects, n_repetitions, n_features] = data.shape
        data = np.reshape(np.transpose(np.double(data), (1, 0, 2)), (n_subjects * n_repetitions, n_features))
        labels = np.array([sub for sub in range(n_subjects) for rep in range(n_repetitions)])
        return data, labels


    def _labeled_2d(self, data, labels):
        """
        The data_management method manages the 2D input data matrix in order to be used for the following analysis.

        :param data:   is the 2D (subjects*features) data matrix
        :param labels: is the list of labels associated to the subjects

        :return:       the managed 2D data matrix and the list of labels
        """
        ind = np.argsort(labels)
        data = data.take(ind, axis=0)
        labels = np.array(labels).take(ind, axis=0)
        return data, labels
import numpy as np


class data_manager():
    def data_management(self, data, labels=None):
        if isinstance(data, list):
            data = np.array(data)
        dim = len(np.shape(data))
        if labels is None and dim == 3:
            data, labels = self._unlabeled_3d(data)
        elif not (labels is None) and dim == 2:
            data, labels = self._labeled_2d(data, labels)
        return data, labels

    def _unlabeled_3d(self, data):
        [n_subjects, n_repetitions, n_features] = data.shape
        data = np.reshape(np.transpose(np.double(data), (1, 0, 2)), (n_subjects * n_repetitions, n_features))
        labels = np.array([sub for sub in range(n_subjects) for rep in range(n_repetitions)])
        return data, labels

    def _labeled_2d(self, data, labels):
        ind = np.argsort(labels)
        data = data.take(ind, axis=0)
        labels = np.array(labels).take(ind, axis=0)
        return data, labels
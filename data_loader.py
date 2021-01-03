from scipy.io import loadmat
from pathlib import Path
import numpy as np

class data_loader():
    def load_data(self, data_file):
        """
        The load_data method allows to load a matrix from a file (.mat).

        :param data_file: it is the name of the file (with its path) containing the matrix
        :return: the loaded matrix
        """
        if '.mat' in data_file:
            data = self._load_mat(data_file)
        return np.squeeze(np.array(data)).tolist()


    def _load_mat(self, data_file):
        """
        The _load_mat method loads a matrix from a .mat file (FOR INTERNAL USE ONLY).

        :param data_file: it is the name of the file (with its path) containing the matrix
        :return: the loaded matrix
        """
        data = loadmat(r'%s' % data_file)
        for k in data.keys():
            if not ('__' in k):
                data = data[k]
                for i in range(1, 5):
                    if not (isinstance(data, np.ndarray)) or data.shape == (1, 1) or data.shape == (1,) or data.shape == ():
                        data = data[0]
                    else:
                        return data
import numpy as np
from sklearn.decomposition import PCA, FastICA


class features_selector():
    def columns_selection(self, data, indexes):
        """
        The columns_selection method allows to select a subset of features from a data matrix, by using the
        corresponding list of indexes.

        :param data: it is the 2D (subjects*features) or 3D (subjects*repetitions*features) data matrix
        :param indexes: it is the list of indexes representing the selected features

        :return: the data matrix considenting the only selected features
        """
        data = np.array(data)
        size = np.shape(data)
        if len(size) == 3:
            return data[0:size[0], 0:size[1], indexes]
        else:
            return data[0:size[0], indexes]


    def pca_selection(self, data, n_features):
        """
        The pca_selection method allows to select a subset of features from a data matrix, by applying the Principal
        Component Analysis.

        :param data: it is the 2D (subjects*features) data matrix
        :param n_features: if greater or equal to 1, it is the number of principal components to extract (the minimum
                           contribution otherwise, in this case the number of selected features will be the minimum
                           one for which the wished contribution is reached)

        :return: the data matrix considenting the only selected features
        """
        if n_features >= 1:
            pca = PCA(n_components=n_features)
        else:
            pca = PCA(n_components=n_features, svd_solver='full')
        return pca.fit_transform(np.array(data))


    def ica_selection(self, data, n_features):
        """
        The ica_selection method allows to select a subset of features from a data matrix, by applying the Fast
        Independent Component Analysis.

        :param data: it is the 2D (subjects*features) data matrix
        :param n_features: if greater or equal to 1, it is the number of independent components to extract

        :return: the data matrix considenting the only selected features
        """
        ica = FastICA(n_components=n_features)
        return ica.fit_transform(np.array(data))


    def select_features(self, algorithm, data, features):
        """
        The select_features method allows to select a subset of features from a data matrix, by applying aa chosen
        selection algorithm.

        :param algorithm: it is the selection algorithm, between 'columns' (for columns selection), 'pca' (for Principal
                           Component Analysis) and 'ica' (for Independent Component Analysis)
        :param data: it is the 2D (subjects*features) data matrix (in case of columns selection, a 3D
                            (subjects*repetitions*features) data matrix is also allowed)
        :param n_features: an integer representing the number of features to extract (a number lower than 1 representing
                           the contribution is also allowed in the 'pca' case, and  in this case the number of selected
                           features will be the minimum one for which the wished contribution is reached)

        :return: the data matrix considenting the only selected features
        """
        selection_algorithms = {'columns': self.columns_selection,
                                'pca': self.pca_selection,
                                'ica': self.ica_selection}
        return selection_algorithms[algorithm](data, features)
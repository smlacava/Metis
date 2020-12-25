import numpy as np
from sklearn.decomposition import PCA, FastICA


class features_selector():
    def columns_selection(self, data, indexes):
        data = np.array(data)
        size = np.shape(data)
        if len(size) == 3:
            return data[0:size[0], 0:size[1], indexes]
        else:
            return data[0:size[0], indexes]

    def pca_selection(self, data, n_features):
        if n_features >= 1:
            pca = PCA(n_components=n_features)
        else:
            pca = PCA(n_components=n_features, svd_solver='full')
        return pca.fit_transform(np.array(data))

    def ica_selection(self, data, n_features):
        ica = FastICA(n_components=n_features)
        return ica.fit_transform(np.array(data))

    def select_features(self, algorithm, data, features):
        selection_algorithms = {'columns': self.columns_selection,
                                'pca': self.pca_selection,
                                'ica': self.ica_selection}
        return selection_algorithms[algorithm](data, features)
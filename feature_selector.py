import numpy as np
from sklearn.decomposition import PCA, FastICA
from scipy import linalg

class features_selector():
    """
    The features_selector class provides different features selection and features extraction methods.
    
    Methods:
        columns_selection: selects some features from the initial dataset by specifying their index
        pca_selection:     extracts a specific number of features from the dataset through the principal component
                           analysis, or the number of features necessary to reach the minimum specified variance
                           contribute
        ica_selection:     extracts a specific number of features from the dataset through the independent component
                           analysis
    """


    def columns_selection(self, data, indexes):
        """
        The columns_selection method allows to select a subset of features from a data matrix, by using the
        corresponding list of indexes.

        :param data:    is the 2D (subjects*features) or 3D (subjects*repetitions*features) data matrix
        :param indexes: is the list of indexes representing the selected features

        :return:        the data matrix considenting the only selected features
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

        :param data:       is the 2D (subjects*features) data matrix
        :param n_features: if greater or equal to 1, it is the number of principal components to extract (the minimum
                           contribution otherwise, in this case the number of selected features will be the minimum
                           one for which the wished contribution is reached)

        :return:           the data matrix considenting the only selected features
        """
        aux_data = self._center(data)
        cov = np.cov(aux_data.T)/aux_data.shape[0]
        v, w = np.linalg.eig(cov)
        idx = v.argsort()[::-1]
        w = w[:, idx]
        tot_v = sum(v)
        if n_features < 1:
            explained = [i*100/tot_v for i in v]
            cumulative = np.cumsum(explained)
            n_features = len(cumulative[cumulative < n_features*100])+1
        return aux_data.dot(w[:, :n_features])


    def ica_selection(self, data, n_features):
        """
        The ica_selection method allows to select a subset of features from a data matrix, by applying the Fast
        Independent Component Analysis.

        :param data:       is the 2D (subjects*features) data matrix
        :param n_features: if greater or equal to 1, it is the number of independent components to extract

        :return:           the data matrix considenting the only selected features
        """
        ica = FastICA(n_components=n_features)
        print(self.fastIca(data, n_features)[0, :])
        print(ica.fit_transform(np.array(data))[0, :])
        return ica.fit_transform(np.array(data))


    def select_features(self, algorithm, data, features):
        """
        The select_features method allows to select a subset of features from a data matrix, by applying aa chosen
        selection algorithm.

        :param algorithm:  is the selection algorithm, between 'columns' (for columns selection), 'pca' (for Principal
                           Component Analysis) and 'ica' (for Independent Component Analysis)
        :param data:       is the 2D (subjects*features) data matrix (in case of columns selection, a 3D
                           (subjects*repetitions*features) data matrix is also allowed)
        :param n_features: an integer representing the number of features to extract (a number lower than 1 representing
                           the contribution is also allowed in the 'pca' case, and  in this case the number of selected
                           features will be the minimum one for which the wished contribution is reached)

        :return:           the data matrix considenting the only selected features
        """
        selection_algorithms = {'columns': self.columns_selection,
                                'pca': self.pca_selection,
                                'ica': self.ica_selection}
        return selection_algorithms[algorithm](data, features)


    def fastIca(self, data, n_features):
        """
        The fastICA method executes a features extraction, through the FastICA algorithm which extimates a certain
        number of independent components chosen by the user (the symmetric orthogonalization as orthogonalization
        method, and the logarithm of the hyerbolic cosine is used as negentropy approximation).

        :param data:       is the data matrix from which the features have to be extracted
        :param n_features: is the number of features which have to be extracted

        :return:           the transformed data matrix
        """
        max_iter = 200
        tol = 1e-4

        data = self._center(data).T
        n_samples, p = data.shape
        X, K = self._whitening(data, n_features, p)
        W = self._initial_W(X, n_features)
        for ii in range(max_iter):
            g, dg = self._logcosh(X, W)
            W = (np.dot(g, X.T)/p)-dg[:, np.newaxis]*W
            s, u = linalg.eigh(np.dot(W, W.T))
            aux_W = np.linalg.multi_dot([u*(1./np.sqrt(s)), u.T, W])
            lim = max(abs(abs(np.diag(np.dot(aux_W, W.T)))-1))
            W = aux_W
            if lim < tol:
                break

        S = np.linalg.multi_dot([W, K, data]).T
        return S


    def _logcosh(self, X, W):
        """
        The _logcosh method returns a the value of the G function, used in the approximation of the negative entropy
        (negentropy) as logarithm of the hyperbolic cosine function, which is good as general-purpose approximation
        (FOR INTERNAL USE ONLY).

        :param X: is the data preprocessed by PCA
        :param W: is the current components matrix

        :return:  the negentropy function values and its derivative values
        """
        x = np.dot(W, X)
        G = np.tanh(x, x)
        dG = np.zeros(x.shape[0])
        for idx, dG_idx in enumerate(G):
            dG[idx] = (1 - dG_idx ** 2).mean()
        return G, dG


    def _center(self, data):
        """
        The _center method centers the data on zero (FOR INTERNAL USE ONLY).

        :param data: is the data matrix

        :return:     the centered data matrix
        """
        data = np.array(data)
        mean = data.mean(axis=0)
        data -= mean
        return data


    def _whitening(self, data, n_components, n_features):
        """
        The _whitening method whitens the input data (FOR INTERNAL USE ONLY).

        :param data:         is the input data matrix
        :param n_components: is the number of components which have to be extracted
        :param n_features:   is the number of features of the input data matrix

        :return:             the whitened data matrix
        """
        u, d, _ = linalg.svd(data, full_matrices=False, check_finite=False)
        K = (u/d).T[:n_components]
        X = np.dot(K, data)
        X *= np.sqrt(n_features)
        return X, K


    def _initial_W(self, X, n_components):
        """
        The _initial_W method provides the initial random values for the components matrix (FOR INTERNAL USE ONLY).

        :param X:            is the preprocessed data matrix
        :param n_components: is the number of independent components which have to be extracted

        :return:             the initial components matrix
        """
        random_state = np.random.mtrand._rand
        w_init = np.asarray(random_state.normal(size=(n_components, n_components)), dtype=X.dtype)
        s, u = linalg.eigh(np.dot(w_init, w_init.T))
        W = np.linalg.multi_dot([u*(1./np.sqrt(s)), u.T, w_init])
        return W
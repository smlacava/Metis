import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import random
from distances import *

class clustering():
    """
    The clustering class provides the methods for executing some cluster analysis and the related evaluations, such as
    the purity and the silhouette analysis.

    Attributes:
        clusters is the default number of clusters

    Methods:
        set_clusters:        allows to set a default number of clusters
        compute_clusters:    computes the clustering, currently through the K-Means algorithm, and provides the labels
                             related to data
        clustering_plot:     plots the data in each pair of features, highlighting them through a different color for
                             any cluster resulting from a previous clustering
        purity:              evaluates a previously computed clustering in terms of purity
        silhouette_score:    evaluates a previously computed clustering in terms of silhouette score
        cluster_analysis:    computes the clustering and then plots the results
        cluster_performance: computes the clustering and then evaluates it it terms of purity
        silhouette_analysis: computes the clustering and evaluates it in terms of silhouette for different numbers of
                             clusters, plotting the silhouette of each in order to choose the optimal number of clusters
    """


    def __init__(self, clusters=2):
        """
        The __init__ method is the initializer, which optionally allows to set the number of clusters.

        :param clusters: is the number of clusters (2 by default)
        """
        self.set_clusters(clusters)


    def set_clusters(self, clusters):
        """
        The set_clusters mehod allows to set the number of clusters.

        :param clusters: is the number of clusters
        """
        if not(clusters is None):
            self.clusters = clusters


    def compute_clusters(self, data, clusters=None):
        """
        The compute_clusters method allows to find the clusters to which the samples belong, through the KMeans
        algorithm.

        :param data:     is the 2D (samples*features) data matrix
        :param clusters: is the number of cluster to evaluate, or None to use the previously inserted clusters (None by
                         default)

        :return:         the labels identify the clusters to which the subjects belong
        """
        self.set_clusters(clusters)
        return self._KMeans(data, self.clusters)


    def clustering_plot(self, data, y_pred=None, view=True, save=False, outPath=None, group_name=""):
        """
        The clustering_plot method generates the clustering plots for each pair of feature, as well as the single
        features, eventually saving the resulting figure as clustering.png.

        :param data:       is the 2D (samples*features) data matrix
        :param y_pred:     is the array containing the cluster for each subject, or None to consider each as belonging
                           to the same subject (None by default)
        :param view:       has to be True in order to show the resulting plots, False otherwise (True by default)
        :param save:       has to be True in order to save the resulting figure as clustering.png, False othersise
                           (False by default)
        :param outPath:    is the path (directory) in which the resulting image has to be saved (None by default)
        :param group_name: is the name of the analyzed group (the image will be eventually saved as "nameclustering.png"
                           where "name" is the group_name value, "" by default)
        """
        features = np.shape(data)[1]
        count = 1
        if y_pred is None:
            y_pred = np.ones(shape=(np.shape(data)[0],1))
        for f1 in range(features):
            for f2 in range(features):
                plt.subplot(features, features, count)
                plt.scatter(data[:, f1], data[:, f2], 2, c=y_pred)
                if f2 == 0:
                    m = np.min(data[:, f2])
                    plt.yticks([m+(np.max(data[:, f2])-m)/2], [str(f1+1)])
                    plt.tick_params(axis='both', length=0, labelsize=13)
                else:
                    plt.yticks([])

                if f1 == 0:
                    plt.title(str(f2+1))
                plt.xticks([])
                count += 1
        if save is True:
            if not (outPath is None):
                plt.savefig(str(Path(outPath) / (group_name + "clustering.png")))
            else:
                plt.savefig("clustering.png")
        if view is True:
            plt.show()


    def cluster_analysis(self, data, clusters=None, view=True, save=False, outPath=None, group_name=""):
        """
        The clustering_analysis method performs the whole clustering analysis, from the clustering searching to the
        final plots.

        :param data:       is the 2D (samples*features) data matrix
        :param clusters:   is the number of cluster to evaluate, or None to use the previously inserted clusters
                           (None by default)
        :param view:       has to be True in order to show the resulting plots, False otherwise (True by default)
        :param save:       has to be True in order to save the resulting figure as clustering.png, False othersise
                           (False by default)
        :param outPath:    is the directory in which eventually store the resulting figure (None by default)
        :param group_name: is the name of the group related to the data matrix (optional)
        """
        y_pred = self.compute_clusters(data, clusters)
        self.clustering_plot(data, y_pred, view, save, outPath, group_name)


    def cluster_performance(self, data, labels, clusters=2):
        """
        The cluster_performance evaluate the performance of the KMeans algorithm in terms of purity.

        :param data:     is the 2D (samples*features) data matrix
        :param labels:   is the list of real labels
        :param clusters: is the number of clusters to evaluate (2 by default)

        :return:         the purity value
        """
        y_pred = self.compute_clusters(data, clusters)
        return self.purity(labels, y_pred)


    def purity(self, labels, y_pred):
        """
        The purity method compute the purity related to a previously computed clustering.

        :param labels: is the list of real labels
        :param y_pred: is the list of predicted labels

        :return: the purity value
        """
        accuracy = 0
        L = np.max(np.shape(y_pred))
        unique_labels = np.unique(labels)
        unique_y = np.unique(y_pred)
        purity = 0
        for lbl in unique_labels:
            predicted = dict((el, 0) for el in unique_y)
            for idx in range(L):
                if labels[idx] == lbl:
                    predicted[y_pred[idx]] += 1
            purity += max(predicted.values())
        return purity / L


    def _centroids_initialization(self, data, clusters):
        """
        The _centroids_initialization select randomly a number of samples (defined by clusters) from the data matrix in
        order to be used as initial centroids (FOR INTERNAL USE ONLY).

        :param data:     is the data matrix
        :param clusters: is the number of clusters

        :return:         the initial clusters
        """
        centroids = data.copy()
        np.random.shuffle(centroids)
        return centroids[:clusters]


    def _centroid_assignment(self, data, centroids):
        """
        The _centroid_assignment method assigns each data sample to the related cluster, with respect to the its
        distance with the centroids (FOR INTERNAL USE ONLY).

        :param data:      is the data matrix
        :param centroids: is the matrix containing the coordinates (features values) of each centroid

        :return:          the index array identifying to which cluster each sample belongs
        """
        distances = self._distance(data, centroids)
        return np.argmin(distances, axis=0)


    def _distance(self, data, centroids):
        """
        The _distance computes the distance of each sample to each centroid (FOR INTERNAL USE ONLY).

        :param data:      is the data matrix
        :param centroids: is the matrix containing the coordinates (features values) of each centroid

        :return:          the distances matrix
        """
        return np.sqrt(((data - centroids[:, np.newaxis]) ** 2).sum(axis=2)) #togliere sqrt?


    def _compute_se(self, data, centroids, assigned, n_samples):
        """
        The _compute_se method computes the squared error related to the actual clustering (FOR INTERNAL USE ONLY).

        :param data:      is the data matrix
        :param centroids: is the matrix containing the coordinates (features values) of each centroid
        :param assigned:  is the index array identifying to which cluster each sample belongs
        :param n_samples: is the number of samples inside the data matrix

        :return:          the squared error value related to the current clustering
        """
        se = 0
        for idx in range(n_samples):
            se += np.sqrt((data[idx, :]-centroids[assigned[idx], :])**2).sum()
        return se/n_samples


    def _centroid_computation(self, data, assigned, centroids):
        """
        The _centroid_computation method computes the new coordinates (feature values) for each centroid with respect
        to the current cluster (FOR INTERNAL USE ONLY).

        :param data:      is the data matrix
        :param assigned:  is the index array identifying to which cluster each sample belongs
        :param centroids: is the matrix containing the coordinates (features values) of each centroid

        :return:          the matrix representing the new centroids
        """
        return np.array([data[assigned == k].mean(axis=0) for k in range(centroids.shape[0])])


    def _KMeans(self, data, clusters, iterations=100):
        """
        The _KMeans method executes the clustering on a dataset through the K-Means clustering algorithm (FOR INTERNAL
        USE ONLY).

        :param data:       is the data matrix
        :param clusters:   is the number of clusters to find
        :param iterations: is the maximum number of iterations the algorithm (100 by default, however the algorithm
                           automatically stops as soon as a convergence in the squared error is found)

        :return:           the array of labels identifying to which cluster each sample belongs
        """
        (n_samples, n_features) = np.shape(data)
        centroids = self._centroids_initialization(data, clusters)
        assigned = self._centroid_assignment(data, centroids)
        centroids = self._centroid_computation(data, assigned, centroids)
        se = self._compute_se(data, centroids, assigned, n_samples)
        for i in range(iterations):
            assigned = self._centroid_assignment(data, centroids)
            centroids = self._centroid_computation(data, assigned, centroids)
            aux_se = self._compute_se(data, centroids, assigned, n_samples)
            if aux_se == se:
                break
            else:
                se = aux_se
        return assigned


    def silhouette_score(self, data, assigned):
        """
        The silhouette_score method computes the silhouette score related to the clustering.

        :param data:     is the data matrix
        :param assigned: is the array of labels identifying to which cluster each sample belongs

        :return:         the silhouette score
        """
        s = 0
        clusters = np.unique(assigned)
        L = np.max(np.shape(assigned))
        clusters_dict = dict()
        for c in clusters:
            clusters_dict[clusters[c]] = sum(assigned == clusters[c])

        for idx in range(L):
            if clusters_dict[assigned[idx]] == 1:
                continue
            a = 0
            b = float('inf')
            for idx2 in range(L):
                if idx == idx2:
                    continue
                elif assigned[idx] == assigned[idx2]:
                    a += np.linalg.norm(data[idx, :] - data[idx2, :])
            a = a/(clusters_dict[assigned[idx]]-1)
            for c in clusters:
                if c == assigned[idx]:
                    continue
                else:
                    aux_b = 0
                    for idx2 in range(L):
                        if assigned[idx2] == c:
                            aux_b += np.linalg.norm(data[idx, :] - data[idx2, :])
                    b = np.minimum(b, aux_b/clusters_dict[c])
            s += ((b-a)/np.max([b, a]))
        return s/L


    def silhouette_analysis(self, data, max_clusters=10, min_clusters=2, repetitions=10, view=True, save=False,
                            outPath=None, group_name=""):
        """
        The silhouette_analysis method computes the clustering and evaluates it in terms of silhouette a range of
        numbers of clusters, plotting the silhouette of each in order to choose the optimal number of clusters (i.e. the
        one which provides the highest silhouette value).

        :param data:         is the data matrix
        :param max_clusters: is the maximum number of clusters to analyze (10 by default)
        :param min_clusters: is the minimum number of clusters to analyze (2 by default)
        :param repetitions:  is the number of repetitions for each number of clusters, in order to evaluate a mean
                             silhouette score
        :param view:         has to be True in order to show the resulting plots, False otherwise (True by default)
        :param save:         has to be True in order to save the resulting figure as clustering.png, False othersise
                             (False by default)
        :param outPath:      is the path (directory) in which the resulting image has to be saved (None by default)
        :param group_name:   is the name of the analyzed group (the image will be eventually saved as
                             "namesilhouette.png" where "name" is the group_name value, "" by default)
        :return:
        """
        scores = np.zeros(shape=(max_clusters-min_clusters+1,))
        clusters = range(min_clusters, max_clusters+1)
        for cl in clusters:
            for r in range(repetitions):
                scores[cl-min_clusters] += self.silhouette_score(data, self._KMeans(data, cl))
            scores[cl-min_clusters] = scores[cl-min_clusters]/repetitions
            print(str(cl) + " clusters: " + str(scores[cl-min_clusters]))
        if save is False and view is False:
            return scores
        plt.plot(clusters, scores)
        plt.xlabel('Clusters')
        plt.ylabel('Silhouette scores')
        if save is True:
            if not (outPath is None):
                plt.savefig(str(Path(outPath) / (group_name + "silhouette.png")))
            else:
                plt.savefig("silhouette.png")
        if view is True:
            plt.show()
        return scores


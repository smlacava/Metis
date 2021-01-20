import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from pathlib import Path

class clustering():
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
        return KMeans(self.clusters, random_state=170).fit_predict(data)


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


    def cluster_performance(self, data, labels):
        """
        The cluster_performance evaluate the performance of the KMeans algorithm in terms of accuracy, using 2 clusters.

        :param data:     is the 2D (samples*features) data matrix
        :param labels:   is the list of real labels.
        :return:         the overall accuracy
        """
        y_pred = self.compute_clusters(data, 2)
        accuracy = 0
        L = np.max(np.shape(y_pred))
        for idx in range(L):
            accuracy += int(y_pred[idx]==labels[idx])
        accuracy = accuracy/L
        if accuracy < 0.5:
            accuracy = 1-accuracy
        return accuracy
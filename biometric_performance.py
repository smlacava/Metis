import numpy as np


class biometric_performance():
    """
    The biometric_performance class provides the methods for computing the similarity scores, the genuine score
    distribution, the impostor score distribution, the False Acceptance Rate (FAR), the False Rejection Rate (FRR), the
    Correct Acceptance Rate (CAR), the Correct Rejection Rate (CRR), and the Equal Error Rate (EER).

    Methods:
        compute_scores:               computes the similarity scores from the raw data, with respect to a chosen
                                      distance metric
        genuines_and_impostors:       computes the genuine and the impostor score distributions from the similarity
                                      scores
        compute_FAR:                  computes the FAR from the impostor score distribution
        compute_FRR:                  computes the FRR from the genuine score distribution
        compute_CRR:                  computes the CRR from the impostor score distribution
        compute_CAR:                  computes the CAR from the genuine score distribution
        compute_EER:                  computes the EER from the FAR and the FRR
        compute_performance_analysis: computes FAR, FRR, CRR, CAR, and EER from the genuine and impostor score
                                      distributions
        compute_analysis:             computes FAR, FRR, CRR, CAR, and EER from the raw data

    """


    def compute_FAR(self, impostor_score, thresholds=0.01):
        """
        The compute_FAR method is used to compute the False Acceptance Rate (FAR).

        :param impostor_score: is the 1D-array, representing the impostor scores, used to compute the FAR array
        :param thresholds:     is the length of each step which has to be used in evaluating the different thresholds
                               for which values compute the FAR, or the array representing all the considered thrsholds
                               (0.01 by default)

        :return:               the 1D-array representing the FAR computed on each threshold value between 0 and 1
        """
        print('Computing FAR')
        condition = lambda score, thr: score > thr
        return self._F_performance(np.squeeze(np.array(impostor_score)), thresholds, condition)


    def compute_FRR(self, genuine_score, thresholds=0.01):
        """
        The compute_FRR method is used to compute the False Rejection Rate (FRR).

        :param genuine_score:  is the 1D-array, representing the genuine scores, used to compute the FRR array
        :param thresholds:     is the length of each step which has to be used in evaluating the different thresholds
                               for which values compute the FAR, or the array representing all the considered thrsholds
                               (0.01 by default)

        :return:               the 1D-array representing the FRR computed on each threshold value between 0 and 1
        """
        print('Computing FRR')
        condition = lambda score, thr: score <= thr
        return self._F_performance(genuine_score, thresholds, condition)


    def _F_performance(self, score, thresholds, condition):
        """
        The _F_performance method is used to compute the False Rejection Rate or the
        False Acceptance Rate (FOR INTERNAL USE ONLY).

        :param score:          is the 1D-array, representing the scores on which compute the FAR or the FRR
        :param thresholds:     is the length of each step which has to be used in evaluating the different thresholds
                               for which values compute the FAR and the FRR, or the array representing all the
                               considered thrsholds
        :param condition:      it is the function which compares a score value with a threshold value (the FAR
                               considers score > threshold, while the FRR considers score <= threshold)

        :return:               the 1D-array representing the FRR computed on each threshold value between 0 and 1
        """
        if type(thresholds) is float:
            thresholds = self._compute_thresholds(thresholds)
        F = np.zeros(shape=(1, len(thresholds)))
        impostors = 0
        L = len(score)
        for count, thr in enumerate(thresholds):
            N = 0
            for idx in range(0, L):
                N += condition(score[idx], thr)
            F[0, count] = N / L
        return F[0]


    def _compute_thresholds(self, thresholds):
        """
        The _compute_thresholds method computes the list of thresholds to use in computing FAR and FRR (FOR INTERNAL USE
        ONLY).

        :param thresholds: is a float number representing the step between two threshold values

        :return:           the list of thresholds
        """
        thr = thresholds
        limit = int(1 / thresholds)
        thresholds = [x * thr for x in range(limit)]
        thresholds.append(1)
        return thresholds


    def confusion_matrix(self, FAR, FRR):
        """
        The confusion_matrix method provides a the confusion matrix as a 2D-matrix ([[CAR, FRR], [FAR, CRR]]), computed
        on the threshold in which the Equal Error Rate (EER) is computed.

        :param FAR: is the 1D-array representing the FAR on each threshold value
        :param FRR: is the 1D-array representing the FRR on each threshold value

        :return:    the confusion matrix ([[CAR, FRR], [FAR, CRR]])
        """
        distance = abs(FAR - FRR)
        min_distance = min(distance)
        idx = np.where(distance == min_distance)[0][0]
        return [[1-float(FRR[idx]), float(FRR[idx])], [float(FAR[idx]), 1-float(FAR[idx])]]


    def compute_EER(self, FAR, FRR):
        """
        The compute_EER method computes the Equal Error Rate (EER) through the False Acceptance Rate (FAR) and the
        False Rejection Rate (FRR).

        :param FAR: is the 1D-array representing the FAR on each threshold value
        :param FRR: is the 1D-array representing the FRR on each threshold value

        :return:    a value representing the EER
        """
        print('Computing EER')
        distance = abs(FAR - FRR)
        min_distance = min(distance)
        idx = np.where(distance == min_distance)
        return np.mean((FAR[idx] + FRR[idx]) / 2)


    def compute_AUC(self, FAR, CAR):
        """
        The compute_AUC method computes the Area Under the Curve (AUC) value from the False Acceptance Rate (FAR) and
        the Correct Acceptance Rate (CAR).

        :param FAR: is the 1D-array representing the FAR on each threshold value
        :param CAR: is the 1D-array representing the CARR on each threshold value

        :return:    a value representing the AUC
        """
        print('Computing AUC')
        return abs(np.trapz(CAR, FAR))


    def compute_CRR(self, FAR):
        """
        The compute_CRR method computes the Correct Rejection Rate (CRR) from the False Acceptance Rate (FAR).

        :param FAR: is the 1D-array representing the FAR on each threshold value

        :return: the 1D-array representing the CRR on each threshold value
        """
        print('Computing CRR')
        return (np.ones((1, len(FAR))) - FAR)[0]


    def compute_CAR(self, FRR):
        """
        The compute_CAR method computes the Correct Acceptance Rate (CAR) from the False Rejection Rate (FRR).

        :param FRR: is the 1D-array representing the FRR on each threshold value

        :return:    the 1D-array representing the CAR on each threshold value
        """
        print('Computing CAR')
        return (np.ones((1, len(FRR))) - FRR)[0]


    def compute_performance_analysis(self, G, I, thresholds=0.01):
        """
        The compute_performance_analysis method computes the False Acceptance Rate (FAR), the False Rejection Rate
        (FRR), the Correct Rejection Rate (CRR), the Correct Acceptance Rate (CAR) for each threshold value, the Equal
        Error Rate (EER) and the Area Under the Curve (AUC) on a genuine scores array and an impostor scores array.

        :param G:          is the 1D-array representing the genuine scores
        :param I:          is the 1D-array representing the impostor scores
        :param thresholds: is the length of each step which has to be used in evaluating the different thresholds for
                           which values compute the FAR, or the array representing all the considered thrsholds (0.01 by
                           default)

        :return:           the FAR, FRR, CRR and CAR 1D-arrays, the EER value and the AUC value
        """
        FAR = self.compute_FAR(I, thresholds)
        FRR = self.compute_FRR(G, thresholds)
        CRR = self.compute_CRR(FAR)
        CAR = self.compute_CAR(FRR)
        EER = self.compute_EER(FAR, FRR)
        AUC = self.compute_AUC(FAR, CAR)
        return FAR, FRR, CRR, CAR, EER, AUC


    def compute_analysis(self, data, labels, distance, thresholds=None):
        """
        The compute_analysis method computes the False Acceptance Rate (FAR), the False Rejection Rate (FRR), the
        Correct Rejection Rate (CRR), the Correct Acceptance Rate (CAR) for each threshold value, the Equal Error Rate
        (EER) and the Area Under the Curve on a data matrix.

        :param data:       is the 3D (subjects*repetitions*features) data matrix (None by default, the previous data
                           will be used if None)
        :param labels:     is the list of labels associated to the subjects, in the samme order as the scores
        :param distance:   is the function (or one string between 'euclidean', 'manhattan', 'mahalanobis' and
                           'minkowski', representing the homonymous distances) which is used in order to evaluate the
                           distance in the genuine and impostor scores computation (optional, euclidean distance by
                           default)
        :param thresholds: is the length of each step which has to be used in evaluating the different thresholds for
                           which values compute the FAR, or the array representing all the considered thrsholds (None by
                           default)

        :return:           the FAR, FRR, CRR and CAR 1D-arrays, the EER value and the AUC value
        """
        print('  Computing genuine and impostor scores')
        scores = self.compute_scores(data, distance)
        if thresholds is None:
            G, I, thresholds = self.genuines_and_impostors(scores, labels)
        else:
            G, I, aux_thresholds = self.genuines_and_impostors(scores, labels)
        FAR, FRR, CRR, CAR, EER, AUC = self.compute_performance_analysis(G, I, thresholds)
        return FAR, FRR, CRR, CAR, EER, AUC


    def compute_scores(self, data, distance):
        """
        The compute_scores method computes the genuine and the impostor scores.

        :param data:     is the (subjects*repetitions*features) 3D-matrix as to analyze (None by default, the previous
                         data will be used if None)
        :param distance: is the function (or one string between 'euclidean', 'manhattan', 'mahalanobis' and
                         'minkowski', representing the homonymous distances) which is used in order to evaluate the
                         distance in the genuine and impostor scores computation (None by default, the previously
                         inserted data if None)

        :return:         the 1D-array representing the genuine scores
                         (genuine_scores) and the impostor scores (impostor_scores)
        """
        print('Computing the scores')
        distance.set_parameters(data)
        size = np.shape(data)
        if len(size) == 3:
            data = np.reshape(data, (size[0]*size[1], size[2]))
            size = np.shape(data)
        scores_dimension = size[0]
        n_features = size[1]
        scores = np.ones(shape=(scores_dimension, scores_dimension))
        for i in range(scores_dimension):
            for j in range(i + 1, scores_dimension):
                dist = distance.compute_distance(data[i, 0:n_features], data[j, 0:n_features])
                scores[i, j] = 1 / (1 + dist)
                scores[j, i] = scores[i, j]
        return scores


    def genuines_and_impostors(self, scores, labels):
        """
        The genuines_and_impostors method computes the genuine scores and the
        impostor scores.

        :param scores: is the 2D (subjects*subjects) representing the computed scores
        :param labels: is the list of labels associated to the subjects, in the samme order as the scores

        :return:       the array of genuine scores, the array of impostor scores and the array of values found either in
                       one or both the previous arrays (if a total number of elements lower than 1000 is found, a set of
                       linearly separated elements having a 0.001 step between two consecutive elements otherwise)
        """
        print('Computing genuine scores and impostor scores')
        scores_dimension, genuine_dimension, impostor_dimension = self._define_dimensions(scores, labels)
        genuine_score = np.zeros(shape=(genuine_dimension, 1))
        impostor_score = np.zeros(shape=(impostor_dimension, 1))
        indg = 0
        indi = 0
        for i in range(scores_dimension):
            for j in range(i):
                if labels[i] == labels[j]:
                    genuine_score[indg, 0] = scores[i, j];
                    indg = indg + 1;
                else:
                    impostor_score[indi, 0] = scores[i, j];
                    indi = indi + 1;
        gen_unique = np.unique(genuine_score)
        imp_unique = np.unique(impostor_score)
        print('Defining the thresholds')
        thresholds = np.concatenate(([0], gen_unique, imp_unique, [1]))
        thresholds = np.unique(thresholds)
        if np.max(np.shape(thresholds)) > 100:
            thresholds = self._compute_thresholds(0.01)
        return genuine_score, impostor_score, thresholds


    def scores_statistics(self, scores):
        """
        The scores_statiscics computes a set of descriptive statistical parameters (mean, median, standard deviation) on
        the array of similarity scores.

        :param scores: is the 1D array representing the scores distribution (for example, the genuine scores)

        :return:       the mean, the median and the standard deviation of the scores distribution
        """
        aux_scores = np.array(scores)
        return np.mean(aux_scores), np.median(aux_scores), np.std(aux_scores)



    def _define_dimensions(self, scores, labels=None):
        """
        The _define_dimension method computes the dimension of arrays related to impostor and genuine scores computation
        (FOR INTERNAL USE ONLY).

        :param scores: is the 2D (subjects*subjects) representing the computed scores
        :param labels: is the list of labels associated to the subjects, in the samme order as the scores

        :return:       the number of subjects, the dimension of the genuine array and the dimension of the impostor
                       array
        """
        scores_dimension = np.shape(scores)[0]
        genuine_dimension = 0
        impostor_dimension = 0
        for i in range(scores_dimension):
            for j in range(i):
                if labels[i] == labels[j]:
                    genuine_dimension += 1;
                else:
                    impostor_dimension += 1;
        return scores_dimension, genuine_dimension, impostor_dimension
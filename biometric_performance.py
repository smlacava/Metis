import numpy as np


class biometric_performance():
    def compute_FAR(self, impostor_score, thresholds=0.01):
        """
        The compute_FAR method is used to compute the False Acceptance Rate (FAR).

        :param impostor_score: is the 1D-array, representing the impostor scores,
                               used to compute the FAR array
        :param thresholds:     is the length of each step which has to be used in
                               evaluating the different thresholds for which values
                               compute the FAR, or the array representing all the
                               considered thrsholds (0.01 by default)

        :return:               the 1D-array representing the FAR computed on each
                               threshold value between 0 and 1
        """
        condition = lambda score, thr: score > thr
        return self._F_performance(np.squeeze(np.array(impostor_score)),
                                   thresholds, condition)

    def compute_FRR(self, genuine_score, thresholds=0.01):
        """
        The compute_FRR method is used to compute the False Rejection Rate (FRR).

        :param genuine_score:  is the 1D-array, representing the genuine scores,
                               used to compute the FRR array
        :param thresholds:     is the length of each step which has to be used in
                               evaluating the different thresholds for which values
                               compute the FAR, or the array representing all the
                               considered thrsholds (0.01 by default)

        :return:               the 1D-array representing the FRR computed on each
                               threshold value between 0 and 1
        """
        condition = lambda score, thr: score <= thr
        return self._F_performance(genuine_score, thresholds, condition)

    def _F_performance(self, score, thresholds, condition):
        """
        The _F_performance method is used to compute the False Rejection Rate or the
        False Acceptance Rate (FOR INTERNAL USE ONLY).

        :param score:          is the 1D-array, representing the scores on which
                               compute the FAR or the FRR
        :param thresholds:     is the length of each step which has to be used in
                               evaluating the different thresholds for which values
                               compute the FAR and the FRR, or the array
                               representing all the considered thrsholds
        :param condition:      it is the function which compares a score value with
                               a threshold value (score > threshold for the FAR
                               computation, score <= threshold for the FRR
                               computation)

        :return:               the 1D-array representing the FRR computed on each
                               threshold value between 0 and 1
        """
        if type(thresholds) is float:
            thr = thresholds
            limit = int(1 / thresholds)
            thresholds = [x * thr for x in range(limit)]
            thresholds.append(1)
        F = np.zeros(shape=(1, len(thresholds)))
        impostors = 0
        L = len(score)
        for count, thr in enumerate(thresholds):
            N = 0
            for idx in range(0, L):
                N += condition(score[idx], thr)
            F[0, count] = N / L
        return F[0]

    def compute_EER(self, FAR, FRR):
        """
        The compute_EER method computes the Equality Error Rate (EER) through the
        False Acceptance Rate (FAR) and the False Rejection Rate (FRR).

        :param FAR: it is the 1D-array representing the FAR on each threshold value
        :param FRR: it is the 1D-array representing the FRR on each threshold value

        :return:    a value representing the EER
        """
        distance = abs(FAR - FRR)
        min_distance = min(distance)
        idx = np.where(distance == min_distance)
        return np.mean((FAR[idx] + FRR[idx]) / 2)

    def compute_CRR(self, FAR):
        """
        The compute_CRR method computes the Correct Rejection Rate (CRR) from the
        False Acceptance Rate (FAR).

        :param FAR: it is the 1D-array representing the FAR on each threshold value

        :return: the 1D-array representing the CRR on each threshold value
        """
        return (np.ones((1, len(FAR))) - FAR)[0]

    def compute_CAR(self, FRR):
        """
        The compute_CAR method computes the Correct Acceptance Rate (CAR) from the
        False Rejection Rate (FRR).

        :param FRR: it is the 1D-array representing the FRR on each threshold value

        :return: the 1D-array representing the CAR on each threshold value
        """
        return (np.ones((1, len(FRR))) - FRR)[0]

    def compute_performance_analysis(self, G, I, thresholds=0.01):
        """
        The compute_performance_analysis method computes the False Acceptance Rate
        (FAR), the False Rejection Rate (FRR), the Correct Rejection Rate (CRR), the
        Correct Acceptance Rate (CAR) for each threshold value, and the Equality
        Error Rate (EER) on a genuine scores array and an impostor scores array.

        :param G:          it is the 1D-array representing the genuine scores
        :param I:          it is the 1D-array representing the impostor scores
        :param thresholds: is the length of each step which has to be used in
                           evaluating the different thresholds for which values
                           compute the FAR, or the array representing all the
                           considered thrsholds (0.01 by default)

        :return:           the FAR, FRR, CRR and CAR 1D-arrays and the EER value
        """
        FAR = self.compute_FAR(I, thresholds)
        FRR = self.compute_FRR(G, thresholds)
        CRR = self.compute_CRR(FAR)
        CAR = self.compute_CAR(FRR)
        EER = self.compute_EER(FAR, FRR)
        return FAR, FRR, CRR, CAR, EER

    def compute_analysis(self, data, labels, distance):
        """
        The compute_analysis method computes the False Acceptance Rate (FAR), the
        False Rejection Rate (FRR), the Correct Rejection Rate (CRR), the Correct
        Acceptance Rate (CAR) for each threshold value, and the Equality Error Rate
        (EER) on a data matrix.

        :param data:       it is the 3D (subjects*repetitions*features) data matrix
                           (None by default, the previous data will be used if None)
        :param distance:   it is the function (or one string between 'euclidean',
                           'manhattan' and 'minkowski', representing the homonymous
                           distances) which is used in order to evaluate the
                           distance in the genuine and impostor scores computation
                           (optional, euclidean distance by default)
        :param thresholds: is the length of each step which has to be used in
                           evaluating the different thresholds for which values
                           compute the FAR, or the array representing all the
                           considered thrsholds (0.01 by default)

        :return:           the FAR, FRR, CRR and CAR 1D-arrays and the EER value
        """
        scores = self.compute_scores(data, distance)
        G, I, thresholds = self.genuines_and_impostors(scores, labels)
        FAR, FRR, CRR, CAR, EER = self.compute_performance_analysis(G, I, thresholds)
        return FAR, FRR, CRR, CAR, EER

    def compute_scores(self, data, distance):
        """
        The compute_scores method computes the genuine and the impostor scores.

        :param data:     it is the (subjects*repetitions*features) 3D-matrix as
                         to analyze (None by default, the previous data will be used
                         if None)
        :param distance: it is the function (or one string between 'euclidean',
                         'manhattan' and 'minkowski', representing the homonymous
                         distances) which is used in order to evaluate the distance
                         in the genuine and impostor scores computation (None by
                         default, the previously inserted data if None)

        :return:         the 1D-array representing the genuine scores
                         (genuine_scores) and the impostor scores (impostor_scores)
        """
        distance.set_parameters(data)
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

        """
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
        thresholds = np.concatenate(([0], gen_unique, imp_unique, [1]))
        thresholds = np.unique(thresholds)
        return genuine_score, impostor_score, thresholds

    def _define_dimensions(self, scores, labels):
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
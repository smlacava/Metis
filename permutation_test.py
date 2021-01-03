import numpy as np
from itertools import combinations
from math import factorial


class permutation_test():
    def __init__(self):
        """
        The __init__ method is the initializer, which sets the value for the attibutes.
        """
        self.methods = {'approximate': self._approximate, 'exact': self._exact}
        self.assumptions = {'different': self._different, 'lower': self._lower,
                            'higher': self._higher, 'first_lower': self._lower,
                            'first_higher': self._higher}


    def _different(self, first, second):
        """
        The _different method return the absolute distance between the means of the two data matrices (FOR INTERNAL USE
        ONLY).

        :param first: it is the first 2D (samples*features) data matrix
        :param second: it is the second 2D (samples*features) data matrix

        :return: the array representing the absolute differences between means for each feature
        """
        return np.abs(self._higher(first, second))


    def _higher(self, first, second):
        """
        The _different method return the difference between the means of the first data matrix and the second one (FOR
        INTERNAL USE ONLY).

        :param first: it is the first 2D (samples*features) data matrix
        :param second: it is the second 2D (samples*features) data matrix

        :return: the array representing the differences between means for each feature
        """
        return np.mean(first) - np.mean(second)


    def _lower(self, first, second):
        """
        The _different method return the difference between the means of the second data matrix and the first one (FOR
        INTERNAL USE ONLY).

        :param first: it is the first 2D (samples*features) data matrix
        :param second: it is the second 2D (samples*features) data matrix

        :return: the array representing the differences between means for each feature
        """
        return np.mean(second) - np.mean(first)


    def _exact(self, first, second, assumption, combined, reference,
               first_samples, second_samples, tot_samples, repetitions):
        """
        The _exact method executes the permutation test by considering all the samples (FOR INTERNAL USE ONLY).

        :param first:          it is the first 2D (samples*features) data matrix
        :param second:         it is the second 2D (samples*features) data matrix
        :param assumption:     it is the considered assumption ("the means are different", "the first mean is higher
                               than the second one", or "the first mean is lower than the second one")
        :param combined:       it is the data matrix resulting by the joining between the two data matrices
        :param reference:      it is the reference value resulting from the assumption applied on the combined matrix
        :param first_samples:  it is the number of samples related to the first data matrix
        :param second_samples: it is the number of samples related to the second data matrix
        :param tot_samples:    it is the total number of samples (first_samples + second_samples)
        :param repetitions:    NOT USED

        :return:               the p-value resulting from the permutation test
        """
        pvalue = 0.
        for first_idx in combinations(range(tot_samples), first_samples):
            second_idx = [idx for idx in range(tot_samples) if idx not in first_idx]
            diff = self.assumptions[assumption](combined[list(first_idx)],
                                                combined[second_idx])
            if diff > reference or np.isclose(diff, reference):
                pvalue += 1
        pvalue *= (factorial(first_samples) * factorial(second_samples))
        return pvalue / factorial(tot_samples)


    def _approximate(self, first, second, assumption, combined, reference,
                     first_samples, second_samples, tot_samples, repetitions):
        """
        The _approximate method executes the permutation test by repeating more times the test on random subsets of
        data (FOR INTERNAL USE ONLY).

        :param first:          it is the first 2D (samples*features) data matrix
        :param second:         it is the second 2D (samples*features) data matrix
        :param assumption:     it is the considered assumption ("the means are different", "the first mean is higher
                               than the second one", or "the first mean is lower than the second one")
        :param combined:       it is the data matrix resulting by the joining between the two data matrices
        :param reference:      it is the reference value resulting from the assumption applied on the combined matrix
        :param first_samples:  it is the number of samples related to the first data matrix
        :param second_samples: it is the number of samples related to the second data matrix
        :param tot_samples:    it is the total number of samples (first_samples + second_samples)
        :param repetitions:    the number of repetitions of the test on the random subset

        :return:               the p-value resulting from the permutation test
        """
        pvalue = 1.
        rng = np.random.RandomState(None)
        for i in range(repetitions):
            rng.shuffle(combined)
            diff = self.assumptions[assumption](combined[:first_samples],
                                                combined[first_samples:])
            if diff > reference or np.isclose(diff, reference):
                pvalue += 1
        return pvalue / (repetitions + 1)


    def compute_permutation_test(self, first, second, method='approximate',
                                 assumption='different', repetitions=100):
        """
        The _exact method executes the permutation test by considering all the samples (FOR INTERNAL USE ONLY).

        :param first:          it is the first 2D (samples*features) data matrix
        :param second:         it is the second 2D (samples*features) data matrix
        :param method:         it is the permutation test method, between 'approximate' and 'exact', to execute the
                               test more times on subsets of the whole dataset or once on the whole dataset,
                               respectively ('approximate' by default)
        :param assumption:     it is the considered assumption, between 'different', 'higher' (or equivalently
                               'first_higher') and 'lower' (or equivalently 'first_lower'), representing that the
                               mean of the first dataset is different from, higher than or lower than the mean of the
                               second dataset, respectively ('different' by default)
        :param repetitions:    it is the number of repetitions of the test in case of the approximate permutation
                               test, unused in the exact case (100 by default)

        :return:               the p-value resulting from the permutation test
        """
        first = np.array(first)
        second = np.array(second)
        first_samples = np.shape(first)[0]
        second_samples = np.shape(second)[0]
        tot_samples = first_samples + second_samples
        combined = np.hstack((first, second))
        reference = self.assumptions[assumption](first, second)
        return self.methods[method](first, second, assumption, combined,
                                    reference, first_samples, second_samples,
                                    tot_samples, repetitions)




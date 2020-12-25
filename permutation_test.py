import numpy as np
from itertools import combinations
from math import factorial


class permutation_test():
    def __init__(self):
        self.methods = {'approximate': self._approximate, 'exact': self._exact}
        self.assumptions = {'different': self._different, 'lower': self._lower,
                            'higher': self._higher, 'first_lower': self._lower,
                            'first_higher': self._higher}

    def _different(self, first, second):
        return np.abs(self._higher(first, second))

    def _higher(self, first, second):
        return np.mean(first) - np.mean(second)

    def _lower(self, first, second):
        return np.mean(second) - np.mean(first)

    def _exact(self, first, second, assumption, combined, reference,
               first_samples, second_samples, tot_samples, repetitions):
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




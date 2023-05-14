import math
import time

import numpy as np
from tqdm import tqdm


class WeakClassifier:

    def __init__(self, feature):
        self.feature = feature
        self.threshold = None
        self.polarity = None

    def __str__(self):
        return 'Haar feature: {}, threshold: {}, polarity: {}'.format(self.feature, self.threshold, self.polarity)

    def classify(self, integral_image):
        return 1 if self.polarity * self.feature.calculate_value(
            integral_image) >= self.polarity * self.threshold else 0


class Adaboost:
    def __init__(self, t):
        self.t = t
        self.alphas = []
        self.clfs = []

    def classify(self, integral_image):
        total = 0
        for alpha, clf in zip(self.alphas, self.clfs):
            classification = clf.classify(integral_image)
            total += alpha * classification
        return 1 if total >= 0.5 * sum(self.alphas) else 0

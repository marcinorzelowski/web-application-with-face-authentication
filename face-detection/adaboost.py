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

    def train(self, feature_values, labels, weights):
        # sorting according to the feature values
        sorted_features = sorted(zip(feature_values, labels, weights), key=lambda a: a[0])
        error = sum(weight for value, label, weight in sorted_features if label == 0)
        min_error = error
        for value, label, weight in sorted_features:
            if label == 1:
                error -= weight
            else:
                error += weight

            if error < min_error:
                min_error = error
                self.threshold = value
                self.polarity = 1

            if 1 - error < min_error:
                min_error = 1 - error
                self.threshold = value
                self.polarity = -1
        return min_error

    def classify(self, integral_image):
        return 1 if self.polarity * self.feature.calculate_value(
            integral_image) >= self.polarity * self.threshold else 0


class Adaboost:
    def __init__(self, t):
        self.t = t
        self.alphas = []
        self.clfs = []

    def fit(self, feature_values, features, integral_images, labels):
        # initialize weights
        n_pos, n_neg = np.sum(labels), len(labels) - np.sum(labels)
        weights = np.zeros(len(labels))
        for i, label in enumerate(labels):
            if label == 1:
                weights[i] = 1 / (2 * n_pos)
            else:
                weights[i] = 1 / (2 * n_neg)

        # Each iteration select best classifier
        for i in tqdm(range(self.t), total=self.t, leave=True, position=1):
            weights = weights / np.sum(weights)
            classifiers = self.createWeakClassifiers(feature_values, features, weights, labels)
            clf, accuracy_matrix, error = self.select_best_classifier(classifiers, integral_images, labels, weights)
            beta = error / (1 - error) if error / (1 - error) else 0.000001
            alpha = math.log(1 / beta)
            for idx in range(len(weights)):
                weights[idx] = weights[idx] * beta ** (1 - accuracy_matrix[idx])
            self.clfs.append(clf)
            self.alphas.append(alpha)
            f_index = np.where(features == clf.feature)
            features = np.delete(features, f_index)
            feature_values = np.delete(feature_values, f_index, axis=0)

            print('Chosen classifier: {} with error {} and corresponding alpha: {}'.format(clf, error, alpha))

    def createWeakClassifiers(self, feature_values, features, weights, labels):
        classifiers = []
        for idx, feature in tqdm(enumerate(features), total=len(features), position=2, leave=True):
            clf = WeakClassifier(feature)
            clf.train(feature_values[idx], labels, weights)
            classifiers.append(clf)
        return classifiers

    def select_best_classifier(self, classifiers, integral_images, labels, weights):
        best_error = float('inf')
        best_clf = None
        best_acc = None

        for clf in tqdm(classifiers, total=len(classifiers)):
            accuracy_errors = []
            error = 0
            for sample, label, weight in zip(integral_images, labels, weights):
                if clf.classify(sample) != label:
                    error += weight
                    accuracy_errors.append(1)
                else:
                    accuracy_errors.append(0)

            if error == 0:
                error += np.random.uniform(0, 1e-6)

            if error < best_error:
                best_error = error
                best_clf = clf
                best_acc = accuracy_errors
        return best_clf, best_acc, best_error

    def classify(self, integral_image):
        total = 0
        for alpha, clf in zip(self.alphas, self.clfs):
            classification = clf.classify(integral_image)
            total += alpha * classification
        return 1 if total >= 0.5 * sum(self.alphas) else 0

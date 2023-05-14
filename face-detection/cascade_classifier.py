import pickle
from datetime import datetime

import cv2
import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score
from tqdm import tqdm

import adaboost
from utils import haar_feature_utils


class CascadeClassifier:

    def __init__(self, layers):
        self.layers = layers
        self.clfs = []

    def fit(self, X, y, X_test, y_test):
        pos, neg = np.sum(y), len(y) - np.sum(y)
        print('Started training dataset with {} positive, {} negative samples.'.format(pos, neg))
        img_h, img_w = X[0].shape[:2]

        # Calculate haar features.
        features = haar_feature_utils.generate_haar_features(img_w, img_h)
        print('Created {} features for image {} x {}'.format(len(features), img_h, img_w))

        # Prepare data
        integral_images = np.array([cv2.integral(x) for x in X], dtype=np.uint32)
        feature_values = haar_feature_utils.calculate_haar_feature_values(features, X)

        pos_idxs, neg_idxs = np.where(y == 1)[0], np.where(y == 0)[0]

        for t in tqdm(self.layers, total=len(self.layers), position=0, leave=False):
            print('Started training layer with {} weak classifiers.'.format(t))
            used_indexes = np.concatenate((pos_idxs, neg_idxs))
            print(len(used_indexes))

            clf = adaboost.Adaboost(t)
            clf.fit(feature_values[:, used_indexes], features, integral_images[used_indexes], y[used_indexes])
            self.clfs.append(clf)
            new_neg_idx = []
            for neg_idx in neg_idxs:
                if self.classify(X[neg_idx]) == 1:
                    new_neg_idx.append(neg_idx)
            if len(new_neg_idx) == 0:
                print('All samples were classified correctly.')
                break
            neg_idxs = np.array(new_neg_idx)
            self.evaluate(X_test, y_test)

    def classify(self, img):
        integral_image = cv2.integral(img)

        for clf in self.clfs:
            if clf.classify(integral_image) == 0:
                return 0
        return 1

    def evaluate(self, X_test, y_test):
        y_pred = []
        for sample, label in zip(X_test, y_test):
            predicated = self.classify(sample)
            y_pred.append(predicated)
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

        print('True Negatives: ', tn)
        print('False Positives: ', fp),
        print('False Negatives: ', fn)
        print('True Positives: ', tp)
        print('Accuracy: ', accuracy_score(y_test, y_pred))
    def save(self):
        filename = './saved/result_' + datetime.now().strftime("%d_%m_%H%M")
        with open(filename + ".pkl", 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename):
        """
        A static method which loads the classifier from a pickle
          Args:
            filename: The name of the file (no file extension necessary)
        """
        with open(filename + ".pkl", 'rb') as f:
            return pickle.load(f)


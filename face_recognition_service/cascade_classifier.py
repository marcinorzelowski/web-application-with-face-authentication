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

    def classify(self, img):
        integral_image = cv2.integral(img)

        for clf in self.clfs:
            if clf.classify(integral_image) == 0:
                return 0
        return 1

    @staticmethod
    def load(filename):
        """
        A static method which loads the classifier from a pickle
          Args:
            filename: The name of the file (no file extension necessary)
        """
        with open(filename + ".pkl", 'rb') as f:
            return pickle.load(f)

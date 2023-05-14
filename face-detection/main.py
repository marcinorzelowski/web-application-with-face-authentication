# This is a sample Python script.
import datetime
import os

import cv2
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix

from utils import dataset_utils
from sklearn.model_selection import train_test_split

from cascade_classifier import CascadeClassifier


def evaluate(X_test, y_test, clf):
    y_pred = []
    for sample, label in zip(X_test, y_test):
        predicated = clf.classify(sample)
        y_pred.append(predicated)
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

    print('True Negatives: ', tn)
    print('False Positives: ', fp),
    print('False Negatives: ', fn)
    print('True Positives: ', tp)
    print('Accuracy: ', accuracy_score(y_test, y_pred))


if __name__ == '__main__':
    # annotations = dataset_utils.read_wider_annotations('raw_data/wider_face_train_bbx_gt.txt')
    # dataset_utils.get_non_faces_images(annotations, 60)
    X, y = dataset_utils.load_dataset(10000, 20000)
    clf = CascadeClassifier.load('saved/result_11_05_1442')
    evaluate(X, y, clf)


import os
import shutil

from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split

from cascade_classifier import CascadeClassifier
from utils import dataset_utils


def evaluate(X_test, y_test, clf):
    y_pred = []
    for sample, label in zip(X_test, y_test):
        predicated = clf.classify(sample)[0]
        y_pred.append(predicated)
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

    print('True Negatives: ', tn)
    print('False Positives: ', fp),
    print('False Negatives: ', fn)
    print('True Positives: ', tp)
    print('Accuracy: ', accuracy_score(y_test, y_pred))



if __name__ == '__main__':
    X, y = dataset_utils.load_dataset(2, 2)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=42)
    clf = CascadeClassifier([2])
    clf.fit(X_train, y_train)
    clf.save()








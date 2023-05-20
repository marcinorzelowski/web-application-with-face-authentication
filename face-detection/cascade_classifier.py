import os.path
import pickle
from datetime import datetime

import cv2
import dlib
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
        total = 0
        for clf in self.clfs:
            score = clf.classify(integral_image)
            total += score
            if score < 0.5:
                return 0, 0
        return 1, total / len(self.clfs)


    def sliding_window(self, image, step_size=2):
        for y in range(0, image.shape[0] - 24, step_size):
            for x in range(0, image.shape[1] - 24, step_size):
                yield x, y, image[y:y + 24, x:x + 24]

    def detect_multiscale(self, image, name):
        h, w = image.shape[:2]
        boxes = []
        probs = []
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        image = clahe.apply(image)
        image_pyramid = self.create_image_pyramid(image)
        for img in image_pyramid:
            scale = (h / img.shape[0])
            for x, y, window in self.sliding_window(img):
                classification, score = self.classify(window)
                if classification == 1:
                    probs.append(score)
                    if not os.path.exists('saved/window/{}'.format(name)):
                        os.makedirs('saved/window/{}'.format(name))
                    cv2.imwrite('saved/window/{}/{}-{}.jpg'.format(name, score, scale), window)
                    boxes.append(
                        (int(x * scale), int(y * scale), int(x * scale + 24 * scale), int(y * scale + 24 * scale)))

        mean_face = self.non_max_suppression(boxes, probs, 0.7)[0]
        return mean_face

    def non_max_suppression(self, boxes, scores, threshold):
        assert len(boxes) == len(scores)

        # List to hold the picked boxes
        pick = []

        # Sort the bounding boxes by the scores
        idxs = np.argsort(scores)

        # Keep looping while some indexes still remain in the indexes list
        while len(idxs) > 0:
            # Grab the last index in the indexes list and add the index value to the list of picked indexes
            last = len(idxs) - 1
            i = idxs[last]
            pick.append(i)

            # Compute the IoU for the current box with all remaining boxes
            overlap = np.array([self.calculate_iou(boxes[i], boxes[idx]) for idx in idxs[:last]])

            # Delete all indexes from the index list that have an IoU greater than the provided threshold
            idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > threshold)[0])))

        boxes = np.array(boxes)
        return boxes[np.array(pick, dtype=int)]




    def calculate_iou(self, box1, box2):
        x1, y1, x2, y2 = box1
        x1_b, y1_b, x2_b, y2_b = box2
        rec1 = dlib.rectangle(x1, y1, x2, y2)
        rec2 = dlib.rectangle(x1_b, y1_b, x2_b, y2_b)

        intersection = rec1.intersect(rec2).area()

        return intersection / (rec1.area() + rec2.area() - intersection)



    def create_image_pyramid(self, image, scale_factor=1.1, min_size=(24, 24)):
        pyramid = []
        while image.shape[0] >= min_size[1] and image.shape[1] >= min_size[0]:
            pyramid.append(image)
            new_height = int(image.shape[0] / scale_factor)
            new_width = int(image.shape[1] / scale_factor)
            image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        return pyramid[-10:]

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

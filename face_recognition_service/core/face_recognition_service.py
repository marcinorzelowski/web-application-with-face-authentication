import os
import pickle
import time

import cv2
import logging

import dlib
import numpy as np

import utils.image_utils as utils
from cascade_classifier import CascadeClassifier

logger = logging.getLogger(__name__)


class FaceRecognitionService:
    def __init__(self):
        self.landmark_predictor = dlib.shape_predictor('core/shape_predictor_68_face_landmarks.dat')
        self.cascade_classifier = CascadeClassifier.load('resources/result_11_05_1442')

    def extract_features(self, image):
        gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        face = self.cascade_classifier.detect_multiscale(gray_scale)
        preprocessed_image = self.preprocess_image(image, face)
        features, landmarks = self.calculate_features(preprocessed_image)
        cv2.imwrite('saved_images/' + str(time.time()) + '.jpg', self.draw_landmarks(preprocessed_image, landmarks))

        logger.info(features)
        return features

    def preprocess_image(self, image, face_rect):
        x1, y1, x2, y2 = face_rect
        padding = int(0.2 * max((y2 - y1), (x2 - x1)))
        img_h, img_w = image.shape[:2]

        x1 = x1 - padding if x1 - padding > 0 else 0
        y1 = y1 - padding if y1 - padding > 0 else 0
        x2 = x2 + padding if x2 + padding < img_w else img_w
        y2 = y2 + padding if y2 + padding < img_h else img_h

        face_image = image[y1: y2, x1: x2]

        face_image = cv2.resize(face_image, (500, 500))
        face_image = cv2.GaussianBlur(face_image, (3, 3), 2)
        face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        face_image = cv2.equalizeHist(face_image)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        face_image = clahe.apply(face_image)

        return face_image

    def calculate_features(self, image):

        rectangle = dlib.rectangle(left=0, top=0, right=500, bottom=500)

        landmarks = self.landmark_predictor(image, rectangle)
        landmarks = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(landmarks.num_parts)],
                             dtype=np.int64)
        eye_distance = utils.calculate_distance_on_landmark(landmarks, 36, 45)
        features = [
            0.5 * (utils.calculate_distance_on_landmark(landmarks, 36, 39) + (
                utils.calculate_distance_on_landmark(landmarks, 42, 45))),
            utils.calculate_distance_on_landmark(landmarks, 0, 16),
            utils.calculate_distance_on_landmark(landmarks, 2, 14),
            utils.calculate_distance_on_landmark(landmarks, 4, 12),
            utils.calculate_distance_on_landmark(landmarks, 6, 10),
            utils.calculate_distance_on_landmark(landmarks, 48, 6),
            utils.calculate_distance_on_landmark(landmarks, 54, 10),
            utils.calculate_distance_on_landmark(landmarks, 48, 54),
            utils.calculate_distance_on_landmark(landmarks, 62, 51),
            utils.calculate_distance_on_landmark(landmarks, 66, 57),
            utils.calculate_distance_on_landmark(landmarks, 8, 57),
            utils.calculate_distance_on_landmark(landmarks, 33, 51),
            utils.calculate_distance_on_landmark(landmarks, 31, 35),
            0.5 * (utils.calculate_distance_on_landmark(landmarks, 0,
                                                        2) + utils.calculate_distance_on_landmark(
                landmarks, 16, 14)),
            0.5 * (utils.calculate_distance_on_landmark(landmarks, 2,
                                                        4) + utils.calculate_distance_on_landmark(
                landmarks, 14, 12)),
            0.5 * (utils.calculate_distance_on_landmark(landmarks, 4,
                                                        6) + utils.calculate_distance_on_landmark(
                landmarks, 10, 12)),
            0.5 * (utils.calculate_distance_on_landmark(landmarks, 39,
                                                        31) + utils.calculate_distance_on_landmark(

                landmarks, 42, 35)),
            utils.calculate_distance_on_landmark(landmarks, 39, 42),
            0.5 * (utils.calculate_distance_on_landmark(landmarks, 36,
                                                        17) + utils.calculate_distance_on_landmark(
                landmarks, 26, 45)),
            0.5 * (utils.calculate_distance_on_landmark(landmarks, 17,
                                                        21) + utils.calculate_distance_on_landmark(
                landmarks, 22, 26)),
            0.5 * (utils.calculate_distance_on_landmark(landmarks, 21,
                                                        39) + utils.calculate_distance_on_landmark(
                landmarks, 42, 22)),
            0.5 * (utils.calculate_distance_on_landmark(landmarks, 37,
                                                        19) + utils.calculate_distance_on_landmark(
                landmarks, 43, 24)),
            0.5 * (utils.calculate_distance_on_landmark(landmarks, 19,
                                                        21) + utils.calculate_distance_on_landmark(
                landmarks, 22, 24)),
            0.5 * (utils.calculate_distance_on_landmark(landmarks, 17,
                                                        19) + utils.calculate_distance_on_landmark(
                landmarks, 24, 26)),
            utils.calculate_distance_on_landmark(landmarks, 39, 33),
            utils.calculate_distance_on_landmark(landmarks, 42, 33),
            0.5 * (utils.calculate_distance_on_landmark(landmarks, 42,
                                                        54) + utils.calculate_distance_on_landmark(
                landmarks, 39, 48)),
            0.5 * (utils.calculate_distance_on_landmark(landmarks, 0,
                                                        36) + utils.calculate_distance_on_landmark(
                landmarks, 16, 45))

        ]
        features = np.array(features)
        features = features / eye_distance
        features = features.tolist()

        return features, landmarks

    def extract_mean_features(self, images):
        data = []
        for i, image in enumerate(images):
            gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            face = self.cascade_classifier.detect_multiscale(gray_scale)

            preprocessed_image = self.preprocess_image(image, face)
            features, landmarks = self.calculate_features(preprocessed_image)
            cv2.imwrite('registration_images/' + str(time.time()) + '.jpg',
                        self.draw_landmarks(preprocessed_image, landmarks))

            data.append(features)
        return data

    def draw_landmarks(self, image, landmarks):

        for i in range(68):
            x, y = landmarks[i]
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

        return image

    def load_face_detector(self, path):
        print(os.path.isfile(path))
        with open(path, 'rb') as file:
            return pickle.load(file)

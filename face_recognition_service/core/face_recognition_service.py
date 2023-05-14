import math
import os
import pickle
import time
from collections import defaultdict

import cv2
import logging

import dlib
import numpy as np

import utils.image_utils
from cascade_classifier import CascadeClassifier
from enums.FeatureType import FeatureType
from exception.FacesNotFound import FacesNotFound
from models.Feature import Feature
from utils import image_utils

logger = logging.getLogger(__name__)


class FaceRecognitionService:
    def __init__(self):
        # self.face_classifier = CascadeClassifier.load('resources/result_05_05_1834')
        self.haar_cascade = cv2.CascadeClassifier('core/cascade.xml')
        self.landmark_predictor = dlib.shape_predictor('core/shape_predictor_68_face_landmarks.dat')

    def extract_features(self, image):
        # Convert to gray scale
        gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = self.haar_cascade.detectMultiScale(gray_scale, 1.1, 10)

        if len(faces) == 0:

            cv2.imwrite('saved_images/' + 'fail' + '.jpg', image)

            raise FacesNotFound()
        else:
            preprocessed_image = self.preprocess_image(image, faces[0])
            features, landmarks = self.calculate_features(preprocessed_image)
            cv2.imwrite('saved_images/' + str(time.time()) + '.jpg', self.draw_landmarks(preprocessed_image, landmarks))

            logger.info(features)
            return features

    def preprocess_image(self, image, face_rect):
        x, y, w, h = face_rect
        padding = int(0.15 * max(w, h))
        img_h, img_w = image.shape[:2]

        padded_y = y - padding if y - padding > 0 else 0
        padded_x = x - padding if x - padding > 0 else 0

        padded_h = y + h + padding if y + h + padding < img_h else img_h
        padded_w = x + w + padding if x + w + padding < img_w else img_w

        face_image = image[padded_y: padded_h, padded_x: padded_w]

        face_image = cv2.resize(face_image, (500, 500))
        face_image = cv2.GaussianBlur(face_image, (3, 3), 2)
        face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        face_image = cv2.equalizeHist(face_image)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        face_image = clahe.apply(face_image)


        return face_image

    def calculate_features(self, image):
        x, y, w, h = self.haar_cascade.detectMultiScale(image, 1.1, 6)[0]

        rectangle = dlib.rectangle(left=x, top=y, right=x + w, bottom=y + h)

        landmarks = self.landmark_predictor(image, rectangle)
        landmarks = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(landmarks.num_parts)],
                                dtype=np.int64)

        features = [
            Feature(value=0.5 * (utils.image_utils.calculate_distance_on_landmark(landmarks, 36, 39) + (
                utils.image_utils.calculate_distance_on_landmark(landmarks, 42, 45))),
                    feature_type=FeatureType.FEATURE_1),
            Feature(value=image_utils.calculate_distance_on_landmark(landmarks, 0, 16),
                    feature_type=FeatureType.FEATURE_3),
            Feature(value=image_utils.calculate_distance_on_landmark(landmarks, 2, 14),
                    feature_type=FeatureType.FEATURE_4),
            Feature(value=image_utils.calculate_distance_on_landmark(landmarks, 4, 12),
                    feature_type=FeatureType.FEATURE_5),
            Feature(value=image_utils.calculate_distance_on_landmark(landmarks, 6, 10),
                    feature_type=FeatureType.FEATURE_6),
            Feature(value=image_utils.calculate_distance_on_landmark(landmarks, 48, 6),
                    feature_type=FeatureType.FEATURE_7),
            Feature(value=image_utils.calculate_distance_on_landmark(landmarks, 54, 10),
                    feature_type=FeatureType.FEATURE_8),
            Feature(value=image_utils.calculate_distance_on_landmark(landmarks, 48, 54),
                    feature_type=FeatureType.FEATURE_9),
            Feature(value=image_utils.calculate_distance_on_landmark(landmarks, 62, 51),
                    feature_type=FeatureType.FEATURE_10),
            Feature(value=image_utils.calculate_distance_on_landmark(landmarks, 66, 57),
                    feature_type=FeatureType.FEATURE_11),
            Feature(value=image_utils.calculate_distance_on_landmark(landmarks, 8, 57),
                    feature_type=FeatureType.FEATURE_12),
            Feature(value=image_utils.calculate_distance_on_landmark(landmarks, 33, 51),
                    feature_type=FeatureType.FEATURE_13),
            Feature(value=image_utils.calculate_distance_on_landmark(landmarks, 31, 35),
                    feature_type=FeatureType.FEATURE_14),
            Feature(value=0.5 * (image_utils.calculate_distance_on_landmark(landmarks, 0,
                                                                            2) + image_utils.calculate_distance_on_landmark(
                landmarks, 16, 14)),
                    feature_type=FeatureType.FEATURE_15),
            Feature(value=0.5 * (image_utils.calculate_distance_on_landmark(landmarks, 2,
                                                                            4) + image_utils.calculate_distance_on_landmark(
                landmarks, 14, 12)),
                    feature_type=FeatureType.FEATURE_16),
            Feature(value=0.5 * (image_utils.calculate_distance_on_landmark(landmarks, 4,
                                                                            6) + image_utils.calculate_distance_on_landmark(
                landmarks, 10, 12)),
                    feature_type=FeatureType.FEATURE_17),
            Feature(value=0.5 * (image_utils.calculate_distance_on_landmark(landmarks, 39,
                                                                            31) + image_utils.calculate_distance_on_landmark(
                landmarks, 42, 35)),
                    feature_type=FeatureType.FEATURE_18),
            Feature(value=image_utils.calculate_distance_on_landmark(landmarks, 39, 42),
                    feature_type=FeatureType.FEATURE_19),
            Feature(value=0.5 * (image_utils.calculate_distance_on_landmark(landmarks, 36,
                                                                            17) + image_utils.calculate_distance_on_landmark(
                landmarks, 26, 45)),
                    feature_type=FeatureType.FEATURE_20),
            Feature(value=0.5 * (image_utils.calculate_distance_on_landmark(landmarks, 17,
                                                                            21) + image_utils.calculate_distance_on_landmark(
                landmarks, 22, 26)),
                    feature_type=FeatureType.FEATURE_21),
            Feature(value=0.5 * (image_utils.calculate_distance_on_landmark(landmarks, 21,
                                                                            39) + image_utils.calculate_distance_on_landmark(
                landmarks, 42, 22)),
                    feature_type=FeatureType.FEATURE_22),
            Feature(value=0.5 * (image_utils.calculate_distance_on_landmark(landmarks, 37,
                                                                            19) + image_utils.calculate_distance_on_landmark(
                landmarks, 43, 24)),
                    feature_type=FeatureType.FEATURE_23),
            Feature(value=0.5 * (image_utils.calculate_distance_on_landmark(landmarks, 19,
                                                                            21) + image_utils.calculate_distance_on_landmark(
                landmarks, 22, 24)),
                    feature_type=FeatureType.FEATURE_25),
            Feature(value=0.5 * (image_utils.calculate_distance_on_landmark(landmarks, 17,
                                                                            19) + image_utils.calculate_distance_on_landmark(
                landmarks, 24, 26)),
                    feature_type=FeatureType.FEATURE_26),
            Feature(value=image_utils.calculate_distance_on_landmark(landmarks, 39, 33),
                    feature_type=FeatureType.FEATURE_27),
            Feature(value=image_utils.calculate_distance_on_landmark(landmarks, 42, 33),
                    feature_type=FeatureType.FEATURE_28),
            Feature(value=0.5 * (image_utils.calculate_distance_on_landmark(landmarks, 42,
                                                                            54) + image_utils.calculate_distance_on_landmark(
                landmarks, 39, 48)),
                    feature_type=FeatureType.FEATURE_29),
            Feature(value=0.5 * (image_utils.calculate_distance_on_landmark(landmarks, 0,
                                                                            36) + image_utils.calculate_distance_on_landmark(
                landmarks, 16, 45)),
                    feature_type=FeatureType.FEATURE_30),

        ]

        return features, landmarks

    def extract_mean_features(self, images):
        data = []
        for i, image in enumerate(images):
            gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.haar_cascade.detectMultiScale(gray_scale, 1.1, 6)

            if len(faces) == 0:
                cv2.imwrite('saved_images/' + 'fail' + str(i) + '.jpg', image)
                logger.error('No faces found with image no.{}.'.format(str(i)))
                raise FacesNotFound()
            else:
                preprocessed_image = self.preprocess_image(image, faces[0])
                features, landmarks = self.calculate_features(preprocessed_image)
                cv2.imwrite('registration_images/' + str(time.time()) + '.jpg',
                            self.draw_landmarks(preprocessed_image, landmarks))

                data.append(features)

        features_dict = dict()
        for feature_list in data:
            for feature in feature_list:
                if feature.type not in features_dict:
                    features_dict[feature.type] = []
                features_dict[feature.type].append(feature.value)

        result = []
        for feature_type, values in features_dict.items():
            result.append(Feature(value=np.median(np.array(values)), feature_type=feature_type))
        return result

    def draw_landmarks(self, image, landmarks):

        for i in range(68):
            x, y = landmarks[i]
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

        return image

    def load_face_detector(self, path):
        print(os.path.isfile(path))
        with open(path, 'rb') as file:
            return pickle.load(file)



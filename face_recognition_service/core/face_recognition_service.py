import math
from collections import defaultdict

import cv2
import logging

import dlib
import numpy as np

from enums.FeatureType import FeatureType
from exception.FacesNotFound import FacesNotFound
from models.Feature import Feature
from utils import image_utils

logger = logging.getLogger(__name__)


class FaceRecognitionService:
    def __init__(self):
        self.haar_cascade = cv2.CascadeClassifier('core/cascade.xml')
        self.landmark_predictor = dlib.shape_predictor('core/shape_predictor_68_face_landmarks.dat')

    def extract_features(self, image):
        # Convert to gray scale
        gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = self.haar_cascade.detectMultiScale(gray_scale, 1.1, 9)

        if len(faces) != 1:
            logger.info('Faces found {}'.format(len(faces)))
            raise FacesNotFound()
        else:
            preprocessd_image = self.preprocess_image(image, faces[0])
            features = self.calculate_features(preprocessd_image)
            logger.info(features)
            return features

    def preprocess_image(self, image, face_rect):
        x, y, w, h = face_rect
        # Crop to the face region
        padding = 1.1
        face_img = image[y:y + int(h * padding), x:x + int(w * padding)]
        height, width = face_img.shape[:2]
        logger.info('Face: {}, {}'.format(height, width))
        img_size = max(height, width)
        black_image = np.zeros((img_size, img_size, 3), dtype=np.uint8)

        black_image[0:height, 0:width] = face_img

        result = cv2.resize(black_image, (200, 200))

        return result

    def calculate_features(self, image):
        rectangle = dlib.rectangle(0, 0, 200, 200)

        landmarks = self.landmark_predictor(image, rectangle)

        features = [Feature(image_utils.calculate_distance_between_eyes(landmarks), FeatureType.DISTANCE_BETWEEN_EYES),
                    Feature(image_utils.calculate_distance_on_landmark(landmarks, 0, 16), FeatureType.DISTANCE_BETWEEN_EARS),
                    Feature(image_utils.calculate_distance_on_landmark(landmarks, 27, 33), FeatureType.NOSE_LENGTH),
                    Feature(image_utils.calculate_distance_on_landmark(landmarks, 31, 35), FeatureType.NOSE_WIDTH),
                    Feature(image_utils.calculate_distance_on_landmark(landmarks, 57, 8), FeatureType.CHIN_HEIGHT)]

        return features

    def extract_mean_features(self, images):
        data = []
        for image in images:
            gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.haar_cascade.detectMultiScale(gray_scale, 1.1, 9)

            if len(faces) != 1:
                logger.info('Faces found {}'.format(len(faces)))
                raise FacesNotFound()
            else:
                preprocessd_image = self.preprocess_image(image, faces[0])
                data.append(self.calculate_features(preprocessd_image))

        values_sum = defaultdict(float)
        for feature_list in data:
            for feature in feature_list:
                values_sum[feature.type] += feature.value

        length = len(data)
        result = []
        for feature_type, mean_val in values_sum.items():
            result.append(Feature(value=mean_val / length, feature_type=feature_type))
        return result

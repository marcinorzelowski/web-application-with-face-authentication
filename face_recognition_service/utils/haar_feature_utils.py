import cv2
import numpy as np
from tqdm import tqdm

from haar_feature import HaarFeature, HaarFeatureType


def generate_haar_features(img_width, img_height, min_size=4, max_size=18):
    features = []
    for x in range(img_width):
        for y in range(img_height):
            for feature_width in range(min_size, img_width - x if img_width - x < max_size else max_size):
                for feature_height in range(min_size, img_height - y if img_height - y < max_size else max_size):
                    if feature_width % 2 == 0:
                        features.append(HaarFeature(x, y, feature_width, feature_height, HaarFeatureType.EDGE_VERTICAL))
                    if feature_width % 3 == 0:
                        features.append(HaarFeature(x, y, feature_width, feature_height, HaarFeatureType.LINE_VERTICAL))
                    if feature_height % 2 == 0:
                        features.append(
                            HaarFeature(x, y, feature_width, feature_height, HaarFeatureType.EDGE_HORIZONTAL))
                    if feature_height % 3 == 0:
                        features.append(
                            HaarFeature(x, y, feature_width, feature_height, HaarFeatureType.LINE_HORIZONTAL))
                    if feature_width % 2 == 0 and feature_height % 2 == 0 and feature_width == feature_height:
                        features.append(HaarFeature(x, y, feature_width, feature_height, HaarFeatureType.FOUR_SQUARED))
    return np.array(features)


def calculate_haar_feature_values(features, integral_images):
    features_values = np.zeros((len(features), len(integral_images)), dtype=np.int32)
    for i, feature in tqdm(enumerate(features), mininterval=5, position=0, leave=True,
                           desc='Calculating feature values out of {}'.format(len(features_values))):
        features_values[i] = list(map(lambda ii: feature.calculate_value(ii), integral_images))
    result = np.array(features_values)
    return result

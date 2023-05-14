import unittest
from unittest import TestCase

import cv2
import numpy as np

from haar_feature import HaarFeature, HaarFeatureType


class HaarFeatureTest(TestCase):

    def setUp(self):
        self.test_array = np.array([np.full(10, i, dtype=np.uint8) for i in range(0, 10, 1)])

    def test_calculating_haar_feature_value_line_horizontal(self):
        # Given
        integral_image = cv2.integral(self.test_array)
        feature = HaarFeature(x=0, y=0, width=3, height=3, type=HaarFeatureType.LINE_HORIZONTAL)

        # When
        real_value = feature.calculate_value(integral_image)

        # Then
        self.assertEqual(3, real_value)

    def test_calculating_haar_feature_value_line_vertical(self):
        # Given
        integral_image = cv2.integral(self.test_array)
        feature = HaarFeature(x=0, y=0, width=3, height=3, type=HaarFeatureType.LINE_VERTICAL)

        # When
        real_value = feature.calculate_value(integral_image)

        # Then
        self.assertEqual(3, real_value)

    def test_calculating_haar_feature_value_edge_horizontal(self):
        # Given
        integral_image = cv2.integral(self.test_array)
        feature = HaarFeature(x=0, y=0, width=6, height=2, type=HaarFeatureType.EDGE_HORIZONTAL)

        # When
        real_value = feature.calculate_value(integral_image)

        # Then
        self.assertEqual(-6, real_value)

    def test_calculating_haar_feature_value_edge_vertical(self):
        # Given
        integral_image = cv2.integral(self.test_array)
        print(self.test_array)
        feature = HaarFeature(x=0, y=0, width=4, height=6, type=HaarFeatureType.EDGE_VERTICAL)

        # When
        real_value = feature.calculate_value(integral_image)

        # Then
        self.assertEqual(0, real_value)

    def test_calculating_haar_feature_value_squared(self):
        # Given
        img = self.test_array
        img[0][0] = 5
        integral_image = cv2.integral(img)
        print(img)
        feature = HaarFeature(x=0, y=0, width=4, height=4, type=HaarFeatureType.FOUR_SQUARED)

        # When
        real_value = feature.calculate_value(integral_image)

        # Then
        self.assertEqual(5, real_value)


if __name__ == '__main__':
    unittest.main()

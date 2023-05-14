import unittest

import cv2
import numpy as np

from utils import image_utils


class ImageUtilsTest(unittest.TestCase):

    def setUp(self):
        self.test_array = np.array([np.full(10, i, dtype=np.uint8) for i in range(0, 10, 1)])

    def test_summed_area(self):
        # Given
        print(self.test_array)
        integral_image = cv2.integral(self.test_array)
        y1, x1 = 0, 0
        y2, x2 = 3, 3

        # When
        real_value = image_utils.calculate_summed_area(integral_image, x1, y1, x2, y2)
        # Then
        self.assertEqual(54, real_value)  # add assertion here


if __name__ == '__main__':
    unittest.main()

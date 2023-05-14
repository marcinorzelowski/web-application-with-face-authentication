import unittest


from utils import haar_feature_utils


class HaarFeatureUtilsTest(unittest.TestCase):


    def test_haar_feature_generation(self):
        haar_features = haar_feature_utils.generate_haar_features(4, 4, 2, 4)
        print(haar_features)

if __name__ == '__main__':
    unittest.main()

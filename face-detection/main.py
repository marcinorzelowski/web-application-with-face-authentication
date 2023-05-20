import os
import shutil

import cv2
from sklearn.metrics import accuracy_score, confusion_matrix


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

def drop_data(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Remove each file
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

if __name__ == '__main__':
    # annotations = dataset_utils.read_wider_annotations('raw_data/wider_face_train_bbx_gt.txt')
    # dataset_utils.get_non_faces_images(annotations, 60)
    drop_data('saved/images')
    drop_data('saved/nms')
    drop_data('saved/snms')
    drop_data('saved/window')
    clf = CascadeClassifier.load('saved/result_11_05_1442')
    for test_image in os.listdir('test_data'):
        img = cv2.imread('test_data/{}'.format(test_image), cv2.IMREAD_GRAYSCALE)
        x1, y1, x2, y2 = clf.detect_multiscale(img, test_image)
        cv2.imwrite('test_result/{}'.format(test_image), img[y1:y2, x1:x2])


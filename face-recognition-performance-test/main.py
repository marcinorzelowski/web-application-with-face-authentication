import math
import os.path
import uuid

import cv2
import dlib
import numpy as np
from scipy.spatial.distance import euclidean, cityblock, cosine, mahalanobis
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

cascade_classifier = cv2.CascadeClassifier('cascade.xml')
landmark_detector = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

counter = 1


def load_dataset():
    X = []
    y = []
    for label in os.listdir('ds'):
        for image_path in os.listdir('ds/{}'.format(label)):
            img = cv2.imread('ds/{}/{}'.format(label, image_path), cv2.IMREAD_GRAYSCALE)
            try:
                face_img = cut_face_image(img)
            except IndexError:
                print('Skipping {}'.format(image_path))
                continue

            X.append(face_img)
            y.append(label)
    return X, y


def cut_face_image(img):
    face_image = cv2.GaussianBlur(img, (3, 3), 2)
    face_image = cv2.equalizeHist(face_image)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    face_image = clahe.apply(face_image)

    face = cascade_classifier.detectMultiScale(image=face_image, scaleFactor=1.1, minNeighbors=7)[0]
    x, y, w, h = face
    padding = int(0.2 * h)
    img_h, img_w = face_image.shape[:2]

    padded_y = y - padding if y - padding > 0 else 0
    padded_x = x - padding if x - padding > 0 else 0

    padded_h = y + h + padding if y + h + padding < img_h else img_h
    padded_w = x + w + padding if x + w + padding < img_w else img_w

    face_image = face_image[padded_y: padded_h, padded_x: padded_w]
    face_image = resize_image_to_height(face_image, 500)
    return face_image


def calculate_distance_on_landmark(landmark, start, end):
    x_s, y_s = landmark[start]
    x_e, y_e = landmark[end]
    return math.dist((x_s, y_s), (x_e, y_e))


def calculate_features(face_image):
    faces = cascade_classifier.detectMultiScale(face_image, scaleFactor=1.1, minNeighbors=7)
    if len(faces) > 0:
        x, y, w, h = faces[0]
        rectangle = dlib.rectangle(left=x, top=y, right=x + w, bottom=y + h)
    else:
        h, w = face_image.shape[:2]

        rectangle = dlib.rectangle(left=0, top=0, right=w, bottom=h)

    landmarks = landmark_detector(face_image, rectangle)
    landmarks = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(landmarks.num_parts)],
                         dtype=np.int64)

    features = [
        0.5 * (calculate_distance_on_landmark(landmarks, 36, 39) + (
            calculate_distance_on_landmark(landmarks, 42, 45))),
        calculate_distance_on_landmark(landmarks, 0, 16),
        calculate_distance_on_landmark(landmarks, 2, 14),
        calculate_distance_on_landmark(landmarks, 4, 12),
        calculate_distance_on_landmark(landmarks, 6, 10),
        calculate_distance_on_landmark(landmarks, 48, 6),
        calculate_distance_on_landmark(landmarks, 54, 10),
        calculate_distance_on_landmark(landmarks, 48, 54),
        calculate_distance_on_landmark(landmarks, 62, 51),
        calculate_distance_on_landmark(landmarks, 66, 57),
        calculate_distance_on_landmark(landmarks, 8, 57),
        calculate_distance_on_landmark(landmarks, 33, 51),
        calculate_distance_on_landmark(landmarks, 31, 35),
        0.5 * (calculate_distance_on_landmark(landmarks, 0,
                                              2) + calculate_distance_on_landmark(
            landmarks, 16, 14)),
        0.5 * (calculate_distance_on_landmark(landmarks, 2,
                                              4) + calculate_distance_on_landmark(
            landmarks, 14, 12)),
        0.5 * (calculate_distance_on_landmark(landmarks, 4,
                                              6) + calculate_distance_on_landmark(
            landmarks, 10, 12)),
        0.5 * (calculate_distance_on_landmark(landmarks, 39,
                                              31) + calculate_distance_on_landmark(

            landmarks, 42, 35)),
        calculate_distance_on_landmark(landmarks, 39, 42),
        0.5 * (calculate_distance_on_landmark(landmarks, 36,
                                              17) + calculate_distance_on_landmark(
            landmarks, 26, 45)),
        0.5 * (calculate_distance_on_landmark(landmarks, 17,
                                              21) + calculate_distance_on_landmark(
            landmarks, 22, 26)),
        0.5 * (calculate_distance_on_landmark(landmarks, 21,
                                              39) + calculate_distance_on_landmark(
            landmarks, 42, 22)),
        0.5 * (calculate_distance_on_landmark(landmarks, 37,
                                              19) + calculate_distance_on_landmark(
            landmarks, 43, 24)),
        0.5 * (calculate_distance_on_landmark(landmarks, 19,
                                              21) + calculate_distance_on_landmark(
            landmarks, 22, 24)),
        0.5 * (calculate_distance_on_landmark(landmarks, 17,
                                              19) + calculate_distance_on_landmark(
            landmarks, 24, 26)),
        calculate_distance_on_landmark(landmarks, 39, 33),
        calculate_distance_on_landmark(landmarks, 42, 33),
        0.5 * (calculate_distance_on_landmark(landmarks, 42,
                                              54) + calculate_distance_on_landmark(
            landmarks, 39, 48)),
        0.5 * (calculate_distance_on_landmark(landmarks, 0,
                                              36) + calculate_distance_on_landmark(
            landmarks, 16, 45))

    ]
    eye_distance = calculate_distance_on_landmark(landmarks, 36, 45)

    features = np.array(features) / eye_distance

    return features.tolist()


def calculate_feature_vector(img):
    features = calculate_features(img)
    return features


def calculate_mean_vector(db_images):
    vectors = []
    for img in db_images:
        vectors.append(calculate_feature_vector(img))
    return np.median(np.array(vectors), axis=0)


def create_database(X, y):
    X_train, X_test, y_train, y_test = [], [], [], []
    for label in np.unique(y):
        label_images = [img for img, img_label in zip(X, y) if img_label == label]
        counter = 0
        for img in label_images:
            if counter < 7:
                X_train.append(calculate_feature_vector(img))
                y_train.append(label)
            else:
                X_test.append(calculate_feature_vector(img))
                y_test.append(label)
            counter += 1
    return X_train, X_test, y_train, y_test


def create_database_for_distances(X, y):
    X_train, X_test, y_train, y_test = [], [], [], []
    for label in np.unique(y):
        label_images = [img for img, img_label in zip(X, y) if img_label == label]
        mean = []
        for img in label_images:
            if len(mean) < 5:
                mean.append(calculate_feature_vector(img))
            else:
                X_test.append(calculate_feature_vector(img))
                y_test.append(label)
        X_train.append(np.mean(mean, axis=0))
        y_train.append(label)
    return X_train, X_test, y_train, y_test


def calculate_euclidean_accuracy(X_train, y_train, X_test, y_test):
    correct, incorrect = 0, 0
    for x, y in zip(X_test, y_test):
        distances = []
        for x_db in X_train:
            distances.append(euclidean(x_db, x))
        min_index = np.argmin(distances)
        if y == y_train[min_index]:
            correct += 1
        else:
            incorrect += 1
    print('Accuracy: {}, Correct: {}, Incorrect: {}'.format(correct / (correct + incorrect), correct, incorrect))


def calculate_manhattan_accuracy(X_train, y_train, X_test, y_test):
    correct, incorrect = 0, 0
    for x, y in zip(X_test, y_test):
        distances = []
        for x_db in X_train:
            distances.append(cityblock(x_db, x))
        min_index = np.argmin(distances)
        if y == y_train[min_index]:
            correct += 1
        else:
            incorrect += 1
    print('Accuracy: {}, Correct: {}, Incorrect: {}'.format(correct / (correct + incorrect), correct, incorrect))


def draw_landmarks(image, landmarks):
    for i in range(68):
        x, y = landmarks[i]
        cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

    cv2.imwrite('saved/landmarks/{}.jpg'.format(uuid.uuid4()), image)


def check_images(X, y):
    for idx, (img, label) in enumerate(zip(X, y)):
        if not os.path.exists('saved/' + str(label)):
            os.makedirs('saved/' + str(label))
        cv2.imwrite('saved/{}/{}.jpg'.format(label, idx), img)


def compute_covariance_matrix(X):
    X = np.array(X)
    mean = np.mean(X, axis=0)
    X_centered = X - mean
    covariance_matrix = np.dot(X_centered.T, X_centered) / (X.shape[0] - 1)
    return covariance_matrix, mean


def calculate_knn_accuracy(X_train, y_train, X_test, y_test, n_neighbors=1, metric='euclidean'):
    knn = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=n_neighbors, metric=metric))
    knn.fit(X_train, y_train)
    y_pred = knn.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy * 100} %')


def calculate_cosine_accuracy(X_train, y_train, X_test, y_test):
    correct, incorrect = 0, 0
    for x, y in zip(X_test, y_test):
        distances = []
        for x_db in X_train:
            distances.append(cosine(x_db, x))
        min_index = np.argmin(distances)
        if y == y_train[min_index]:
            correct += 1
        else:
            incorrect += 1
    print('Accuracy: {}, Correct: {}, Incorrect: {}'.format(correct / (correct + incorrect), correct, incorrect))


def resize_image_to_height(image, new_height):
    original_height, original_width = image.shape[:2]
    aspect_ratio = original_width / original_height
    new_width = int(new_height * aspect_ratio)
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    return resized_image


def calculate_mahalanobis_accuracy(X_train, y_train, X_test, y_test):
    correct, incorrect = 0, 0
    covariance_matrix, mean = compute_covariance_matrix(X_train)
    inv_cov_matrix = np.linalg.pinv(covariance_matrix)

    for x, y in zip(X_test, y_test):
        distances = []
        for x_db in X_train:
            distances.append(mahalanobis(x_db, x, inv_cov_matrix))
        min_index = np.argmin(distances)
        if y == y_train[min_index]:
            correct += 1
        else:
            incorrect += 1
    print('Accuracy: {}, Correct: {}, Incorrect: {}'.format(correct / (correct + incorrect), correct, incorrect))


def calculate_acc(X_train, y_train, X_test, y_test, t_factor):
    corr, neg = 0, 0
    X_train = np.array(X_train)
    y_test = np.array(y_test)
    X_test = np.array(X_test)
    y_train = np.array(y_train)
    for label in np.unique(y_train):
        data = X_train[y_train == label]
        test_correct = X_test[y_test == label]
        test_n_correct = X_test[y_test != label]
        mean_v = np.mean(data, axis=0)
        distances = []
        for vector in data:
            distances.append(euclidean(mean_v, vector))
        treshold = t_factor * max(distances)
        for test_v in test_correct:
            if euclidean(test_v, mean_v) < treshold:
                corr += 1
            else:
                neg += 1
        for test_v in test_n_correct:
            if euclidean(test_v, mean_v) < treshold:
                neg += 1
            else:
                corr += 1

    print('Correct: {}, not correct: {}, acc: {}, factor: {}'.format(corr, neg, corr/(corr + neg), t_factor))


def calculate_acc_manh(X_train, y_train, X_test, y_test, t_factor):
    corr, neg = 0, 0
    X_train = np.array(X_train)
    y_test = np.array(y_test)
    X_test = np.array(X_test)
    y_train = np.array(y_train)
    for label in np.unique(y_train):
        data = X_train[y_train == label]
        test_correct = X_test[y_test == label]
        test_n_correct = X_test[y_test != label]
        mean_v = np.mean(data, axis=0)
        distances = []
        for vector in data:
            distances.append(cityblock(mean_v, vector))
        treshold = t_factor * max(distances)
        for test_v in test_correct:
            if cityblock(test_v, mean_v) < treshold:
                corr += 1
            else:
                neg += 1
        for test_v in test_n_correct:
            if cityblock(test_v, mean_v) < treshold:
                neg += 1
            else:
                corr += 1

    print('Correct: {}, not correct: {}, acc: {}, factor: {}'.format(corr, neg, corr/(corr + neg), t_factor))


def calculate_acc_cos(X_train, y_train, X_test, y_test, t_factor):
    corr, neg = 0, 0
    X_train = np.array(X_train)
    y_test = np.array(y_test)
    X_test = np.array(X_test)
    y_train = np.array(y_train)
    for label in np.unique(y_train):
        data = X_train[y_train == label]
        test_correct = X_test[y_test == label]
        test_n_correct = X_test[y_test != label]
        mean_v = np.mean(data, axis=0)
        distances = []
        for vector in data:
            distances.append(cosine(mean_v, vector))
        treshold = t_factor * max(distances)
        for test_v in test_correct:
            if cosine(test_v, mean_v) < treshold:
                corr += 1
            else:
                neg += 1
        for test_v in test_n_correct:
            if cosine(test_v, mean_v) < treshold:
                neg += 1
            else:
                corr += 1

    print('Correct: {}, not correct: {}, acc: {}, factor: {}'.format(corr, neg, corr/(corr + neg), t_factor))


if __name__ == '__main__':
    X, y = load_dataset()
    check_images(X, y)
    X_train, X_test, y_train, y_test = create_database(X, y)
    X_train_d, X_test_d, y_train_d, y_test_d = create_database_for_distances(X, y)
    calculate_knn_accuracy(X_train, y_train, X_test, y_test, n_neighbors=1, metric='cosine')  # Euclidean distance

    calculate_knn_accuracy(X_train, y_train, X_test, y_test, n_neighbors=1, metric='manhattan')  # Euclidean distance
    calculate_knn_accuracy(X_train, y_train, X_test, y_test, n_neighbors=1)  # Euclidean distance
    calculate_knn_accuracy(X_train, y_train, X_test, y_test, n_neighbors=3, metric='cosine')  # Euclidean distance
    calculate_knn_accuracy(X_train, y_train, X_test, y_test, n_neighbors=3, metric='manhattan')  # Euclidean distance
    calculate_knn_accuracy(X_train, y_train, X_test, y_test, n_neighbors=3)  # Eucl
    t_factor = 1.0
    while (t_factor < 1.3):
        calculate_acc(X_train, y_train, X_test, y_test, t_factor)
        calculate_acc_manh(X_train, y_train, X_test, y_test, t_factor)
        calculate_acc_cos(X_train, y_train, X_test, y_test, t_factor)
        t_factor += 0.05


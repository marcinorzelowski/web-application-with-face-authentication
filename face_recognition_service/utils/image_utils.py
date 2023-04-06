import math

import cv2
import numpy as np


def calculate_distance_between_eyes(landmarks):
    left_eye_center = ((landmarks.part(39).x - landmarks.part(36).x) / 2,
                       (landmarks.part(39).y - landmarks.part(36).y) / 2)
    righ_eye_center = ((landmarks.part(42).x - landmarks.part(45).x) / 2,
                       (landmarks.part(42).y - landmarks.part(45).y) / 2)
    return math.dist(left_eye_center, righ_eye_center)


def calculate_distance_on_landmark(landmark, start, end):
    return math.dist((landmark.part(start).x, landmark.part(start).y),
                     (landmark.part(end).x, landmark.part(end).y))


def preprocess_image(self, image, face_rect):
    x, y, w, h = face_rect
    # Crop to the face region
    padding = 1.1
    face_img = image[y:y + int(h * padding), x:x + int(w * padding)]
    height, width = face_img.shape[:2]
    img_size = max(height, width)
    black_image = np.zeros((img_size, img_size, 3), dtype=np.uint8)

    black_image[0:height, 0:width] = face_img

    result = cv2.resize(black_image, (200, 200))

    return result

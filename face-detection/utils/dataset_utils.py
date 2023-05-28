import os
import cv2
import numpy as np

new_image_size = 60
cropped_image_size = (24, 24)


# DATASET CREATION METHODS
def read_wider_annotations(annotations_path):
    with open(annotations_path, 'r') as file:
        lines = file.readlines()

    annotations = {}
    idx = 0
    while idx < len(lines):
        image_file = lines[idx].strip()
        num_faces = int(lines[idx + 1].strip())
        face_coords = []
        if (num_faces == 0):
            num_faces += 1
        for i in range(num_faces):
            coords = list(map(int, lines[idx + 2 + i].strip().split()))
            x, y, w, h = coords[0], coords[1], coords[2], coords[3]
            face_coords.append((x, y, w, h))

        annotations[image_file] = face_coords
        idx += 2 + num_faces

    return annotations


def get_non_faces_images(annotations, stride):
    i = 0
    for key in annotations.keys():
        img = cv2.imread('raw_data/images/' + key, cv2.COLOR_BGR2GRAY)
        bounding_boxes = annotations.get(key)
        non_faces_parts = get_non_faces_parts(bounding_boxes, img, stride)
        for non_face_img in non_faces_parts:
            resized = cv2.resize(non_face_img, cropped_image_size)
            cv2.imwrite('dataset/negative/' + str(i) + '.jpg', resized)
            if i % 100 == 0:
                print('Created {} new images'.format(i))
            i += 1

        if i > 30000:
            break


def get_faces_images(path):
    for i, file in enumerate(os.listdir(path)):
        img = cv2.imread('raw_data/faces/' + str(file), cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(img, cropped_image_size)
        cv2.imwrite('dataset/positive/' + str(i) + '.jpg', resized)


def is_overlapping_boxes(x, y, bounding_boxes):
    for box in bounding_boxes:
        x2, y2, width, height = box
        if (x2 <= x <= (x2 + width) or x <= x2 <= (x + new_image_size)) and (
                y2 <= y <= (y2 + height) or y <= y2 <= (y + new_image_size)):
            return True
    return False

def is_stick_to_the_box(x, y, bounding_boxes):
    for box in bounding_boxes:
        x2, y2, width, height = box
        stick_horizontally = x + new_image_size == x2 or x2 + width == x
        stick_vertically = y + new_image_size == y2 or y2 + height == y
        if stick_vertically or stick_horizontally:
            return True
    return False



def get_non_faces_parts(bounding_boxes, img, stride):
    image_height, image_width = img.shape[:2]
    cropped_images = []
    for y in range(0, image_height - new_image_size, stride):
        for x in range(0, image_width - new_image_size, stride):
            if not is_overlapping_boxes(x, y, bounding_boxes) and is_stick_to_the_box(x, y, bounding_boxes):
                cropped = img[y:y + new_image_size, x:x + new_image_size]
                cropped_images.append(cropped)

    return cropped_images


def load_dataset(n_pos_images, n_neg_images):
    X, y = [], []
    for i in range(n_neg_images):
        img = cv2.imread('dataset/negative/' + str(i+20000) + '.jpg', cv2.IMREAD_GRAYSCALE)
        X.append(img)
        y.append(0)
    for i in range(n_pos_images):
        img = cv2.imread('dataset/positive/' + str(i+10000) + '.jpg', cv2.IMREAD_GRAYSCALE)
        X.append(img)
        y.append(1)
    return np.array(X), np.array(y)

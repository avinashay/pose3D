import cv2
import numpy as np
import os

def import_and_read_images(data_path):
    left_path = os.path.join(data_path, 'image_2')
    right_path = os.path.join(data_path, 'image_3')
    for filename in os.listdir(left_path):
        left_img = cv2.imread(os.path.join(left_path, filename))
    for filename in os.listdir(right_path):
        right_img = cv2.imread(os.path.join(right_path, filename))

    return left_img, right_img

def visualize_images(left_image, right_image):
    cv2.imshow('left', left_image)
    cv2.imshow('right', right_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def read_labels(data_path):
    labels_list = []
    label_path = os.path.join(data_path, 'labels')
    for filename in os.listdir(label_path):
        with open(os.path.join(label_path, filename)) as f:
            lines = f.read().splitlines()
            for line in lines:
                label = line.split(' ')
                label_details = {}
                label_details['type'] = label[0]
                label_details['truncated'] = float(label[1])
                label_details['occluded'] = int(label[2])
                label_details['alpha'] = float(label[3])
                label_details['bbox'] = np.array(label[4:8], dtype=np.float64)
                label_details['dimensions'] = np.array(label[8:11], dtype=np.float64)
                label_details['location'] = np.array(label[11:14], dtype=np.float64)
                label_details['rotation_y'] = float(label[14])
                # print(label_details)
                labels_list.append(label_details)

    return labels_list

def visulaize_labels(image_left, labels_list):

    for label in labels_list:
        bbox = label['bbox']
        label_type = label['type']
        start = (int(bbox[0]), int(bbox[1]))
        end = (int(bbox[2]), int(bbox[3]))
        text_position = (start[0], start[1] - 10)
        cv2.rectangle(image_left,start,end, (255, 0, 0), 2)
        cv2.putText(image_left, label_type, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow('image', image_left)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def read_calib_file(data_path):
    calib_path = os.path.join(data_path, 'calib')
    for filename in os.listdir(calib_path):
        with open(os.path.join(calib_path, filename)) as f:
            lines = f.read().splitlines()
            calib_details = {}
            calib_details['P2'] = np.asarray(lines[2].split(' ')[1:], dtype=np.float64).reshape(3, 4)
            calib_details['P3'] = np.asarray(lines[3].split(' ')[1:], dtype=np.float64).reshape(3, 4)
            calib_details['R0_rect'] = np.asarray(lines[4].split(' ')[1:], dtype=np.float64).reshape(3, 3)
        # print(calib_details)

    return calib_details

def main():
    data_path = './kitti_test'
    left_image, right_image = import_and_read_images(data_path)
    visualize_images(left_image, right_image)
    labels_list = read_labels(data_path)
    visulaize_labels(left_image, labels_list)
    calib_details = read_calib_file(data_path)

if __name__ == '__main__':
    main()
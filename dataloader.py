import cv2
import numpy as np
import os

def import_and_read_left_images(data_path):
    left_path = os.path.join(data_path, 'image_2')
    left_imgs = []
    for filename in sorted(os.listdir(left_path)):
        left_imgs.append(cv2.imread(os.path.join(left_path, filename)))
    return left_imgs

def read_labels(data_path):
    labels_list = []
    label_path = os.path.join(data_path, 'labels')
    for filename in sorted(os.listdir(label_path)):
        image_labels = []
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
                image_labels.append(label_details)
        labels_list.append(image_labels)
    return labels_list

def visulaize_2D_bbox(images_left, labels_list):

    for image_left, labels in zip(images_left, labels_list):
        for label in labels:
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

def read_calib_files(data_path):
    calib_path = os.path.join(data_path, 'calib')
    calib_list = []
    for filename in sorted(os.listdir(calib_path)):
        with open(os.path.join(calib_path, filename)) as f:
            lines = f.read().splitlines()
            calib_details = {}
            calib_details['P2'] = np.asarray(lines[2].split(' ')[1:], dtype=np.float64).reshape(3, 4)
            calib_details['P3'] = np.asarray(lines[3].split(' ')[1:], dtype=np.float64).reshape(3, 4)
            calib_details['R0_rect'] = np.asarray(lines[4].split(' ')[1:], dtype=np.float64).reshape(3, 3)
        # print(calib_details)
        calib_list.append(calib_details)
    return calib_list

def get_3d_bbox_corners(location, dimensions, rotation_y):
    h, w, l = dimensions
    rotation_y = rotation_y
    # 3D bounding box corners
    x_corners = [l/2, l/2, -l/2, -l/2, l/2, l/2, -l/2, -l/2]
    y_corners = [0,0,0,0,-h,-h,-h,-h]
    z_corners = [w/2, -w/2, -w/2, w/2, w/2, -w/2, -w/2, w/2]
    corners_3d = np.array([x_corners, y_corners, z_corners])

    # rotation matrix
    rotation_matrix = np.array([[np.cos(rotation_y), 0, np.sin(rotation_y)],
                                 [0, 1, 0],
                                 [-np.sin(rotation_y), 0, np.cos(rotation_y)]])
    corners_3d = np.dot(rotation_matrix, corners_3d)
    corners_3d += np.array(location).reshape(3, 1)

    return [corners_3d[:, 0], corners_3d[:, 1], corners_3d[:, 2], corners_3d[:, 3], corners_3d[:, 4], corners_3d[:, 5], corners_3d[:, 6], corners_3d[:, 7]]

def draw_cuboid(image, points):
    # Define the indices of points to connect
    lines = np.array([
        [0, 1], [1, 2], [2, 3], [3, 0],  # Base
        [4, 5], [5, 6], [6, 7], [7, 4],  # Top
        [0, 4], [1, 5], [2, 6], [3, 7]   # Sides
    ])
    # Draw all the lines using a single loop
    for line in lines:
        pt1 = tuple(points[line[0]])
        pt2 = tuple(points[line[1]])
        cv2.line(image, pt1, pt2, (255, 0, 0), 2)

def plot_3d_bbox(images_left, labels_list, calib_list):

    if not os.path.exists('./kitti_test/output'):
            os.makedirs('./kitti_test/output')
    video = cv2.VideoWriter('kitti_test/output/output.avi', cv2.VideoWriter_fourcc(*'DIVX'), 5, (images_left[0].shape[1], images_left[0].shape[0]))
    for image_left, labels, calib_details in zip(images_left, labels_list, calib_list):
        for label in labels:
            location = label['location']
            dimensions = label['dimensions']
            rotation_y = label['rotation_y']
            cuboid_points = get_3d_bbox_corners(location, dimensions, rotation_y)
            p2 = calib_details['P2']
            image_frame_location = np.dot(p2, np.array([location[0], location[1], location[2], 1]))
            image_frame_location = image_frame_location / image_frame_location[2]
            object_point = (int(image_frame_location[0]), int(image_frame_location[1]))

            #convert cuboid points to image pixels
            for i in range(len(cuboid_points)):
                cuboid_points[i] = np.dot(p2, np.array([cuboid_points[i][0], cuboid_points[i][1], cuboid_points[i][2], 1]))
                cuboid_points[i] = cuboid_points[i] / cuboid_points[i][2]
                cuboid_points[i] = (int(cuboid_points[i][0]), int(cuboid_points[i][1]))
            # print(cuboid_points)
            cv2.circle(image_left, object_point, 5, (0,0,255), -1)
            #Write the label on the image
            bbox = label['bbox']
            label_type = label['type']
            start = (int(bbox[0]), int(bbox[1]))
            text_position = (start[0], start[1] - 10)
            cv2.putText(image_left, label_type, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255,0), 2)
            draw_cuboid(image_left, cuboid_points)
        image_left = cv2.resize(image_left, (images_left[0].shape[1], images_left[0].shape[0]))
        video.write(image_left)
    cv2.destroyAllWindows()
    video.release()


def main():
    data_path = './kitti_test'
    left_images = import_and_read_left_images(data_path)
    labels_list = read_labels(data_path)
    # visulaize_2D_bbox(left_images, labels_list)
    calib_list = read_calib_files(data_path)
    plot_3d_bbox(left_images, labels_list, calib_list)

if __name__ == '__main__':
    main()
# pose3D

Repository to perform 3D Object Detection on the KITTI dataset (WIP).

## Dataset Description

The data for training and testing can be found in the corresponding folders.
The sub-folders are structured as follows:

  - image_02/ contains the left color camera images (png)
  - label_02/ contains the left color camera label files (plain text files)
  - calib/ contains the calibration for all four cameras (plain text file)

In the label text file, all values (numerical or strings) are separated via spaces,
each row corresponds to one object. The 15 columns represent:

| Values | Name        | Description                                                                 |
|--------|-------------|-----------------------------------------------------------------------------|
| 1      | type        | Describes the type of object: 'Car', 'Van', 'Truck', 'Pedestrian', 'Person_sitting', 'Cyclist', 'Tram', 'Misc', or 'DontCare' |
| 1      | truncated   | Float from 0 (non-truncated) to 1 (truncated), where truncated refers to the object leaving image boundaries |
| 1      | occluded    | Integer (0, 1, 2, 3) indicating occlusion state: 0 = fully visible, 1 = partly occluded, 2 = largely occluded, 3 = unknown |
| 1      | alpha       | Observation angle of object, ranging [-π..π]                                  |
| 4      | bbox        | 2D bounding box of object in the image (0-based index): contains left, top, right, bottom pixel coordinates |
| 3      | dimensions  | 3D object dimensions: height, width, length (in meters)                      |
| 3      | location    | 3D object location x, y, z in camera coordinates (in meters)                 |
| 1      | rotation_y  | Rotation ry around Y-axis in camera coordinates [-π..π]                      |
| 1      | score       | Only for results: Float, indicating confidence in detection, needed for precision/recall curves, higher is better |
### Object-detection-yolov8

Brief:
* Object detection refers to locating the instances of objects in an image. A
bounding box is drawn around the identified instances to signify the detection.
* YOLO- (You Only Look Once) is an object detection algorithm. It treats the
problem as a regression problem than a classification problem. It has 4 steps:
  * Dividing the input image into NxN grid cells
  * Bounding box regression- to determine the cell with the object in it
  * IOU- Intersection over union to determine the relevant bounding box
  * Non Maximum Suppression- To eliminate poorly drawn boxes

Tools Used:
* Libraries: numpy, argparse, Ultralytics, OpenCV, PIL, python-xml

Dataset:
* The dataset contains 416 images (.jpg) and 416 annotations (.xml) used for ppedetection task. There are 10 classes in this dataset.

Approach:
1. The given dataset had images and their respective annotations. The annotations
were in PascalVOC (Visual Object Classes) format. It has the data of the objects
and metadata of the respective image. It is organized hierarchically and saved as
an .xml file.
2. To make inference with YOLO, the annotations must be in .txt and the syntax of
the data should be as per yolo’s format: _<class_id, x_c, y_c, width, height>_, where
_width_ and _height_ are the width and height of the bounding box, _(x_c, y_c)_ are the
coordinates of the center of the bounding box for the object with class class_id.
![data](https://github.com/sanjay-906/Object-detection-yolov8/assets/99668976/fb7f374b-a8a5-42a1-9d26-086cbfc9725f)
3. To read the .xml file, python’s in-built xml package was used to parse all the data.
For each object in the image, xml stores the coordinates of the bounding box (top
left coordinates _(x_min, y_min)_ and bottom right coordinates _(x_max, y_max)_. The
names of the objects were mapped with class_ids. These were then converted
into yolo’s intended format.
![boxes](https://github.com/sanjay-906/Object-detection-yolov8/assets/99668976/6e9e9489-b617-4be2-a956-2241c3f3f911)
4. The first step is **person-detection**. A copy of annotation files were created such
that they only have the data about the “person” class. Other class details were
excluded.
5. These images and new annotations were split into training and validation sets.
6. Yolov8-nano is trained using this data with image size: 640x640 and batch-size:
32. The hyperparameters were automatically chosen by the model.
7. After the training, the weights were used to create a new dataset for the second
task- **ppe-detection**. The trained model detected “person” from each image and
saved these images separately. Now, new annotations were created for each of
these images. These annotations contain the new coordinates with respect to the
cropped images. These annotations had the remaining 9 classes.
![1](https://github.com/sanjay-906/Object-detection-yolov8/assets/99668976/7f30e1de-ffdb-4c6b-b4e2-37a76ab68d53)
![explaination](https://github.com/sanjay-906/Object-detection-yolov8/assets/99668976/eda97f5d-1f20-4975-8ccf-fd7ad611abe6)
8. The new data has 1227 images (1227 persons from 416 images) and 1227
annotations with utmost 9 classes in each.
9. These annotations were again converted into yolov8 format and now the dataset
is split into train and test. This is now trained for to detecting ppe- objects. Both
yolov8-nano and yolov8-medium sizes were considered for training process.

Inference:
* **pascalVOC_to_yolo.py** takes input directory (annotations) with xml files and an
output directory. It converts all the files in the input directory into yolo v8 type
and saves them in the given output location.
* **inference.py** takes input directory (images), output directory, person-detectionmodel’s weights’ path and ppe-detection-model’s weight’s path. This python
script detects the person instance in each image, crops them and keep them and
stored aside. Then bounding boxes are drawn on the original image and this
image is saved. Now the cropped images which were stored aside are taken, and
passed to the ppe-detection model to detect the ppe-objects for each of the
cropped image (on each person). Now bounding boxes are drawn using
OpenCV’s text and rectangle functions and this image is saved.

Testing:

![output](https://github.com/sanjay-906/Object-detection-yolov8/assets/99668976/f2911ebf-7c60-4f75-9313-7c1f3cd420ee)

Results:

Note: person-detection task was also performed with yolov8 medium and it showed
almost similar results compared to nano model, except it was achieved in fewer epochs

|    <br>Model                  |    <br>Person-det (nano)    |    <br>Ppe-det (nano)    |    <br>Ppe-det (medium)    |
|-------------------------------|-----------------------------|--------------------------|----------------------------|
|    <br>Precision              |    <br>0.949                |    <br>0.796             |    <br>0.854               |
|    <br>Recall                 |    <br>0.91                 |    <br>0.514             |    <br>0.528               |
|    <br>mAP50                  |    <br>0.978                |    <br>0.646             |    <br>0.604               |
|    <br>mAP50-95               |    <br>0.76                 |    <br>0.448             |    <br>0.435               |
|    <br>Inference time (ms)    |    <br>1.9                  |    <br>1.8               |    <br>8.4                 |
|    <br>Weights size (mb)      |    <br>5.95                 |    <br>5.92              |    <br>49.5                |

Try out:

```
  pascalVOC_to_yolo.py --ip_dir INPUT_DIR_PATH --op_dir OUTPUT_DIR_PATH
```
where,
- INPUT_DIR_PATH: folder which has all the .xml files
- OUTPUT_DIR_PATH: where you would want to store the annotated .txt files

note: 
- if OUTPUT_DIR_PATH doesn't exist, it will be created

```
  inference.py --ip_dir IP_PATH op_dir OP_PATH --person_det_model WEIGHTS_PERSON --ppe_det_model WEIGHTS_PPE
```
where,
- IP_PATH: folder which has the images
- OP_PATH: where you would wan to save the detected object images
- WEIGHTS_PERSON: name of weight file of the person-detection model
- WEIGHTS_PPE: name of weight file of the ppe-detection model

note: 
- if OP_PATH doesn't exist, it will be created
- WEIGHTS_PERSON and WEIGHTS_PPE are not just paths, but path+name. 

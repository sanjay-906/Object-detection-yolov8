import argparse
import os
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image



#check path validity
def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"{path} is not valid/ does not exist")

# define argarse for getting input from command line
parser= argparse.ArgumentParser()
parser.add_argument("--ip_dir", type= dir_path, required= True)
parser.add_argument("--op_dir", required= True)
parser.add_argument("--person_det_model", required= True)
parser.add_argument("--ppe_det_model", required= True)

args= parser.parse_args()

#create path if it doesnt exist
if not os.path.exists(args.op_dir):
    os.makedirs(args.op_dir)

# get data from command line arguments
base_ip= os.path.abspath(args.ip_dir)
base_op= os.path.abspath(args.op_dir)
base_person_model= os.path.abspath(args.person_det_model)
base_ppe_model= os.path.abspath(args.ppe_det_model)

#initialize the models
person_det_model= YOLO(base_person_model)
ppe_det_model= YOLO(base_ppe_model)

ppe_classes= ['hard-hat', 'gloves', 'mask', 'glasses', 'boots', \
'vest', 'ppe-suit', 'ear-protector', 'safety-harness']

#store croppped images
people= []

'''
Step 1: Person Detection
'''
for file in os.listdir(base_ip):
    img1= cv2.imread(base_ip+ "/"+ file)
    img1= cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    #store the coordinates of the person detected for every image
    coordinates= {}
    result= person_det_model.predict(img1)
    #copy the image to prevent bounding boxes being drawn on cropped images
    temp= result[0].orig_img.copy()
    for i,c in enumerate(result[0].boxes):
        if person_det_model.names[int(c.cls)]== "person":
            class_name = person_det_model.names[int(c.cls)]
            x1, y1, x2, y2 = map(int, c.xyxy[0])
            coordinates[i]= [x1,y1,x2,y2]
            image= result[0].orig_img
            # draw boxes and put the label
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(image, class_name, (x1, y1+ 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # save the image with boxes drawn on each person
    im= Image.fromarray(image)
    im.save(base_op+"/"+file[:-4]+".jpg")

    #for each "person" in that image, crop the "person" and store it in "people"
    for i in coordinates:
        instance= temp[coordinates[i][1]:coordinates[i][3],coordinates[i][0]:coordinates[i][2]]
        people.append(instance)

'''
Step 2: PPE Detection
'''
for i, person in enumerate(people):
    result= ppe_det_model.predict(person)
    image= result[0].orig_img
    # for each ppe object in person image
    for c in result[0].boxes:
        if ppe_det_model.names[int(c.cls)] in ppe_classes:
            class_name = ppe_det_model.names[int(c.cls)]
            x1, y1, x2, y2 = map(int, c.xyxy[0])

            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(image, class_name, (x1, y1+ 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    #save image after drawing all ppe objects
    im= Image.fromarray(image)
    im.save(base_op+"/"+"object"+str(i)+".jpg")

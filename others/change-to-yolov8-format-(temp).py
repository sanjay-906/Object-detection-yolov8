'''
This code file is for annotating objects of ppe-detection task

step 1: comment the return values of the function "_get_yolov8_type_data"
in "pascal2Yolo.py", instead return the original xml data

step 2: use that annotations to find annotations of the objects in the
cropped images by shifting origin (this python script does that)

step 3: use the new annotations and run "pascalVOC_to_yolo.py" to create
yolo's format annotations.

'''
import os
import cv2
import numpy as np
base= "C:/Users/Admin/Desktop/datasets/ppe-detection"

if not os.path.exists(base+"/final-annotations"):
    os.mkdir(base+"/final-annotations")

unclassified= []
for file in os.listdir(base+ "/annotations"):
    filename= file[:-4]
    try:
        temp_path= base+"/annotations"+"/"+filename+".txt"
        img1= cv2.imread(base+"/images"+"/"+filename+".jpg")
        height, width, _= img1.shape
    except:
        unclassified.append(temp_path)
        continue

    with open(base+"/annotations/"+filename+".txt") as fin:
        detections=""
        values= fin.readlines()
        for line in values:
            values= line.strip('\n')
            points= [int(i) for i in values.split(' ') if i!='']
            x_min= points[1]
            y_min= points[3]
            x_max= points[2]
            y_max= points[4]

            x_c= (x_min+ x_max)/2
            x_c/= width
            x_c= "%.4f" % round(x_c,4)

            y_c= (y_min+ y_max)/ 2
            y_c/= height
            y_c= "%.4f" % round(y_c,4)

            box_width= "%.4f" % round((x_max- x_min)/width, 4)
            box_height= "%.4f" % round((y_max- y_min)/height, 4)

            detections+=str(points[0])+" "+str(x_c)+" "+str(y_c)+" "+str(box_width)+" "+str(box_height)+"\n"
        with open(base+ "/final-annotations/"+ filename+".txt", "w") as fout:
            fout.write(detections)

for i in unclassified:
    os.remove(i)

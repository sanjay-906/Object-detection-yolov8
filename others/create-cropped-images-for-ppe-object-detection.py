#note: order of arguments is wrong in line 73, this has been fixed in "change-to-yolov8format-(temp).py in line 39"

import os
from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

result_dir= "C:/Users/Admin/Desktop/datasets/ppe-detection"
data= "C:/Users/Admin/Desktop/datasets"

if not os.path.exists(result_dir):
    os.mkdir(result_dir)
    os.mkdir(result_dir+"/images")
    os.mkdir(result_dir+"/annotations")

def crop_images_and_create_new_object_annotations(filename):
    img1= cv2.imread(data+"/images"+"/"+filename+".jpg")
    img1= cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)

    model = YOLO('best.pt')
    label= ['person']
    result= model.predict(img1)
    #k=0
    for i,c in enumerate(result[0].boxes):
        if model.names[int(c.cls)] in label:
            class_name = model.names[int(c.cls)]
            x1, y1, x2, y2 = map(int, c.xyxy[0])

            #crop the image, so that the image has only "person" object
            image= result[0].orig_img
            image= image[y1:y2, x1:x2]
            cropped_img = Image.fromarray(image)


            def clamp(n, smallest, largest):
                return max(smallest, min(n, largest))

            with open(data+"/annotations/"+filename+".txt","r") as fin:
                values= fin.readlines()
                detections=""
                for line in values:
                    if(line.strip('\n')[0]!='0'):
                        values= line.strip('\n')
                        points= [int(i) for i in values.split(' ') if i!='']

                        #xmin= points[1], ymin= points[2], xmax= points[3], ymax= points[4]
                        '''if coordinates lie inside the detected are i.e., object is on the person
                        (for e.g. person wearing a hard-hat)
                        '''
                        if(points[1]>=x1 and points[3]<=x2 and points[2]>=y1 and points[4]<=y2):
                            x_1= points[1]-x1
                            y_1= points[2]-y1
                            x_2= points[3]-x1
                            y_2= points[4]-y1
                        #else include only the area within the detected area
                        else:
                            x_1= clamp(points[1]-x1, 0, x2-x1)
                            y_1= clamp(points[2]-y1, 0, y2-y1)
                            x_2= clamp(points[3]-x1, 0, x2-x1)
                            y_2= clamp(points[4]-y1, 0, y2-y1)

                        try:
                            '''
                            if the relocated object coordinates doesnt fall inside the image's area
                            this block will throw an error because that object doesnt belong to
                            this person..maybe other person is wearing/holding it
                            '''
                            temp= image[y_1:y_2, x_1:x_2]
                            im = Image.fromarray(temp)

                            detections+=str(points[0])+" "+str(x_1)+" "+str(x_2)+" "+str(y_1)+" "+str(y_2)+"\n"
                            #image cropped to object
                            #im.save(result_dir+"/images/"+filename+str(k)+".jpg")
                            cropped_img.save(result_dir+"/images/"+filename+str(i)+".jpg")
                        except:
                            pass
                        #k+=1
                '''
                for each person detected, create a annotation file which has objects inside
                the detected person area
                '''
                with open(result_dir+"/annotations/"+filename+str(i)+".txt","w") as fout:
                    fout.write(detections)

'''
for each image, detect the people, crop them and create an annoted file which has
objects for that person and save both of these
'''
for t,file in enumerate(os.listdir(data+"/images")):
    filename= file[:-4]
    crop_images_and_create_new_object_annotations(filename)
    print(t," done")



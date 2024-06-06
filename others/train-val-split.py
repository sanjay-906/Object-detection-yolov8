import os
from random import shuffle


#person-detection
'''
label_dir= "C:/Users/Admin/Desktop/datasets/person_class"
image_dir= "C:/Users/Admin/Desktop/datasets/images"
split= 400
data= "C:/Users/Admin/Desktop/datasets/person-detection"
'''

#ppe-detection
label_dir= "C:/Users/Admin/Desktop/datasets/ppe-detection/final-annotations"
image_dir= "C:/Users/Admin/Desktop/datasets/ppe-detection/images"
split=1127
data= "C:/Users/Admin/Desktop/datasets/ppe-detection"


parent= ["train", "val"]
child=["images", "labels"]

#create directories
if not os.path.exists(data):
    os.mkdir(data)
for i in parent:
    if not os.path.exists(os.path.join(data+"/"+i)):
        os.mkdir(os.path.join(data+"/"+i))
        for j in child:
            if not os.path.exists(os.path.join(data+"/"+i+"/"+j)):
                os.mkdir(os.path.join(data+"/"+i+"/"+j))

#store filenames
names= []
for filename in os.listdir(image_dir):
    names.append(filename[:-4])

#not necessary
shuffle(names)

#move files into train and val folders (split the dataset)
for i, file in enumerate(names):
    if i<split:
        os.replace(image_dir+"/"+file+".jpg", data+"/train/images/"+file +".jpg")
        os.replace(label_dir+"/"+file+".txt", data+"/train/labels/"+file +".txt")
    else:
        os.replace(image_dir+"/"+file+".jpg", data+"/val/images/"+file +".jpg")
        os.replace(label_dir+"/"+file+".txt", data+"/val/labels/"+file +".txt")

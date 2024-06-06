'''
Created annotated files such that it has only "person" class.
Use those to train person-detection model
'''

import os
#this folder has the .txt annotated files where each file could have more than 1 classes
path= "C:/Users/Admin/Desktop/datasets/annotations"
#this folder will have annotated files but only for the class "person"
person_class= "C:/Users/Admin/Desktop/datasets/person_class"

if not os.path.exists(person_class):
    os.makedirs(person_class)

for file in os.listdir(path):
    with open(path+"/"+file,'r') as fin:
        data= fin.readlines()
        with open(person_class+"/"+file,"w") as fout:
            for line in data:
                if(line.strip('\n')[0]=='0'):
                    fout.write(line)

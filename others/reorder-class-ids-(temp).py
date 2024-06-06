'''
class_ids should start from 0 for yolo,
since class 0 is "person" and we are doing ppe detection,
the class ids must be reordered. This script does that
'''

import os
base= "C:/Users/Admin/Desktop/datasets/ppe-detection/final-annotations"

for file in os.listdir(base):
    with open(base+"/"+file, 'r') as fin:
        data= fin.read()
        print(data)
        data= data.splitlines()
        new_data=""
        for i in data:
            temp= int(i[0])
            temp-=1
            new_val=str(temp)+i[1:]
            new_data+=new_val+"\n"
        print(new_data)
        with open(base+"/"+file, "w") as fout:
            fout.write(new_data)

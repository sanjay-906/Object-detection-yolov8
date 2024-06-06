'''
YOLOv8 format:

class_id x_center y_center width height
'''

#this file just has the class

import os
import xml.etree.ElementTree as ET

class Pascal2Yolo:
    def __init__(self, path, mappings, op_dir):
        '''
        Initializes the object with path (input path),
        mappings (class name : label mappings) and op_dir
        (path to output directory)
        '''
        self.path= path
        self.op_dir= op_dir
        self.height= None
        self.width= None
        #self.mapping= {}
        self.mapping= mappings

        #with text file:
        '''
        with open(classes, "r") as fin:
            for i, name in enumerate(fin.read().splitlines()):
                self.mapping[name]= i
        '''


    def _get_yolov8_type_data(self, instances):
        '''
        This function takes the coordinates of the bounding box
        and returns the coordinate of the center and length of edges
        '''
        x_min= instances["xmin"]
        y_min= instances["ymin"]
        x_max= instances["xmax"]
        y_max= instances["ymax"]

        x_c= (x_min+ x_max)/2
        x_c/= self.width
        x_c= "%.4f" % round(x_c,4)

        y_c= (y_min+ y_max)/ 2
        y_c/= self.height
        y_c= "%.4f" % round(y_c,4)

        box_width= "%.4f" % round((x_max- x_min)/self.width, 4)
        box_height= "%.4f" % round((y_max- y_min)/self.height, 4)

        #return [x_min, y_min, x_max, y_max]
        return [x_c, y_c, box_width, box_height]

    def _write_text_file(self, data):
        '''
        This function takes the data computed by the
        _get_yolov8_type_data function and puts that data
        into a text file
        '''
        name= os.path.basename(self.path)
        filename= "{}.txt".format(name[:-4])
        with open(self.op_dir+ "/"+ filename, "w") as fout:
            for line in data:
                for obj in line:
                    if obj=="name":
                        fout.write(str(self.mapping[line[obj]])+" ")
                    elif obj=="values":
                        for value in line[obj]:
                            fout.write(str(value)+" ")
                fout.write("\n")
        print("Done")

    def convert(self):
        '''
        When this function is called, it parses the XML file
        and stores that data and calls further helper functions
        for data processing
        '''
        tree= ET.parse(self.path)
        root= tree.getroot()
        self.width= int(root.find('./size/width').text)
        self.height= int(root.find('./size/height').text)

        data= []
        for item in root.findall('./object'):
            instance= {}
            for obj in item:
                if obj.tag=="name":
                    instance[obj.tag]= obj.text
                else:
                    for coordinate in obj:
                        instance[coordinate.tag]= int(coordinate.text)
                    ready_data= self._get_yolov8_type_data(instance)
                    instance["values"]= ready_data

            data.append(instance)

        self._write_text_file(data)

#path= "C:/Users/Admin/Desktop/datasets/labels/-184-_png_jpg.rf.b02963998a79b9ad5079f57b65130bc2.xml"
#classes= "C:/Users/Admin/Desktop/datasets/classes.txt"
#ob= Pascal2Yolo(path, classes)
#ob.convert()

'''
mapping= {
    'person': 0, 'hard-hat': 1,
    'gloves': 2, 'mask': 3,
    'glasses': 4, 'boots': 5,
    'vest': 6, 'ppe-suit': 7,
    'ear-protector': 8, 'safety-harness': 9
}
op_dir= "C:/Users/Admin/Desktop/datasets/annotations"
ob= Pascal2Yolo(path, mapping, op_dir)
ob.convert()
'''

import argparse
import os
from Pascal2Yolo import Pascal2Yolo

# class names: label
mapping= {
    'person': 0, 'hard-hat': 1,
    'gloves': 2, 'mask': 3,
    'glasses': 4, 'boots': 5,
    'vest': 6, 'ppe-suit': 7,
    'ear-protector': 8, 'safety-harness': 9
}

# check if the path is a directory
def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"{path} is not valid/ does not exist")

# define argarse for getting input from command line
parser= argparse.ArgumentParser()
parser.add_argument("--ip_dir", type= dir_path, required= True)
parser.add_argument("--op_dir", required= True)

args= parser.parse_args()

# create output dir if it doesn not exist
if not os.path.exists(args.op_dir):
    os.makedirs(args.op_dir)

base_ip= os.path.abspath(args.ip_dir)
base_op= os.path.abspath(args.op_dir)

# convert all Pascal VOC files into txt files as per yolo v8 format
for file in os.listdir(args.ip_dir):
    path= os.path.join(base_ip,file)
    converter= Pascal2Yolo(path, mapping, base_op)
    converter.convert()


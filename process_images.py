import os
import cv2
from functions import run_mrz

def process_directory(full_path_to_directory):
    image_names = []
    num_images = 0
    for filename in os.listdir(full_path_to_directory):
        img = cv2.imread(os.path.join(full_path_to_directory,filename))
        if img is not None:
            image_names.append(filename)
            num_images = num_images + 1
    if num_images is 0:
        print("Found 0 images in the given directory \nQuitting ...")
    else:
        print("-"*50)
        print("Found {} images in the given directory".format(num_images))
        print("-"*50)
        process_list_of_image_names(image_names, full_path_to_directory)

def process_list_of_image_names(image_names, full_path_to_image_directory):
    if len(image_names) is 0:
        print("Given list of image names is empty \nQuitting ...")
    else:
        run_mrz(image_names, full_path_to_image_directory)

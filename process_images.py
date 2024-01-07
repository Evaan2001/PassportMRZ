import os
import cv2
import functions.py

def process_directory(full_path_to_directory):
    image_names = []
    num_images = 0
    for filename in os.listdir(full_path_to_directory):
        img = cv2.imread(os.path.join(full_path_to_directory,filename))
        if img is not None:
            image_names.append(filename)
            num_images = num_images + 1
    print("-"*50)
    print("Found {} images in the given directory".format(num_images))
    print("-"*50)

def process_list_of_image_names(image_names, full_path_to_image_directory):
    pass

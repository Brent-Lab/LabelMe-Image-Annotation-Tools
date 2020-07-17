import json
import sys
import cv2
import numpy as np
import os
import utilities


def fixJPEG(py_json, name, ext):
    #list of dicts
    shapes_dict = py_json['shapes']
    #list of Dicts with label:objectName   
    object_dict = [d for d in shapes_dict if item_name in d.values()]
    name_of_img_file_to_read = name + ext
    img = cv2.imread(name_of_img_file_to_read, cv2.IMREAD_COLOR)
    for d in object_dict:
        #list of coordinates [x,y]
        #list_points needs to be a numpy array so now np_points
        list_points = d['points']
        np_points = np.array([list_points], dtype=np.int32)
        cv2.fillPoly(img, np_points, (255, 255, 255)) 
    return object_dict, img



def fixJSON(py_json):
    #editing json file
    for element in py_json['shapes']:
        #element and py_json are both dictionary
        if item_name in element.values():
            #remove the dictionary element from the list py_json['shapes']
            py_json['shapes'].remove(element)
    #py_json is new json file          
    return py_json


def moveNewFiles(object_dict, new_img_name, img, json_filename, new_json_filename, py_json):    
    if len(object_dict) > 0:
        utilities.cv2_copy_and_rename_file(src_folder_dir, dest_folder_dir, filename, new_img_name, img)
    else:
        utilities.copy_and_rename_file(src_folder_dir, dest_folder_dir, filename, new_img_name)
    if not os.path.exists(os.path.join(src_folder_dir, json_filename)):
        return
    new_json_dir = os.path.join(dest_folder_dir, new_json_filename)
    with open(new_json_dir, 'w') as data_file:
        py_json = json.dump(py_json, data_file, indent=4)

def editFiles(filename, img_file_count, item_name, name, ext):
    img_file_count += 1
    json_filename = name + ".json"
    # Copy image name
    new_name = "UpdatedPic" + "_" + str(img_file_count)
    new_img_name = new_name + ext
    new_json_filename = new_name + ".json" 

    open_file = open(json_filename, "r")
    py_json = json.load(open_file)
    open_file.close()
    
    object_dict, img = fixJPEG(py_json, name, ext)
    py_json = fixJSON(py_json)
    moveNewFiles(object_dict, new_img_name, img, json_filename, new_json_filename, py_json)
    return img_file_count


if __name__ == '__main__':
    #set up
    src_folder_name = sys.argv[1]
    item_name = sys.argv[2]
    allowed_image_types = (".jpg", ".jpeg")
    work_dir = os.getcwd()
    img_file_count = 0    
    src_folder_dir = os.path.join(work_dir, src_folder_name)
    src_folder_dir = os.path.join(src_folder_dir, '')
    
    #check
    if not os.path.exists(src_folder_dir):
        print(src_folder_dir + " does not exist")
    else: 
        
        #looping through files in folder
        dest_folder_dir = utilities.create_folder(work_dir, "Renamed " + os.path.basename(os.path.dirname(src_folder_dir)))
        #filename = jpg filename
        for filename in os.listdir(src_folder_dir):
            name, ext = os.path.splitext(os.path.join(src_folder_dir, filename))
            #since json and jpg files have same names, once you have jpeg, you also have json
            if ext.endswith(allowed_image_types):
                img_file_count = editFiles(filename, img_file_count, item_name, name, ext)
            elif filename == "trainval.json":
                utilities.copy_and_rename_file(src_folder_dir, dest_folder_dir, filename, filename)
                
            
            
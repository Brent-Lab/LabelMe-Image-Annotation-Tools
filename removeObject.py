#remove_object but python
import json
import sys
import cv2
import numpy as np
import os
import utilities

if __name__ == '__main__':

    src_folder_name = sys.argv[1]
    item_name = sys.argv[2]
    allowed_image_types = (".jpg", ".jpeg")
    work_dir = os.getcwd()
    img_file_count = 0
    
    #TODO: traverse folder and open each file individually
    
    src_folder_dir = os.path.join(work_dir, src_folder_name)
    src_folder_dir = os.path.join(src_folder_dir, '')
    if not os.path.exists(src_folder_dir):
        print(src_folder_dir + " does not exist")
    else:   
    
        dest_folder_dir = utilities.create_folder(work_dir, "Renamed " + os.path.basename(os.path.dirname(src_folder_dir)))
    
        for filename in os.listdir(src_folder_dir):
            name, ext = os.path.splitext(os.path.join(src_folder_dir, filename))
            name, ext = name.lower(), ext.lower()
            #since json and jpg files have same names, once you have jpeg, you also have json
            #so filename = jpg_file_name
            print('processing',name)
            if ext.endswith(allowed_image_types):
                print(name,'type is good')
                img = None
                img_file_count += 1
                json_filename = name + ".json"
                # Copy image #
                new_name = item_name + "_" + str(img_file_count)
                new_img_name = os.path.join(new_name, ext)
                new_json_filename = os.path.join(new_name, ".json" )
    
                #open file
                open_file = open(json_filename, "r")
                py_json = json.load(open_file)
                #pull points for object to change
                #list of dicts
                shapes_dict = py_json['shapes']
                #list of Dicts with label:objectName   
                object_dict = [d for d in shapes_dict if item_name in d.values()]
                print('len object_dict',len(object_dict))
                print(new_img_name)
                img = cv2.imread(new_img_name, cv2.IMREAD_COLOR)
                if img is None:
                    print('Whoops! Is file extension missing?')
                    assert(True==False)
                    
                print('img type:',type(img))
                for d in object_dict:
                    #list of coordinates [x,y]
                    #list_points needs to be a numpy array so now np_points
                    list_points = d['points']
                    np_points = np.array([list_points], dtype=np.int32)
                    print('before fill',type(img))
                    cv2.fillPoly(img, np_points, (255, 255, 255)) 
                    print('after fill',type(img))
                #img is edited og

                #jpeg done
                if len(object_dict) > 0:
                    utilities.cv2_copy_and_rename_file(src_folder_dir, \
                                                       dest_folder_dir, \
                                                       filename, new_img_name, img)
                else:
                    utilities.copy_and_rename_file(src_folder_dir, \
                                                   dest_folder_dir, filename,\
                                                   new_img_name)
                if not os.path.exists(os.path.join(src_folder_dir, json_filename)):
                    continue
    
                #editing json file
                for element in py_json['shapes']:
                    #element and py_json are both dictionary
                    if item_name in element.values():
                        #remove the dictionary element from the list py_json['shapes']
                        py_json['shapes'].remove(element) 
                #py_json is new json file          
                open_file.close()
                #json done
                new_json_dir = os.path.join(dest_folder_dir, new_json_filename)
                with open(new_json_dir, 'w') as data_file:
                    py_json = json.dump(py_json, data_file)
                print("Finished editing " + str(img_file_count) + " images and corresponding json files.")
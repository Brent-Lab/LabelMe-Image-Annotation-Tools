import os
import shutil
import json
import cv2

def create_folder(dest_dir, name):
    new_folder_name = name
    new_folder_dir = os.path.join(dest_dir, new_folder_name)
    
    identifier = 0
    while os.path.exists(new_folder_dir): # Creates new folder
        identifier += 1
        new_folder_name = name + " " + str(identifier)
        new_folder_dir = os.path.join(dest_dir, new_folder_name)
        
    os.mkdir(new_folder_dir)
    return new_folder_dir
    
def copy_and_rename_file(src_dir, dest_dir, src_name, new_name):
    old_file_dir = os.path.join(src_dir, src_name)
    new_renamed_file_dir = os.path.join(dest_dir, new_name)

    shutil.copy(old_file_dir, new_renamed_file_dir)

    return new_renamed_file_dir
    
def cv2_copy_and_rename_file(src_dir, dest_dir, src_name, new_name, img):
    print(img.shape)
    old_file_dir = os.path.join(src_dir, src_name)
    new_renamed_file_dir = os.path.join(dest_dir, new_name)

    cv2.imwrite(new_renamed_file_dir, img)
    return new_renamed_file_dir

def get_label_me_annotations(json_dir):
    class LabelMeAnnotation:
        def __init__(self, src_dir):
            with open(src_dir, 'r') as f:
                json_data = json.load(f)
        
                self.version = json_data['version']
                self.flags = json_data['flags']
                self.shapes = json_data['shapes']
                self.imagePath = json_data['imagePath']
                self.imageData = json_data['imageData']
                self.imageHeight = int(json_data['imageHeight'])
                self.imageWidth = int(json_data['imageWidth'])
                
                self.src = src_dir
        
        def get_labels(self):
            labels = []
            
            for label in self.shapes:
                if not label['label'] in labels: # If label name does not already exist
                    labels.append(label['label'])
                    
            return labels
                    
        def set_labels(self, old_label, new_label):
            count = 0
        
            for i in range(len(self.shapes)):
                if self.shapes[i]['label'] == old_label:
                    self.shapes[i]['label'] = new_label
                    count+= 1
            
            return count
        
        def write_to_src(self):
            with open(self.src, 'w') as f:
                data = {"version": self.version,
                        "flags": self.flags,
                        "shapes": self.shapes,
                        "imagePath": self.imagePath,
                        "imageData": self.imageData,
                        "imageHeight": str(self.imageHeight),
                        "imageWidth": str(self.imageWidth)
                        }
                
                json.dump(data, f, indent=1)
    
    #
    annotation = LabelMeAnnotation(json_dir)
    return annotation
    

def get_all_labels(label_me_annotations):
    labels = []
    for annotation in label_me_annotations:
        annotation_labels = annotation.get_labels()
        for label in annotation_labels:
            if not label in labels:
                labels.append(label)
    return labels

def get_all_annotations(dir): # No Recursion yet
    annotations = []
    
    for filename in os.listdir(dir):
        if filename.lower().endswith('.json'):
            try:
                json_dir = os.path.join(dir, filename)
                annotation = get_label_me_annotations(json_dir)
                annotations.append(annotation)
            except KeyError:
                print("Found " + filename + " not in labelme format")
    return annotations

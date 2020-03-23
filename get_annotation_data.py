import os
import sys
import json

def get_annotation_data(dir):
    
    def helper(work_dir):
        labeled_images = 0
        classes = []
        for filename in os.listdir(work_dir):
            name, ext = os.path.splitext(os.path.join(work_dir, filename))
            if os.path.isdir(os.path.join(work_dir, filename)):
                print("Found new directory")
                v1, v2 = helper(os.path.join(work_dir, filename))
                labeled_images += v1
                classes = classes + v2
                continue
            # Find all json files
            if not ext.endswith(".json"):
                continue
            
            labeled_images += 1 # Each json file corresponds to one image
                    
            with open(os.path.join(work_dir, filename), 'r') as f:
                data = json.load(f)
                    
                #for shape in data['shapes']:
        return labeled_images, classes
                    
                        
        
    labeled_images, classes = helper(dir)
    print("Labeled Images: " + str(labeled_images))
    
    
get_annotation_data(os.getcwd() + "/TaqPath")

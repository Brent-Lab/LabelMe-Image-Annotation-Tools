import os
import sys
import piexif
import piexif.helper
import utilities
import json

src_folder_name = sys.argv[1]

def append_exif(src_dir):
    
    annotations = utilities.get_all_annotations(src_dir)
    labels = utilities.get_all_labels(annotations)
    
    print("Labels found: " + str(labels))
    
    exif_labels = {}
    
    for label in labels:
        exif_labels[label] = str(input("Please input EXIF data to append for images with label \'"  + label + "\':")).strip()
    
    count = 0
    for annotation in annotations:
        img_dir = os.path.join(src_dir, annotation.imagePath)
        
        annotation_labels = annotation.get_labels()
        
        comment = ""
        
        for label in annotation_labels:
            if not exif_labels[label] == "":
                comment = comment + exif_labels[label] + ";"
        
        comment = comment[:-1] + ":"
        
        exif_dict = piexif.load(img_dir)
        full_comment_dump = piexif.helper.UserComment.dump(comment)
        
        exif_dict["Exif"][piexif.ExifIFD.UserComment] = full_comment_dump

        piexif.insert(piexif.dump(exif_dict), img_dir)
        count+= 1
        
    print("Finished appending EXIF data to " + str(count) + " images")
        
    
                    
                
append_exif(os.path.join(os.getcwd(), src_folder_name))

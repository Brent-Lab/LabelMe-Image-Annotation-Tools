import os
import sys
import utilities

src_folder_name = sys.argv[1]

def rename_labels(src_folder_dir):
    annotations = utilities.get_all_annotations(src_folder_dir)
    labels = utilities.get_all_labels(annotations)
    
    print("Labels: ")
    
    for i in range(len(labels)):
        print(str(i) + ": " + labels[i])
    
    index = int(input("\nPlease choose a number corresponding to a label to edit or type -1 to exit:"))
    
    if index <= -1:
        return
        
    if index >= len(labels):
        print("Invalid value")
        return
            
    new_name = input("What would you like to rename the label " + labels[index] + " to?")
    
    print("Renaming...")
    
    for i in range(len(annotations)):
        annotations[i].set_labels(labels[index], new_name)
        annotations[i].write_to_src()
    
    print("Renamed " + labels[index] + " to " + new_name)
    

rename_labels(os.path.join(os.getcwd(), src_folder_name))

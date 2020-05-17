import os
import sys
import shutil
import json
import utilities

src_folder_name = sys.argv[1]
item_name = sys.argv[2]

allowed_image_types = (".jpg", ".jpeg")

def rename_annotation_files(work_dir):
    src_folder_dir = os.path.join(work_dir, src_folder_name)
    src_folder_dir = os.path.join(src_folder_dir, '')
    if not os.path.exists(src_folder_dir):
        print(src_folder_dir + " does not exist")
        return

    print(os.path.basename(os.path.dirname(src_folder_dir)))
    dest_folder_dir = utilities.create_folder(work_dir, "Renamed " + os.path.basename(os.path.dirname(src_folder_dir)))
    
    img_file_count = 0
    for filename in os.listdir(src_folder_dir):
        name, ext = os.path.splitext(os.path.join(src_folder_dir, filename))
        name, ext = name.lower(), ext.lower()
        if ext.endswith(allowed_image_types):
            img_file_count += 1
            
            # Copy image #
            new_name = item_name+"_"+str(img_file_count)
            new_img_name = new_name+ext
            
            utilities.copy_and_rename_file(src_folder_dir, dest_folder_dir, filename, new_img_name)
            
            # Copy corresponding json #
            
            json_filename = name + ".json"
            new_json_filename = new_name + ".json"
            
            if not os.path.exists(os.path.join(src_folder_dir, json_filename)):
                continue
            
            new_json_dir = utilities.copy_and_rename_file(src_folder_dir, dest_folder_dir, json_filename, new_json_filename)
            
            # Read and write to json file #
            
            with open(new_json_dir, 'r') as f:
                data = json.load(f)
                data['imagePath'] = new_img_name
                with open(new_json_dir, 'w') as f2:
                    json.dump(data, f2, indent=1)
            
    print("Finished Renaming " + str(img_file_count) + " images and corresponding json files.")
            
rename_annotation_files(os.getcwd())

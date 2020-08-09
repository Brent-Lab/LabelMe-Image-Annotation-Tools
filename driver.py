import os
import sys
import glob
import json

import tools


allowed_image_types = (".jpg", ".jpeg")


def copy_and_rename_files_driver(output_dir, src_folder_path, new_folder_name, item_name):
    new_folder_path = tools.create_folder(output_dir, new_folder_name)
    # utilities.copy_and_rename_file(file_path, dest_dir, new_name)

    count = 0
    for name in os.listdir(src_folder_path):
        file_path = os.path.join(src_folder_path, name)
        name, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext.endswith(allowed_image_types):  # If allowed image format
            count += 1

            new_name = item_name + "_" + str(count)

            # Copy image
            new_img_name = new_name + ext
            tools.copy_and_rename_file(file_path, new_folder_path, new_img_name)

            # Copy corresponding json Files
            json_file_path = name + ".json"
            new_json_name = new_name + ".json"

            # If json does not exist for image skip
            if not os.path.exists(json_file_path):
                continue

            new_json_dir = tools.copy_and_rename_file(json_file_path, new_folder_path, new_json_name)

            # Read and write new corresponding image path to json file #

            with open(new_json_dir, 'r') as f:
                data = json.load(f)
                data['imagePath'] = new_img_name
                with open(new_json_dir, 'w') as f2:
                    json.dump(data, f2, indent=1)

    print("Finished renaming " + str(count) + " images and their corresponding json files.")
    return new_folder_path


def labelme_to_coco_driver(output_dir, src_dir):
    tools.save_to_coco_json(src_dir, output_dir, "trainval.json")


def set_exif_driver(src_dir):
    annotations = tools.get_annotations(src_dir)
    labels = tools.get_all_labels(annotations)
    exif_label_map = {}

    print("Labels found: " + str(labels))
    for label in labels:
        exif_label_map[label] = str(input("Please input EXIF data to append for images with label \'" + label + "\':"))\
                                .strip()

    count = tools.set_exif_from_annotations(annotations, exif_label_map)

    print("Finished appending EXIF data to " + str(count) + " images")


def main():
    src_folder_name = sys.argv[1]
    src_folder_path = os.path.join(os.getcwd(), src_folder_name)

    print("Press CTRL+C to exit at any time")

    # Copy and rename files
    ans = str(input("Would you like to rename the files in the folder? (y/n)")).lower().strip()
    if ans == "y":
        item_name = str(input("What would you like to rename the files to?")).strip()

        src_folder_path = copy_and_rename_files_driver(os.getcwd(), src_folder_path, src_folder_name, item_name)
        print("Switching source folder to " + src_folder_path)

    # Create coco annotation
    ans = str(input("Would you like to create a COCO annotation from LabelMe files? (y/n)")).lower().strip()
    if ans == "y":
        labelme_to_coco_driver(src_folder_path, src_folder_path)

    # Append EXIF data
    ans = str(input("Would you like to append EXIF data to images based on LabelMe labels? (y/n)")).lower().strip()
    if ans == "y":
        set_exif_driver(src_folder_path)


if __name__ == "__main__":
    main()
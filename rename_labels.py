import os
import sys
import tools

# TODO:
# Integrate with labelme_utils.py


def print_labels(labels):
    print("Labels:")
    for i in range(len(labels)):
        print(str(i) + ": " + labels[i])


def rename_labels(src_folder_dir):
    annotations = tools.get_all_annotations(src_folder_dir)
    labels = tools.get_all_labels(annotations)

    print_labels(labels)

    index = int(input("\nPlease choose a number corresponding to a label to edit or type -1 to exit:")).strip()
    if index <= -1:
        return
    if index >= len(labels):
        print("Invalid value")
        return
            
    new_name = input("What would you like to rename the label " + labels[index] + " to?").strip()
    print("Renaming...")
    for i in range(len(annotations)):
        annotations[i].set_labels(labels[index], new_name)
        annotations[i].write_to_src()
    
    print("Renamed " + labels[index] + " to " + new_name)


def main():
    src_folder_name = sys.argv[1]
    rename_labels(os.path.join(os.getcwd(), src_folder_name))


if __name__ == "__main__":
    main()
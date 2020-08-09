import os
import io
import json
import base64
import cv2
from pathlib import Path
import numpy as np
import PIL.Image


class LabelMeAnnotation:
    """
        Class holding Label Me Annotation data from a json file.

        Attributes:
            version (string): Version of LabelMe encoded for.
            flags (dict(string)): Labels for an entire image.
            shapes (list(dict)): List of labeled data.
            imagePath (string): Local path of an annotation's corresponding image.
            imageData (string): String encoding the corresponding image to UTF-8 format.
            imageHeight (int): Height of the corresponding image.
            imageWidth (int): Width of the corresponding image.
            src (string): Path to corresponding json file.
    """
    def __init__(self, json_dir=None):
        self.version = None
        self.flags = {}
        self.shapes = []
        self.imagePath = None
        self.imageData = None
        self.imageWidth = None

        self.globalImagePath = None
        self.src = None

        if json_dir is not None:
            self.__load_json(json_dir)

    def __load_json(self, json_dir):
        with open(json_dir, 'r') as f:
            json_data = json.load(f)

            self.version = json_data['version']
            self.flags = json_data['flags']
            self.shapes = json_data['shapes']
            self.imagePath = json_data['imagePath']
            self.imageData = json_data['imageData']
            self.imageHeight = int(json_data['imageHeight'])
            self.imageWidth = int(json_data['imageWidth'])

            # For now, image file should be in same directory as json file
            # Updating json path will cause problems in future
            parent_dir = os.path.dirname(json_dir)
            self.globalImagePath = os.path.join(parent_dir, self.imagePath)
            self.src = json_dir

    def get_labels(self):
        """
        Gets every label name.

        Returns:
            labels (list(string)): List of label names.
        """
        labels = []
        for label in self.shapes:
            if not label['label'] in labels: # If label name does not already exist
                labels.append(label['label'])
        return labels
    
    def rename_labels(self, old_label, new_label):
        """
        Renames every label.

        Parameters:
            old_label (string): Label name to replace.
            new_label (string): Label name which replaces the old label.

        Returns:
            count (int): Count of every label renamed.
        """
        count = 0
        for i, label in enumerate(self.shapes):
            if label['label'] == old_label:
                self.shapes[i]['label'] = new_label
                count += 1
        return count
        
    def add_label(self, label_name, points, group_id=None, shape_type="polygon", flags={}):
        """
        Adds a new label.

        Parameters:
            label_name (string): Name of new label.
            points (list(list)): List of a list of an x and a y coordinate.
            group_id (int): ID of group image belongs to.
            shape_type (string): Shape of the drawn label.
            flags (dict): Flags of a polygon.
        """
        print("Adding label")
        self.shapes.append({"label": label_name,
                            "points": points,
                            "group_id": group_id,
                            "shape_type": shape_type,
                            "flags": flags
                            })
    
    def remove_labels(self, label_name):
        """
        Removes labels based on name.

        Parameters:
            label_name (string): Name of label to be removed.

        Returns:
            count (int): Number of labels removed
        """
        count = 0
        for i, label in enumerate(self.shapes):
            if label["label"] == label_name:
                del self.shapes[i]
                count += 1
        return count
    
    def write_to_src(self):
        """
        Writes data to corresponding json file.
        """
        if self.src is None:
            print("No source file for Labelme Class")
            return
        with open(self.src, 'w') as f:
            data = {"version": self.version,
                    "flags": self.flags,
                    "shapes": self.shapes,
                    "imagePath": self.imagePath,
                    "imageData": self.imageData,
                    "imageHeight": self.imageHeight,
                    "imageWidth": self.imageWidth
                    }
            json.dump(data, f, ensure_ascii=False, indent=2)


def get_annotations(dir, recursive=True):
    """
    Gets all LabelMe json files in a directory and returns a list of LabelMeAnnotation class objects.

    Parameters:
        dir (string): Directory containing LabelMe json files.
        recursive (bool): Get annotations within nested folders.

    Returns:
        annotations (list(LabelMeAnnotation)): List of LabelMeAnnotation classes.
    """
    annotations = []

    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if name.lower().endswith('.json'):  # If json file
            try:  # Checks if in labelme format
                annotation = LabelMeAnnotation(path)
                annotations.append(annotation)
            except KeyError:
                print("Found " + name + " not in LabelMe format")
        elif os.path.isdir(path) and recursive:
            annotations.extend(get_annotations(path))  # Append nested folder's annotations to annotation list
            
    return annotations


def get_all_labels(annotations):
    """
    Gets all labels in an array of LabelMeAnnotation classes.

    Parameters:
        annotations(list(LabelMeAnnotation)): List of LabelMeAnnotation classes.

    Returns:
        labels (list(string)): List of names of labels within the annotations array.
    """
    labels = []
    for annotation in annotations:
        annotation_labels = annotation.get_labels()
        for label in annotation_labels:
            if label not in labels:
                labels.append(label)
    return labels


def write_annotations_to_files(annotations):
    """
    Writes array of LabelMeAnnotation classes to their json file.

    Parameters:
        annotations (list(LabelMeAnnotation)): Array of LabelMeAnnotation classes.

    Returns:
       count (int): Count of annotations written to file.
    """
    count = 0
    for annotation in annotations:
        annotation.write_to_src()
        count += 1
    return count


def apply_exif_orientation(image):
    try:
        exif = image._getexif()
    except AttributeError:
        exif = None

    if exif is None:
        return image

    exif = {
        PIL.ExifTags.TAGS[k]: v
        for k, v in exif.items()
        if k in PIL.ExifTags.TAGS
    }

    orientation = exif.get("Orientation", None)

    if orientation == 1:
        # do nothing
        return image
    elif orientation == 2:
        # left-to-right mirror
        return PIL.ImageOps.mirror(image)
    elif orientation == 3:
        # rotate 180
        return image.transpose(PIL.Image.ROTATE_180)
    elif orientation == 4:
        # top-to-bottom mirror
        return PIL.ImageOps.flip(image)
    elif orientation == 5:
        # top-to-left mirror
        return PIL.ImageOps.mirror(image.transpose(PIL.Image.ROTATE_270))
    elif orientation == 6:
        # rotate 270
        return image.transpose(PIL.Image.ROTATE_270)
    elif orientation == 7:
        # top-to-right mirror
        return PIL.ImageOps.mirror(image.transpose(PIL.Image.ROTATE_90))
    elif orientation == 8:
        # rotate 90
        return image.transpose(PIL.Image.ROTATE_90)
    else:
        return image


def load_image_file(filename):
    try:
        image_pil = PIL.Image.open(filename)
    except IOError:
        print("Failed opening image file: {}".format(filename))
        return

    # apply orientation to image according to exif
    image_pil = apply_exif_orientation(image_pil)

    with io.BytesIO() as f:
        ext = os.path.splitext(filename)[1].lower()
        if ext in [".jpg", ".jpeg"]:
            format = "JPEG"
        else:
            format = "PNG"
        image_pil.save(f, format=format)
        f.seek(0)
        return f.read()


def img_data_to_pil(img_data):
    f = io.BytesIO()
    f.write(img_data)
    img_pil = PIL.Image.open(f)
    return img_pil


def img_data_to_arr(img_data):
    img_pil = img_data_to_pil(img_data)
    img_arr = np.array(img_pil)
    return img_arr


def create_empty_labelme_json(img_path):
    img_path_object = Path(img_path)

    img_file_name = img_path_object.name
    img_name = img_path_object.stem
    parent_dir = img_path_object.parent

    img_data = load_image_file(img_path)
    img_arr = img_data_to_arr(img_data)

    data = {}
    data["version"] = "4.2.9"
    data["flags"] = {}
    data["shapes"] = []
    data["imagePath"] = img_file_name
    data["imageData"] = base64.b64encode(img_data).decode("utf-8")
    data["imageHeight"] = img_arr.shape[0]
    data["imageWidth"] = img_arr.shape[1]

    json_path = os.path.join(parent_dir, img_name + ".json")

    with open(json_path, 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=2)

    return json_path
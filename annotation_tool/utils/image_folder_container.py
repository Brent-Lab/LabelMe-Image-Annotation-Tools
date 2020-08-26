import os
import piexif
import piexif.helper
from PIL import ImageTk, Image, ExifTags
from .labelme_annotation import LabelMeAnnotation
from .labelme2coco import save_to_coco_json


class ImageContainer:
    def __init__(self, img_path):
        self.img_path = img_path
        self.annotation = self.__load_labelme_annotation()
        self.user_comments = "test"

    def get_imgtk(self, resize_width, resize_height):
        img_pil = self.__load_img_pil_with_exif(self.img_path)
        resize_ratio = min(resize_width / img_pil.width, resize_height / img_pil.height)

        img_pil_resized = img_pil.resize((int(img_pil.width*resize_ratio), int(img_pil.height*resize_ratio)), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img_pil_resized)

    def set_exif_user_comments(self, comments):
        self.user_comments = comments

    def save_img(self, img_out_path):
        img_pil = Image.open(self.img_path)
        exif_dict = piexif.load(img_pil.info["exif"])

        # Dump comment into exif data
        full_comment_dump = piexif.helper.UserComment.dump(self.user_comments)
        exif_dict["Exif"][piexif.ExifIFD.UserComment] = full_comment_dump

        exif_bytes = piexif.dump(exif_dict)
        img_pil.save(img_out_path, "JPEG", exif=exif_bytes)

    def save_annotation(self, json_out_path):
        self.annotation.save(json_out_path)

    def __load_img_pil_with_exif(self, img_path):
        img_pil = Image.open(img_path)
        return self.__apply_exif_orientation(img_pil)

    def __load_labelme_annotation(self):
        annotation = LabelMeAnnotation(self.img_path)
        return annotation

    def __apply_exif_orientation(self, img_pil):
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(img_pil._getexif().items())

        if exif[orientation] == 3:
            img_pil = img_pil.transpose(Image.ROTATE_180)
        elif exif[orientation] == 6:
            img_pil = img_pil.transpose(Image.ROTATE_270)
        elif exif[orientation] == 8:
            img_pil = img_pil.transpose(Image.ROTATE_90)

        return img_pil


class ImageFolderContainer:
    def __init__(self, folder_path, allowed_img_types=['.jpg', '.jpeg']):
        self.folder_name = os.path.basename(folder_path) + "_New"
        self.folder_path = folder_path
        self.allowed_img_types = allowed_img_types
        self.img_paths = self.__get_img_paths_in_folder(folder_path)
        self.img_container_list = self.__create_img_container_list(self.img_paths)
        self.current_img_idx = 0 if len(self.img_container_list) > 0 else None

    def get_current_imgtk(self, resize_width, resize_height):
        img_container = self.img_container_list[self.current_img_idx]
        return img_container.get_imgtk(resize_width=resize_width, resize_height=resize_height)

    def move_next_img(self):
        if self.current_img_idx is None:
            return
        self.current_img_idx = min(self.current_img_idx+1, len(self.img_container_list)-1)

    def move_prev_img(self):
        if self.current_img_idx is None:
            return
        self.current_img_idx = max(self.current_img_idx-1, 0)

    def get_all_label_names(self):
        labels = {}
        for img_container in self.img_container_list:
            annotation_labels = img_container.annotation.get_labels()
            for label_name, count in annotation_labels.items():
                if label_name not in labels:
                    labels[label_name] = count
                else:
                    labels[label_name] += count
        return labels

    def set_exif_user_comments(self, exif_label_map):
        for img_container in self.img_container_list:
            comments = ""
            annotation_labels = img_container.annotation.get_labels()
            for label, count in annotation_labels.items():
                if label in exif_label_map:
                    comments = comments + exif_label_map[label] + ";"
            comments = comments[:-1] + ":" # Replace last ; with a :
            img_container.set_exif_user_comments(comments)


    def export_folder(self, folder_path, img_name):
        # 1. Create directory of folder_path
        # 2. Save images from img_container with EXIF data
        # 3. Save json files from annotation

        try:
            os.mkdir(folder_path)
        except OSError as e:
            print(e)
            return

        count = 0
        for img_container in self.img_container_list:
            count += 1
            out_name = img_name+"_"+str(count)

            img_out_path = os.path.join(folder_path, out_name + ".jpg")
            json_out_path = os.path.join(folder_path, out_name + ".json")
            img_container.annotation.set_new_img_path(img_out_path)
            img_container.save_img(img_out_path)
            img_container.save_annotation(json_out_path)

        save_to_coco_json(folder_path, folder_path, "trainval_new.json")

    def __get_img_paths_in_folder(self, folder_path):
        img_paths = []
        for filename in os.listdir(folder_path):
            basename, ext = os.path.splitext(filename)
            ext_lower = ext.lower()
            if ext_lower in self.allowed_img_types:
                file_path = os.path.join(folder_path, filename)
                img_paths.append(file_path)
        return img_paths

    def __create_img_container_list(self, img_paths):
        img_container_list = []
        for img_path in img_paths:
            img_container = ImageContainer(img_path)
            img_container_list.append(img_container)
        return img_container_list

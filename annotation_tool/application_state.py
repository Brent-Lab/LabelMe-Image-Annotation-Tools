import tkinter as tk


class Singleton(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Creating Singleton")
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


class ApplicationState(Singleton):
    def __init__(self):
        self.target_folder = "/"
        self.current_img = None

        self.statistics = {
            "total_images": {"title": "Total Images", "number": 0},
            "total_images_annotated": {"title": "Total Images Annotated", "number": 0},
            "total_annotations": {"title": "Total Annotations", "number": 0},
            "total_unique_objects": {"title": "Total Unique Objects", "number": 0}
        }

        self.object_list = {}
        self.exif_label_map = {}

class WindowViewState(Singleton):
    def __init__(self):
        pass
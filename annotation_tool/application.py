import os
from window import Window
from application_state import ApplicationState
from utils import ImageFolderContainer


class Application():
    def __init__(self):
        self.app_state = ApplicationState()
        self.img_folder_container = None
        self.func_callbacks = {
            "open_folder": self.open_folder,
            "next_img": self.next_img,
            "prev_img": self.prev_img,
            "export_folder": self.export_folder,
            "open_exif_dialogue": self.open_exif_dialogue,
            "save_exif_label_map": self.save_exif_label_map
        }

        self.window = Window(self.func_callbacks)
        self.window.start()

    # Function Callbacks #
    def open_folder(self, folder_path):
        self.app_state.target_folder = folder_path
        self.img_folder_container = ImageFolderContainer(folder_path)

        self.window.update_current_folder_view(folder_path)
        self.__update_img_view()
        self.__update_statistics()
        self.__update_object_list()

    def next_img(self):
        self.img_folder_container.move_next_img()
        self.__update_img_view()

    def prev_img(self):
        self.img_folder_container.move_prev_img()
        self.__update_img_view()

    def export_folder(self, dir_path, img_name):
        folder_name = self.img_folder_container.folder_name
        folder_path = os.path.join(dir_path, folder_name)

        print("Saving folder to ", folder_path)
        self.img_folder_container.export_folder(folder_path, img_name)
        print("Finished saving")

    def open_exif_dialogue(self):
        object_list = self.img_folder_container.get_all_label_names()
        for key, value in object_list.items():
            object_list[key] = ""
        self.window.open_exif_dialogue(object_list)
        print(self.app_state.exif_label_map)

    def save_exif_label_map(self, exif_label_map):
        print("Exif Label Map: ", exif_label_map)
        self.app_state.exif_label_map = exif_label_map
        self.img_folder_container.set_exif_user_comments(exif_label_map)


    # End of Function Callbacks

    def __update_object_list(self):
        self.app_state.object_list = self.img_folder_container.get_all_label_names()
        self.window.update_object_list_viewer(self.app_state.object_list)

    def __update_statistics(self):
        self.window.update_statistics_view(self.app_state.statistics)

    def __update_img_view(self):
        if self.img_folder_container is None:
            print("No images")
            return

        canvas_width = self.window.window_frame.image_viewer.winfo_width()
        canvas_height = self.window.window_frame.image_viewer.winfo_height()
        self.current_img = self.img_folder_container.get_current_imgtk(canvas_width, canvas_height)
        self.window.update_img_view(self.current_img)

        
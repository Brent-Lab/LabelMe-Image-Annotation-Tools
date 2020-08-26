import os
from window import Window
from application_state import ApplicationState
from utils import ImageFolderContainer


ALLOWED_IMG_TYPES = ['.jpg', '.jpeg']


class Application():
    def __init__(self):
        self.app_state = ApplicationState()
        self.img_folder_container = None
        self.func_callbacks = {
            "open_folder": self.open_folder,
            "next_img": self.next_img,
            "prev_img": self.prev_img,
            "export_folder": self.export_folder
        }

        self.window = Window(self.func_callbacks)
        self.window.start()

    def next_img(self):
        self.img_folder_container.move_next_img()
        self.update_img()

    def prev_img(self):
        self.img_folder_container.move_prev_img()
        self.update_img()

    def open_folder(self, folder_path):
        self.app_state.target_folder = folder_path
        self.img_folder_container = ImageFolderContainer(folder_path)
        self.window.update_folder_name(folder_path)
        self.update_img()
        self.update_statistics()
        self.update_object_list()

    #def set_exif_user_comments(self):
        #self.img_folder_container.set_exif_user_comments(self.app_state.exif_label_map)

    def update_object_list(self):
        self.app_state.object_list = self.img_folder_container.get_all_label_names()
        self.window.update_object_list_viewer()
        print(self.app_state.object_list)

    def update_statistics(self):
        self.window.update_statics_viewer()

    def update_img(self):
        if self.img_folder_container is None:
            print("No images")
            return

        canvas_width = self.window.window_frame.image_viewer.winfo_width()
        canvas_height = self.window.window_frame.image_viewer.winfo_height()
        self.current_img = self.img_folder_container.get_current_imgtk(canvas_width, canvas_height)
        self.window.update_image_viewer(self.current_img)

    def export_folder(self, dir_path, img_name):
        folder_name = self.img_folder_container.folder_name
        folder_path = os.path.join(dir_path, folder_name)

        self.img_folder_container.export_folder(folder_path, img_name)
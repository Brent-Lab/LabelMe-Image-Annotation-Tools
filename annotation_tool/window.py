import tkinter as tk
from widgets import SideToolBar, ImageViewer, InfoFrame, ExifPrompt


class WindowFrame(tk.Frame):
    def __init__(self, parent, func_callbacks={}, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.func_callbacks = func_callbacks

        self.img_viewer_size = 600
        self.create_widgets()

    def create_widgets(self):
        self.folder_name_label = tk.Label(text="Folder: ")
        self.side_tool_bar = SideToolBar(self, func_callbacks=self.func_callbacks, borderwidth=1)
        self.image_viewer = ImageViewer(self, func_callbacks=self.func_callbacks, width=self.img_viewer_size, height=self.img_viewer_size, bg="black")
        self.info_frame = InfoFrame(self, func_callbacks=self.func_callbacks)

        # Pack Widgets
        self.side_tool_bar.pack(side="left", anchor=tk.NW, fill=tk.Y, padx=10, pady=10)
        self.image_viewer.pack(side="left", fill=tk.X, expand=False)
        self.info_frame.pack(side="right", anchor=tk.NE, fill=tk.Y, padx=10, pady=10)
        self.folder_name_label.pack(side="top", fill=tk.X)


class Window():
    """
    Controls the user interface.
    """
    def __init__(self, func_callbacks={}):
        self.gui_root = tk.Tk()
        self.gui_root.title("Annotation Tools")
        self.gui_root.resizable(False, False)
        self.func_callbacks = func_callbacks

        self.window_frame = WindowFrame(self.gui_root, func_callbacks)
        self.window_frame.pack()

    def start(self):
        self.window_frame.mainloop()

    def update_img_view(self, img):
        viewer_width = self.window_frame.image_viewer.winfo_width()
        viewer_height = self.window_frame.image_viewer.winfo_height()
        self.window_frame.image_viewer.create_image(viewer_width/2, viewer_height/2, anchor=tk.CENTER, image=img)

    def update_statistics_view(self, statistics):
        listbox = self.window_frame.info_frame.statistics_frame.listbox
        listbox.delete(0, tk.END) # Clear listbox

        for key, value in statistics.items():
            title = value["title"]
            number = str(value["number"])
            listbox.insert(tk.END, title+": "+number)

    def update_object_list_viewer(self, object_list):
        listbox = self.window_frame.info_frame.object_list.listbox
        listbox.delete(0, tk.END) # Clear listbox

        for key, value in sorted(object_list.items()):
            listbox.insert(tk.END, key+": "+str(value))

    def update_current_folder_view(self, folder_path):
        self.window_frame.folder_name_label["text"] = ("Folder: " + folder_path)

    def open_exif_dialogue(self, exif_label_map):
        if (len(exif_label_map) == 0):
            print("No labels")
            #return
        object_list = list(exif_label_map.keys())
        self.current_index = 0

        def next_exif_object():
            comment = self.exif_dialogue.exif_comment.get()
            exif_label_map[object_list[self.current_index]] = comment

            # Stop if no more objects
            if self.current_index >= len(object_list)-1:
                self.exif_dialogue.destroy()
                self.func_callbacks["save_exif_label_map"](exif_label_map)
                return

            # New object
            self.current_index += 1
            key = object_list[self.current_index]
            # self.exif_dialogue.exif_comment.delete(0, tk.END)
            self.exif_dialogue.desc["text"] = "Enter EXIF comment for \"" + key + "\""

        self.func_callbacks["next_exif_object"] = next_exif_object
        self.exif_dialogue = ExifPrompt(self.window_frame, self.func_callbacks)
        key = object_list[self.current_index]
        self.exif_dialogue.desc["text"] = "Enter EXIF comment for \"" + key + "\""
        self.exif_dialogue.overrideredirect(True)


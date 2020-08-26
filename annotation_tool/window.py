import tkinter as tk
from widgets import SideToolBar, ImageViewer, InfoFrame
from application_state import ApplicationState, WindowViewState


class WindowFrame(tk.Frame):
    def __init__(self, parent, func_callbacks={}, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.func_callbacks = func_callbacks
        self.app_state = ApplicationState()
        #self.window_state = WindowViewState()
        self.img_viewer_size = 600
        self.create_widgets()

    def create_widgets(self):
        self.folder_name_label = tk.Label(text="Folder: ")
        self.side_tool_bar = SideToolBar(self, borderwidth=1, func_callbacks=self.func_callbacks)
        self.image_viewer = ImageViewer(self, width=self.img_viewer_size, height=self.img_viewer_size, bg="black")
        self.info_frame = InfoFrame(self)

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
        self.gui_root=tk.Tk()
        self.gui_root.title("Annotation Tools")
        self.gui_root.resizable(False, False)

        self.app_state = ApplicationState()
        self.window_frame = WindowFrame(self.gui_root, func_callbacks)
        self.window_frame.pack()

    def start(self):
        self.window_frame.mainloop()

    def update_app_state_view(self):
        self.window_state.target_folder.set(self.app_state.target_folder)

    def update_image_viewer(self, img):
        viewer_width = self.window_frame.image_viewer.winfo_width()
        viewer_height = self.window_frame.image_viewer.winfo_height()
        self.window_frame.image_viewer.create_image(viewer_width/2, viewer_height/2, anchor=tk.CENTER, image=img)

    def update_statics_viewer(self):
        listbox = self.window_frame.info_frame.statistics_frame.listbox

        listbox.delete(0, tk.END)
        for key, value in self.app_state.statistics.items():
            title = value["title"]
            number = str(value["number"])
            listbox.insert(tk.END, title+": "+number)

    def update_object_list_viewer(self):
        listbox = self.window_frame.info_frame.object_list.listbox
        listbox.delete(0, tk.END)

        for key, value in sorted(self.app_state.object_list.items()):
            listbox.insert(tk.END, key+": "+str(value))

    def update_folder_name(self, folder_path):
        self.window_frame.folder_name_label["text"] = ("Folder: " + folder_path)

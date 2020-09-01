import tkinter as tk
from tkinter import filedialog


class AddExifPrompt(tk.Toplevel):
    def __init__(self, parent, func_callbacks={}, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.func_callbacks = func_callbacks
        self.create_widgets()

    def create_widgets(self):
        self.desc = tk.Label(self, text="Select the objects you would like to append EXIF data to.")
        self.exif_comment = tk.Entry(self)
        self.scrollbar = tk.Scrollbar(self)
        self.cancel = tk.Button(self, text="Cancel", anchor=tk.CENTER, command=self.destroy)
        self.enter = tk.Button(self, text="Enter", anchor=tk.CENTER)
        self.listbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
        self.listbox.bindtags(())

        self.desc.pack()
        self.exif_comment.pack(side=tk.RIGHT, anchor=tk.N)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.scrollbar.config(command=self.listbox.yview)
        self.cancel.pack(side=tk.BOTTOM)
        self.enter.pack(side=tk.BOTTOM)
        self.listbox.pack(side=tk.RIGHT, fill=tk.BOTH)

    def update_listbox(self):
        pass
        #for key, value in self.app_state.object_list.items():
            #print(key)


class ExportPrompt(tk.Toplevel):
    def __init__(self, parent, func_callbacks={}, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.func_callbacks = func_callbacks
        self.create_widgets()

    def create_widgets(self):
        self.desc = tk.Label(self, text="What would you like to name the images?")
        self.img_name = tk.Entry(self)
        self.cancel = tk.Button(self, text="Cancel", anchor=tk.CENTER, command=self.destroy)
        self.enter = tk.Button(self, text="Enter", anchor=tk.CENTER, command=self.export_to_directory)

        self.desc.pack()
        self.img_name.pack()
        self.cancel.pack(side=tk.LEFT)
        self.enter.pack(side=tk.LEFT)

    def export_to_directory(self):
        img_name = self.img_name.get()
        self.destroy()
        folder_path = filedialog.askdirectory()

        self.func_callbacks["export_folder"](folder_path, img_name)


class RenameLabelsPrompt(tk.Toplevel):
    def __init__(self, parent, func_callbacks={}, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.func_callbacks=func_callbacks
        self.create_widgets()

    def create_widgets(self):
        self.desc = tk.Label(self, text="What would you like to rename?")
        self.img_name = tk.Entry(self)
        self.cancel = tk.Button(self, text="Cancel", anchor=tk.CENTER, command=self.destroy)
        self.enter = tk.Button(self, text="Enter", anchor=tk.CENTER, command=self.destroy)

        self.desc.pack()
        self.img_name.pack()
        self.cancel.pack(side=tk.LEFT)
        self.enter.pack(side=tk.LEFT)


class SideToolBar(tk.Frame):
    def __init__(self, parent, func_callbacks={}, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.func_callbacks = func_callbacks
        self.create_widgets()

    def create_widgets(self):
        self.open_folder = tk.Button(self, text="Import Folder", command=self.browse_folder)
        self.export = tk.Button(self, text="Export", command=self.open_export_dialogue)
        self.seperator1 = tk.Label(self, text="_______")
        self.add_exif = tk.Button(self, text="Add EXIF", command=self.func_callbacks["open_exif_dialogue"])
        self.rename_label = tk.Button(self, text="Rename Labels")
        self.seperator2 = tk.Label(self, text="_______")
        self.next_button = tk.Button(self, text="Next Image", command=self.func_callbacks["next_img"])
        self.prev_button = tk.Button(self, text="Prev Image", command=self.func_callbacks["prev_img"])

        # Pack widgets
        self.open_folder.pack(fill=tk.X)
        self.export.pack(fill=tk.X)
        self.seperator1.pack(fill=tk.X)
        self.add_exif.pack(fill=tk.X)
        self.rename_label.pack(fill=tk.X)
        self.seperator2.pack(fill=tk.X)
        self.next_button.pack(fill=tk.X)
        self.prev_button.pack(fill=tk.X)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        self.func_callbacks["open_folder"](folder_path)

    def open_export_dialogue(self):
        self.new_window = ExportPrompt(self, self.func_callbacks)

    def open_rename_labels_dialogue(self):
        self.rename_labels_dialogue = RenameLabelsPrompt(self, self.func_callbacks)

    def open_exif_dialogue(self):
        self.exif_dialogue = AddExifPrompt(self, self.func_callbacks)


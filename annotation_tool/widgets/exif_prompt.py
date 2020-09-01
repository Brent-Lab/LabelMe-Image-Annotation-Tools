import tkinter as tk

class ExifPrompt(tk.Toplevel):
    def __init__(self, parent, func_callbacks={}, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.func_callbacks=func_callbacks
        self.create_widgets()

    def create_widgets(self):
        self.desc = tk.Label(self, text="Enter EXIF comment for object \"\"")
        self.exif_comment = tk.Entry(self)
        self.cancel = tk.Button(self, text="Cancel", anchor=tk.CENTER, command=self.destroy)
        self.enter = tk.Button(self, text="Enter", anchor=tk.CENTER, command=self.func_callbacks["next_exif_object"])

        self.desc.pack()
        self.exif_comment.pack(anchor=tk.N)
        self.cancel.pack(side=tk.LEFT)
        self.enter.pack(side=tk.LEFT)
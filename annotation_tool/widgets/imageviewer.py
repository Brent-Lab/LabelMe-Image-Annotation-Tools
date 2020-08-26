import tkinter as tk


class ImageViewer(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        pass
import tkinter as tk
from application_state import ApplicationState


class ObjectList(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.frame_title = tk.Label(self, text="Object List")
        self.scrollbar = tk.Scrollbar(self)
        self.listbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
        self.listbox.bindtags(())

        self.frame_title.pack()
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.scrollbar.config(command=self.listbox.yview)


class StatisticsFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.app_state = ApplicationState()
        self.create_widgets()

    def create_widgets(self):
        self.frame_title = tk.Label(self, text="Folder Statistics")
        self.scrollbar = tk.Scrollbar(self)
        self.listbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
        self.listbox.bindtags(())

        self.frame_title.pack()
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.scrollbar.config(command=self.listbox.yview)


class InfoFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.object_list = ObjectList(self, borderwidth=0, highlightbackground="black", highlightthickness=1)
        self.statistics_frame = StatisticsFrame(self, borderwidth=0, highlightbackground="black", highlightthickness=1)

        self.object_list.pack(side=tk.TOP)
        self.statistics_frame.pack(side=tk.TOP)

import tkinter as tk


class ObjectList(tk.Frame):
    def __init__(self, parent, func_callbacks, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.func_callbacks = func_callbacks
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
    def __init__(self, parent, func_callbacks, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.func_callbacks = func_callbacks
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
    def __init__(self, parent, func_callbacks, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.func_callbacks = func_callbacks
        self.create_widgets()

    def create_widgets(self):
        self.object_list = ObjectList(self, func_callbacks=self.func_callbacks, borderwidth=0, highlightbackground="black", highlightthickness=1)
        self.statistics_frame = StatisticsFrame(self, func_callbacks=self.func_callbacks, borderwidth=0, highlightbackground="black", highlightthickness=1)

        self.object_list.pack(side=tk.TOP)
        self.statistics_frame.pack(side=tk.TOP)

from tkinter import *
from tkinter import ttk
from tkinter import Tk

class CustomLabel (ttk.Label):
    def __init__(self, parent, text, font_size=12, font_family="Comic Sans", **kwargs):
        super().__init__(parent,  text=text, font=(font_family,font_size), **kwargs)

class CustomRoot (Tk):
    def __init__(self):
        super().__init__()

        self.title("автоматизоване вивільнекння ліцензії та запуск клієнта")
        self.geometry("500x500")

        self.start_window()

    def start_window(self):
        pass
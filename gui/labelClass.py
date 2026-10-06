from tkinter import *
from tkinter import ttk
from tkinter import Tk

class CustomLabel (ttk.Label):
    def __init__(self, parent, text, font_size=12, font_family="Comic Sans", **kwargs):
        super().__init__(parent,  text=text, font=(font_family,font_size), **kwargs)

        self.bind("<Control-c>", self.copy_text)
        self.bind("<Button-1>", self.focus_label)

    def focus_label(self, event):
        self.focus_set()

    def copy_text(self, event):
        self.clipboard_clear()
        self.clipboard_append(self.cget("text"))
        return "break"

class CustomRoot (Tk):
    def __init__(self):
        super().__init__()

        self.title("Автоматизоване вивільнення ліцензії та запуск клієнта")
        self.geometry("500x500")

        self.start_window()

    def start_window(self):
        pass
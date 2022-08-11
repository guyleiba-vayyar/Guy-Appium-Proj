import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter



class LabelEntry(tk.Frame):
    """
    This class is mostly for the choose apk and choose folder labels text boxes and buttons
    """
    def __init__(self, parent, text, button):
        super().__init__(parent)
        self.pack(fill=tk.X)

        lbl = tk.Label(self, text=text, width=63, anchor='w')
        lbl.pack(side=tk.LEFT, padx=5, pady=5)

        curr_frame = tk.Frame(self)
        curr_frame.pack(side=tk.LEFT, expand=True)

        self.box = tk.Text(curr_frame, width=50, height=1)
        self.box.pack(side=tk.LEFT, padx=20)

        button.pack(in_=curr_frame, side=tk.LEFT, padx=5, pady=5)

    def insert(self,path):
        """
        This function enters the file/apk path to the relevent instance entrybox
        :param path:
        :return:
        """
        self.box.insert(tkinter.END,path)

    def get_box_value(self):
        return self.box.get("1.0", 'end-1c')


class SSID_creator(tk.Frame):

    def __init__(self,parent):
        # super().__init__(parent)
        # self.pack(fill=tk.X)

        self.ssid_box = tk.Text(parent, width=3, height=1)
        self.ssid_box.bind("<Tab>", self.focus_next_window)
        self.ssid_box.bind('<Key>', self.key_limit)
        self.ssid_box.pack(side=tk.LEFT, fill=tk.X, padx=5)



    def key_limit(self,event):
        """
        helper function for ssid fields, Limits number of ssid key
        """
        s = event.widget.get("1.0","end-1c")
        if len(s) > 1:
            event.widget.tk_focusNext().focus()

    def focus_next_window(self,event):
        """
        helper function for ssid fields, makes pressing tab skiping between ssid fields
        """
        event.widget.tk_focusNext().focus()
        return ("break")

    def get_str_value(self):
        return str(self.ssid_box.get("1.0",'end-1c'))

    def insert_val(self,value):
        self.ssid_box.insert(tkinter.END,value)
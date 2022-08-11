import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import *
import json
import re

class quick_scan_popup(object):
    """
        This Class is called when a new device is connected to the App,
        In case the device name is not known (Program identifies Devices by ID) then the user needs to add it,
        The local json file called udid_names.json will be updated.
        """

    def __init__(self, master,current_device):

        top = self.top = Toplevel(master)
        top.title("Quick Scan")
        self.current_device=current_device
        self.E = Entry(top)
        self.E.focus_set()
        self.E.bind('<Return>', self.auto_scan)
        self.E.pack(side=tk.LEFT,pady=10,padx=10)
        self.b = ttk.Button(top, text='Ok', width=5, command=self.auto_scan)
        self.b.pack(pady=10,padx=10)


    def auto_scan(self,string):
        self.value = self.E.get()
        ssid_clean=self.ssid_cleaner(self.value)
        if not self.current_device.ssid_1.get_str_value() and ssid_clean:
            self.current_device.ssid_1.insert_val(ssid_clean[0:3])
            self.current_device.ssid_2.insert_val(ssid_clean[3:6])
            self.current_device.ssid_3.insert_val(ssid_clean[6:9])

        self.top.destroy()

    def ssid_cleaner(self,dirty_str):
        m = re.search('ID=(.+?)&', dirty_str)
        if m:
            found = m.group(1)
        else:
            found= None
        return found

class popupWindow(object):
    """
    This Class is called when a new device is connected to the App,
    In case the device name is not known (Program identifies Devices by ID) then the user needs to add it,
    The local json file called udid_names.json will be updated.
    """

    def __init__(self,master,device_name,data_dict):
        self.device_name=device_name
        self.ud_dict=data_dict
        top=self.top=Toplevel(master)
        self.name_label=Label(top,text=f"Couldn't find {device_name}")
        self.name_label.pack()
        self.choose=Label(top,text="Choose Name:")
        self.choose.pack(side=tk.LEFT)
        self.E=Entry(top)
        self.E.pack(side=tk.LEFT)
        self.b=Button(top,text='Ok',width=5,command=self.cleanup)
        self.b.pack()

    def cleanup(self):
        self.value=self.E.get()
        with open("udid_names.json", "w") as write_content:
            data={self.device_name:self.value}
            self.ud_dict.update(data)
            json.dump(self.ud_dict, write_content)

        ##need a temporary memory value
        # udid_dict[self.device_name]=self.value
        self.top.destroy()
import sys
import time
import tkinter
import concurrent.futures
from multiprocessing.pool import ThreadPool
import threading, queue
import queue
import ctypes

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog  ##chosing directory
from tkinter.messagebox import showerror
from tkinter import messagebox
import re
from subprocess import check_output, CalledProcessError
from tkinter.ttk import Style, Progressbar
import gui_helpers
import helpers
import appium_helpers
import json
from Popup_helpers import popupWindow, quick_scan_popup
from datetime import datetime
from threading import Thread
from Devices_Dict import udid_dict, FieldsEmptyError, SSIDError, ApkNFolderError, BadApkName, num_dict, \
    AppiumConnectionError, ssid_dict
import FunTesting

# from helpers_no_gui import Tester
from frame_rate_helper import Frame_Rater


class Device(tk.Frame):
    """
    This class represents the device, from this class the tests initiates.
    """

    def __init__(self, parent, apk_sec, folder_sec, device_number,queue):
        tk.Frame.__init__(self, parent)

        self.master = parent
        self.stepper=10
        self.folder_path = folder_sec.get_box_value()
        self.apk_path = apk_sec.get_box_value()

        # # <editor-fold desc="To delete">
        # self.folder_path = r"C:/Users/GuyLeiba/Documents/Projtesting"
        # self.apk_path = r"C:/Users/GuyLeiba/Documents/Projtesting/inwall-prod-sensor-debug-3.14.4_change_frame_rate-710a9c84b_WalabotDIY_2022.01.10_v3.0.26-b03ed7ba.apk"
        # # </editor-fold>

        self.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=2)
        self.device_number = device_number
        self.queue=queue

        """"These three values will be initialize in adb_devices/set_devlog function"""
        self.run_in_progress=False
        self.udid_val = None
        self.device_real_name = None
        self.os_string = None
        self.desired_run_num=1
        self.desired_cool_num=1
        self.desired_scan_time=120

        dev_lbl = tk.Label(self, text=f'Device Number {device_number}:', width=18, anchor='w')
        dev_lbl.pack(side=tk.LEFT, padx=2, pady=5)

        # self.dev_name_box = tk.Text(self, width=20, height=1)
        # self.dev_name_box.pack(side=tk.LEFT, fill=tk.X, padx=5)

        """Initialize progress bar"""
        # <editor-fold desc="Each progress bar has its own layout called p{device number}.LabeledProgressbar">
        self.prog_bar_style = Style(self)
        self.prog_bar_style.layout("LabeledProgressbar",
                                   [('LabeledProgressbar.trough',
                                     {'children': [('LabeledProgressbar.pbar',
                                                    {'side': 'left', 'sticky': 'ns'}),
                                                   ("LabeledProgressbar.label",  # label inside the bar
                                                    {"sticky": ""})],
                                      'sticky': 'nswe'})])
        self.prog_bar = Progressbar(self, orient="horizontal", length=220,
                                    style=f"p{self.device_number}.LabeledProgressbar")
        self.prog_bar["value"] = 0
        self.prog_bar["maximum"] = 100
        self.prog_bar.pack(side=tk.LEFT, fill=tk.X, padx=2)

        # </editor-fold>

        """SSID boxes initialize"""
        walabot_lbl = tk.Label(self, text='SSID:', width=5, anchor='w')
        walabot_lbl.pack(side=tk.LEFT, padx=3, pady=5)
        self.ssid_1 = gui_helpers.SSID_creator(self)
        self.ssid_2 = gui_helpers.SSID_creator(self)
        self.ssid_3 = gui_helpers.SSID_creator(self)

        """Tests Number Combobox"""
        runs_lbl = tk.Label(self, text='Tests Number:', width=11, anchor='w')
        runs_lbl.pack(side=tk.LEFT, padx=5, pady=5)
        self.run_number = tk.StringVar()
        self.runcombo = ttk.Combobox(self, textvariable=self.run_number, width=3)
        self.runcombo['values'] = ('1', '2', '3', '4')
        self.runcombo['state'] = 'readonly'
        self.runcombo.current(0)
        self.runcombo.pack(side=tk.LEFT, padx=5, pady=5)

        """Scan Time Combobox"""
        scan_lbl = tk.Label(self, text='Scan Time:', width=8, anchor='w')
        scan_lbl.pack(side=tk.LEFT, padx=5, pady=5)
        self.scan_time = tk.StringVar()
        self.scancombo = ttk.Combobox(self, textvariable=self.scan_time, width=8)
        self.scancombo['values'] = ('60 sec', '120 sec', '180 sec')
        self.scancombo['state'] = 'readonly'
        self.scancombo.current(1)
        self.scancombo.pack(side=tk.LEFT, padx=5, pady=5)


        """Cooling Time Combobox"""
        cool_lbl = tk.Label(self, text='Cool Time:', width=8, anchor='w')
        cool_lbl.pack(side=tk.LEFT, padx=5, pady=5)
        self.cooling_time = tk.StringVar()
        self.coolcombo = ttk.Combobox(self, textvariable=self.cooling_time, width=5)
        self.coolcombo['values'] = ('1 min', '2 min', '5 min', '10 min')
        self.coolcombo['state'] = 'readonly'
        self.coolcombo.current(0)
        self.coolcombo.pack(side=tk.LEFT, padx=5, pady=5)


        self.start_btn = ttk.Button(self, text="Start Run", command=self.start_session_local)
        self.start_btn.pack(side=tk.LEFT, padx=5, pady=5)


    def set_devlog_name(self, ssid):
        """
        This function sets the devlog based on the device id, it gets the real device
        name from a file called devices_Dict
        devlog name will be- [device name]-[date-time]-[android version]-[ssid]
        :return:devlog name
        """
        """retrieve OS Version"""
        try:
            adb_version_command = check_output(
                ["adb", "-s", str(self.udid_val), "shell", "getprop", "ro.build.version.release"])
            os_string = str(adb_version_command)
            os_lst = re.findall(r'\d+', os_string)
            self.os_string = os_lst[0]
        except Exception:
            self.os_string = ""

        name = self.device_real_name.replace(" ", "-")
        return f"[{name}]-[SSID-{ssid}]-[OS-{self.os_string}]"



    def start_session_local(self):
        """This block of code checks if thread is already running"""
        try:
            if self.device_thread.join():
                return
        except AttributeError:
            pass

        """This block of code creates the dict"""
        try:
            device_dict = self.create_dict()
        except Exception:
            messagebox.showerror(title="Error",message="Please Fill All Device Fields")
            return
        self.start_session_helper(device_dict)

    def start_session(self):
        """
        This function creates the uniqe device dict and pass it to the parent class
        the parent class starts the test session
        """

        """This block of code checks if thread is already running"""
        try:
            if self.device_thread.join():
                return
        except AttributeError:
            pass

        """This block of code creates the dict"""
        try:
            device_dict = self.create_dict()
        except Exception:
            raise FieldsEmptyError

        self.start_session_helper(device_dict)


    def start_session_helper(self,device_dict):
        """An helper function that helps me to cope with multiple messagebox error. """

        self.device_thread = ThreadedTask(self.queue)
        self.start_btn.config(state='disabled')
        self.device_thread.value_dict = device_dict
        self.device_thread.udid = self.udid_val
        self.device_thread.start()

    def get_package(self):
        """
        This function extract the package name from the apk file, so the appium session could start
        :return:nothing, sets up self.package_name
        """
        if "prod" in str(self.apk_path):
            return "com.walabot.vayyar.ai.plumbing"
        elif "dev" in str(self.apk_path):
            return "com.walabot.test"
        elif "stg" in str(self.apk_path):
            return "com.walabot.test"
        else:
            print(self.apk_path)
            raise BadApkName



    def change_prog_bar(self, color=None, value=None, message=None):

        if value:
            """reset value"""
            if value==0.1:
                self.prog_bar['value'] = 0
            else:
                self.prog_bar['value'] = value
        else:
            self.prog_bar.step(self.stepper)

        if color and message:
            self.prog_bar_style.configure(f"p{self.device_number}.LabeledProgressbar", foreground='black',
                                                 background=color, text=f"{message}     ")
        elif message:
            self.prog_bar_style.configure(f"p{self.device_number}.LabeledProgressbar",
                                                 text=f"{message}     ")


    def create_dict(self):
        """
        This function creates the dictionary for the device and sends it to start session
        """

        walabot_ssid = self.ssid_1.get_str_value() + self.ssid_2.get_str_value() + self.ssid_3.get_str_value()

        temp_cool_num=self.cooling_time.get()
        self.desired_cool_num = int(temp_cool_num.replace("min", ""))

        temp_scan_time = self.scan_time.get()
        self.desired_scan_time = int(temp_scan_time.replace("sec", ""))

        self.desired_run_num = int(self.run_number.get())
        package = self.get_package()

        """This section checks that all values are full, in case of error it will be send to start_session_local"""
        if self.udid_val == None:
            raise FieldsEmptyError
        if self.folder_path == '' or self.apk_path == '':
            raise ApkNFolderError
        # <editor-fold desc="To return">
        if len(walabot_ssid) != 9:
            raise SSIDError
        # </editor-fold>

        self.devlog_name=self.set_devlog_name(walabot_ssid)
        dict = {

            "walabot_ssid": walabot_ssid,
            "app_package": package,
            "device": self,

            #"devlogname": self.set_devlog_name(walabot_ssid),

            # <editor-fold desc="To delete">
            # "walabot_ssid": ssid_dict[self.device_number],
            # </editor-fold>

        }

        return dict




class MainWindow(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        frame = tk.Frame(self)
        frame.pack()

        #self.bind("<<start>>", self.count_events)  # bind to event

        self.at_least_one_run= False
        self.after(100, self.process_queue)

        self.counter=0
        """Initialize default values"""
        self.device_number = 1
        self.apk_path = ""
        self.folder_selected = ""
        self.checking_thread=None
        self.appium_started_indicator=False
        self.all_devices_dict = {}
        self.thread_dict={}
        self.queue = queue.Queue()


        # # <editor-fold desc="To delete">
        # self.folder_selected = r"C:/Users/GuyLeiba/Documents/Projtesting"
        # self.apk_path = r"C:/Users/GuyLeiba/Documents/Projtesting/inwall-prod-sensor-debug-3.14.4_change_frame_rate-710a9c84b_WalabotDIY_2022.01.10_v3.0.26-b03ed7ba.apk"
        # # </editor-fold>

        """All device related in the main frame"""
        self.label = tk.Label(self)
        self.add_btn = ttk.Button(frame, text="Add Device", command=self.add_and_pack)
        self.refresh_device = ttk.Button(frame, text="Refresh Devices", command=self.adb_device)
        self.quick_qr_scan = ttk.Button(frame, text="Quick QR Scan", command=self.quick_scan_popup)
        self.start_all=ttk.Button(frame, text="Start All & Analyze", command=self.drop_ta_bomb)


        """Get all the udid_names"""
        with open("udid_names.json", "r") as read_content:
            self.udid_dict = json.load(read_content)

        """APK and Folder buttons and labels."""
        self.apk_button = ttk.Button(self, text='  Choose APK  ',command=self.choose_file)
        self.folder_button = ttk.Button(self, text='Choose Folder',command=self.dir_chooser)
        self.apk_sec = gui_helpers.LabelEntry(frame, "Choose Apk:", self.apk_button)
        self.folder_sec = gui_helpers.LabelEntry(frame, "Choose Devlogs Containing Folder:", self.folder_button)

        """Packing"""
        self.add_btn.pack(side=tk.LEFT, padx=5, pady=5)
        self.refresh_device.pack(side=tk.LEFT, padx=5, pady=5)
        self.quick_qr_scan.pack(side=tk.LEFT, padx=5, pady=5)
        self.start_all.pack(side=tk.RIGHT, padx=5, pady=5)

    def choose_file(self):
        """
        tkinter function that allows the user to choose the apk file.
        """
        self.apk_path = filedialog.askopenfilename(title="Open file")
        self.apk_sec.insert(self.apk_path)

    def dir_chooser(self):
        """
        tkinter function that allows the user to choose the containing devlogs directory
        """
        self.folder_selected = filedialog.askdirectory(title="Choose folder")
        self.folder_sec.insert(self.folder_selected)

    def add_and_pack(self):
        """
        This function adds a new device to frame, packs it into the frame
        and adds its instance to all_device_dict dictionary.
        """

        if self.apk_path == "":
            messagebox.showerror(title="Error", message="Please Choose apk first")
            return
        if self.folder_selected == "":
            messagebox.showerror(title="Error", message="Please Choose folder first")
            return

        self.all_devices_dict[self.device_number] = Device(self, self.apk_sec, self.folder_sec,self.device_number,self.queue)
        self.all_devices_dict[self.device_number].pack()
        self.frame_rate=Frame_Rater(self.folder_selected)
        self.device_number += 1

    def new_device_popup(self, device_name, data_dict):
        """
        This function is related to POPUP class, it simply generates a new pop up window
        and sends the desired values, one of them is data_dict which is all the known devices names.
        """
        self.w = popupWindow(self.master, device_name, data_dict)
        self.master.wait_window(self.w.top)

    def quick_scan_popup(self):
        """
        This function is related to Quickscanclass class, it simply generates a new pop up window
        it checks if there are devices in the gui, if not it will pop an error message
        then it will update the devices list
        """
        if self.all_devices_dict:
            for device in self.all_devices_dict.values():
                if device.ssid_1.get_str_value():
                    continue
                else:
                    self.w = quick_scan_popup(self.master, device)
                    self.master.wait_window(self.w.top)
        else:
            messagebox.showerror(title="Error", message=f"No Devices Connected")

    def adb_device(self):
        """
        This function is being called when refresh devices is pressed.
        This function detects the android phones that is currently connected to the computer
        the function inserts the devices names to the devices boxes and assignees them to the device variables
        it uses regex to get the device names
        """


        """Clear All Progress Bars"""
        for index, device in enumerate(self.all_devices_dict.values()):

            """Check if the current device is in an active session"""
            try:run_in_prog = device.device_thread.join()
            except AttributeError:run_in_prog = False

            """If the device doesn't have an active session, clear progress bar"""
            if not run_in_prog:
                device.change_prog_bar("white","0.1","      ")

        """Create The device list"""
        try:
            adb_ouput = check_output(["adb", "devices"])
            self.device_lst = re.findall(r"[0-9a-zA-Z]{9,}", str(adb_ouput))
            self.device_lst = [e[1:] for e in self.device_lst]
        except CalledProcessError as e:
            print(e.returncode)

        """Alert if USB Debugging is not enabled"""
        if "unauthorized" in self.device_lst:
            self.device_lst.remove("unauthorized")
            messagebox.showerror(title="Attention", message=f"One Of The Devices Has USB Debugging Disabled")

        """check that UDID dict is updated"""
        for device_name in self.device_lst:
            if not device_name in self.udid_dict:
                self.new_device_popup(device_name, self.udid_dict)

        for index, device in enumerate(self.all_devices_dict.values()):
            """Check if the current device is in an active session"""
            try:run_in_prog = device.device_thread.join()
            except AttributeError:run_in_prog = False
            try:
                if not run_in_prog:
                    device.prog_bar_style.configure(f"p{index + 1}.LabeledProgressbar",
                                                    text=f"{self.udid_dict[self.device_lst[index]]}     ")

                device.udid_val = self.device_lst[index]
                device.device_real_name = self.udid_dict[self.device_lst[index]]

            except IndexError:
                pass
            except KeyError:
                messagebox.showerror(title="Error", message=f"Could not Find {self.device_lst[index]} in device list")



    def drop_ta_bomb(self):
        """This function starts all the tests in the same time."""

        """Check if all the fields are filled"""
        not_all_field=False
        for device in self.all_devices_dict.values():
            try:
                device.start_session()
            except FieldsEmptyError:
                not_all_field=True
        if not_all_field:
            messagebox.showerror(title="Error",
                                     message="Please Fill All Fields\nOnly Relevant Devices Tests Started")

    def process_queue(self):

        if self.queue.empty():
            if self.at_least_one_run:
                messagebox.showinfo(title="Info", message="All Runs Are Done!")
                self.frame_rate.trigger_analyzer()
                #FunTesting.fire(self)
                self.at_least_one_run = False

        else:
            self.at_least_one_run = True  ###Meaning There is one device That is running
        self.after(100, self.process_queue)



class ThreadedTask(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.value_dict=None
        self._return = None


    def run(self):

        local_test = appium_helpers.Tester(self.value_dict)
        self._return=True
        self.queue.put_nowait(1)
        local_test.start_test()
        self._return= False
        self.queue.get_nowait()

    def join(self):
        return self._return


if __name__ == "__main__":
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    root = tk.Tk()
    MainWindow(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

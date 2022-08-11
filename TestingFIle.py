import threading

from selenium.common.exceptions import InvalidSessionIdException, NoSuchElementException, ElementNotVisibleException
import sys, os
import time
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import *
from appium import webdriver
from subprocess import call
import re
import json
from datetime import datetime
from loguru import logger
from subprocess import check_output, CalledProcessError
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.extensions.android.nativekey import AndroidKey
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.wait import WebDriverWait
from urllib3.exceptions import MaxRetryError
#
# from Devices_Dict import num_dict, InsideElementError, FlagElementCouldNotFound, ScanInProgress, SignInError, \
#     AppiumConnectionError
#
# import base64
#
#
# class Tester():
#
#     def __init__(self, value_dict):
#
#         self.port_num = value_dict["port_num"]
#         self.walabot_ssid = value_dict["walabot_ssid"]
#         self.app_package_prod = value_dict["app_package"]
#         self.app_package_test="com.walabot.test"
#         self.devlog_name = value_dict["devlogname"]
#         self.udid_val= value_dict["deviceid"]
#         self.apk_path=value_dict["apk_path"]
#         self.test_path=value_dict["test_path"]
#
#         self.test_base_caps={
#
#             "appium:udid": self.udid_val,
#             "appium:appPackage": self.app_package_test,
#             "appium:systemPort": self.port_num,
#             "app": self.test_path,
#             "appActivity": "com.walabot.vayyar.ai.plumbing.presentation.MainActivity",
#             "platformName": "Android",
#             "appium:automationName": "uiautomator2",
#             "appium: autoLaunch": "false",
#             "appium:newCommandTimeout": 10,
#             "noReset": "true",
#             "fullReset": "false"
#
#         }
#
#         self.prod_caps ={
#             "appium:udid": self.udid_val,
#             "appium:appPackage": self.app_package_prod,
#             "appium:systemPort": self.port_num,
#             "app": self.apk_path,
#             "appActivity": "com.walabot.vayyar.ai.plumbing.presentation.MainActivity",
#             "platformName": "Android",
#             "appium:automationName": "uiautomator2",
#             "appium: autoLaunch": "false",
#             "appium:newCommandTimeout": 10,
#             "noReset": "true",
#             "fullReset": "false"
#         }
#
#     def start_test_prod(self):
#
#         try:
#             self.driver = webdriver.Remote("http://localhost:4723/wd/hub", self.prod_caps)
#         except Exception as e:
#             if "INSTALL_FAILED_CONFLICTING_PROVIDER" in str(e):
#                 time.sleep(10)
#                 self.driver = webdriver.Remote("http://localhost:4723/wd/hub", self.test_base_caps)
#                 self.driver.remove_app("com.walabot.test")
#
#         self.appium_connection(self.prod_caps)
#
#     def start_test_stg(self):
#         try:
#             self.driver = webdriver.Remote("http://localhost:4723/wd/hub", self.test_base_caps)
#         except Exception as e:
#             if "INSTALL_FAILED_CONFLICTING_PROVIDER" in str(e):
#                 time.sleep(10)
#                 self.driver = webdriver.Remote("http://localhost:4723/wd/hub",self.prod_caps)  ##create session
#                 self.driver.remove_app("com.walabot.vayyar.ai.plumbing")
#
#             # self.driver = webdriver.Remote("http://localhost:4723/wd/hub", self.base_caps)  ##create session
#
#     def appium_connection(self, base_caps):
#         try:
#             self.driver = webdriver.Remote("http://localhost:4723/wd/hub", base_caps)
#         except Exception as e:
#             pass
#
#
#
#         # print(self.driver.is_app_installed(self.test_path))
#         # if (self.driver.is_app_installed(self.app_package)):
#         #     self.driver.remove_app(self.app_package)
#
#         # time.wait()
#         # try:
#         #     self.driver.close_app()
#         #     self.driver.quit()
#         # except Exception:
#         #     self.context_logger.trace(f"404 Couldn't close connection")
#
# choosen_folder=r"C:\Users\GuyLeiba\Documents\Projtesting"
# app_package = "com.walabot.vayyar.ai.plumbing"
# app_apk=r'C:\Users\GuyLeiba\Desktop\3Testing\inwall-prod-sensor-debug-3.14.07_58-add-new-sdk.apk'
# test_apk=r'C:\Users\GuyLeiba\Desktop\3Testing\inwall-dev-sensor-debug-3.14.07_58-add-new-sdk.apk'
# devlogname="new.txt"
#
# dict1={
#     "test_path":test_apk,
#     "apk_path":app_apk,
#     "folder":choosen_folder,
#     "app_package":app_package,
#     "deviceid":"R58M38BXYTX",
#     "port_num":8202,
#     "walabot_ssid":801_402_666,
#     "devlogname":devlogname,
# }
# test1=Tester(dict1)
# test1.start_test_prod()
#
# def take_screenshot(self):
#     screenshotBase64 = self.driver.get_screenshot_as_base64()
#     with open(f"{self.folder_path}\imageToSave.png", "wb") as fh:
#         fh.write(base64.b64decode(screenshotBase64))

# import queue
# class GUI:
#     def __init__(self, master):
#         self.master = master
#         self.test_button = tk.Button(self.master, command=self.tb_click)
#         self.test_button.configure(
#             text="Start", background="Grey",
#             padx=50
#             )
#         self.test_button.pack(side=TOP)
#
#     def progress(self):
#         self.prog_bar = ttk.Progressbar(
#             self.master, orient="horizontal",
#             length=200, mode="indeterminate"
#             )
#         self.prog_bar.pack(side=TOP)
#
#
#     def tb_click(self):
#         self.progress()
#         self.prog_bar.start()
#         self.queue = queue.Queue()
#         ThreadedTask(self.queue).start()
#         self.master.after(100, self.process_queue)
#
#     def process_queue(self):
#         try:
#             msg = self.queue.get_nowait()
#             print(msg)
#             # Show result of the task if needed
#             self.prog_bar.stop()
#         except queue.Empty:
#             self.master.after(100, self.process_queue)
#
# class ThreadedTask(threading.Thread):
#     def __init__(self, queue):
#         super().__init__()
#         self.queue = queue
#     def run(self):
#         time.sleep(5)  # Simulate long running process
#         self.queue.put("Task finished")
#
# root = Tk()
# root.title("Test Button")
# main_ui = GUI(root)
# root.mainloop()

# from tkinter import *
# import datetime
# import threading
# import time
#
# root = Tk()
# root.title("Thread Test")
# print('Main Thread', threading.get_ident())    # main thread id
#
# def timecnt():  # runs in background thread
#     print('Timer Thread',threading.get_ident())  # background thread id
#     for x in range(10):
#         root.event_generate("<<event1>>", when="tail", state=123) # trigger event in main thread
#         txtvar.set(' '*15 + str(x))  # update text entry from background thread
#         time.sleep(1)  # one second
#
# def eventhandler(evt):  # runs in main thread
#     print('Event Thread',threading.get_ident())   # event thread id (same as main)
#     print(evt.state)  # 123, data from event
#     string = datetime.datetime.now().strftime('%I:%M:%S %p')
#     lbl.config(text=string)  # update widget
#     #txtvar.set(' '*15 + str(evt.state))  # update text entry in main thread
#
# lbl = Label(root, text='Start')  # label in main thread
# lbl.place(x=0, y=0, relwidth=1, relheight=.5)
#
# txtvar = StringVar() # var for text entry
# txt = Entry(root, textvariable=txtvar)  # in main thread
# txt.place(relx = 0.5, rely = 0.75, relwidth=.5, anchor = CENTER)
#
# thd = threading.Thread(target=timecnt)   # timer thread
# thd.daemon = True
# thd.start()  # start timer loop
#
# root.bind("<<event1>>", eventhandler)  # event triggered by background thread
# root.mainloop()
# thd.join()  # not needed

import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
import time


class Application:
    def __init__(self, master):
        # set main window
        frame = tk.Frame(master, width=300, height=100)
        frame.pack(fill=tk.BOTH)

        # button widget
        run_button = tk.Button(frame, text="GO", command=self.do_something)
        run_button.pack()

        # simulate some gui input from user
        self.user_input = "specified by user"

    def do_something(self):
        thread1 = Thread(target=FunctionClass, args=(self.user_input,))
        thread1.start()  # launch thread
        ProgressWindow()  # main thread continues to new tkinter window


class ProgressWindow(tk.Toplevel):
    """ displays progress """

    def __init__(self):
        super().__init__()

        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="indeterminate")
        self.progress.pack()
        self.note = "Processing data..."
        self.p_label = tk.Label(self, text=self.note)
        self.p_label.pack()
        self.progress.start(50)


class FunctionClass:
    """ thread1 works on this class """

    def __init__(self, user_data):
        self.user_data = user_data
        self.do_something_else()

    def do_something_else(self):
        # simulate thread 1 working
        time.sleep(3)
        print("Thread1 job done")
        # call <<stop>> virtual event (unsure if 'tail' is necessary here)
        root.event_generate("<<stop>>", when="tail")


def end_program(*args):
    """ called with tkinter event_generate command after thread completion """
    messagebox.showinfo("Complete", "Processing Complete")
    root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    Application(root)
    root.bind("<<stop>>", end_program)   # bind to event
    root.mainloop()
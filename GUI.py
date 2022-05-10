import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog  ##chosing directory
from tkinter.messagebox import showerror
from helpers import main_session


class App(tk.Tk):

    def __init__(self):
        super().__init__() # create window

        self.title('Temperature Converter')
        #self.geometry("540x320")
        self.geometry("540x320")
        self.resizable(False, False)

class ButtonFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # field options
        space = {'padx': 5, 'pady': 5}
        # self.columnconfigure(0, weight=7)
        # self.columnconfigure(1, weight=3)
        # self.columnconfigure(2, weight=1)
        frame_apk = tk.Frame(master=self).pack(side=tk.TOP)
        frame_folder = tk.Frame(master=self).pack(side=tk.TOP)
        frame_check = tk.Frame(master=self).pack(side=tk.TOP)
        frame_error = tk.Frame(master=self).pack(side=tk.TOP)

        #self.filename = "" # variable to store filename

        self.apk_button = ttk.Button(master=frame_apk, text='Choose APK')
        self.apk_button['command'] = self.choose_file
        #self.apk_button.grid(column=2, row=0, sticky=tk.E, **space)

        # apk label
        self.apklabel = ttk.Label(master=frame_apk,text='APK File Location:')
        #self.apklabel.grid(column=0, row=0, sticky=tk.W, **space)

        ##APK Text box
        self.apk_box = tk.Text(master=frame_apk, width=30, height=1)
        #self.apk_box.grid(column=1, row=0, sticky=tk.W, **space)

        self.apklabel.pack(side=tk.LEFT,**space)
        self.apk_box.pack(side=tk.LEFT,**space)
        self.apk_button.pack(side=tk.LEFT,**space)

###########Folder#####

        #choose folder button
        self.folder_button = ttk.Button(frame_folder, text='Choose Folder')
        self.folder_button['command'] = self.dir_chooser
        #self.apk_button.grid(column=2, row=1, sticky=tk.E, **space)

        # folder label
        self.folderlabel = ttk.Label(frame_folder,text='Containing Folder Location:')
        #self.folderlabel.grid(column=0, row=1, sticky=tk.W, **space)

        ##Folder Text box
        self.folder_box = tk.Text(frame_folder, width=30, height=1)
        #self.folder_box.grid(column=1, row=1, sticky=tk.W, **space)

        self.folderlabel.pack(side=tk.LEFT, **space)
        self.folder_box.pack(side=tk.LEFT, **space)
        self.folder_button.pack(side=tk.LEFT, **space)

        ########start
        self.start_button = ttk.Button(frame_check, text='Start')
        self.start_button['command'] = self.init_session
        #self.apk_button.grid(column=2, row=2, sticky=tk.E, **space)



#################Error Section

        ##error label
        self.error_label = ttk.Label(frame_error,text='Error Description:')
        #self.error_label.grid(column=0, row=3, sticky=tk.W, **space)

        ##error box
        self.error_box = tk.Text(frame_error, width=50,height=8)
        #self.error_box.grid(column=0, row=4, sticky=tk.W,**space)

        self.error_label.pack(side=tk.LEFT, **space)
        self.error_box.pack(side=tk.LEFT, **space)

        # add padding to the frame and show it

        #self.grid(padx=10, pady=10, sticky=tk.NSEW)


    def choose_file(self):
        self.file_path = filedialog.askopenfilename(title="Open file")
        self.apk_box.insert("1.0",self.file_path)
        #self.apklabel.config(text=self.file_path)

    def dir_chooser(self):  ##Choosing Diractory
        self.folder_selected = filedialog.askdirectory(title="Choose folder")
        self.folder_box.insert("1.0",self.folder_selected)
        #self.folderlabel.config(text=self.folder_selected)

    def init_session(self):
        apk_path = str(self.file_path)
        folder=str(self.folder_selected)
        apk_package="com.walabot.test"
        self.error_message=main_session(apk_package,apk_path,folder)
        self.error_box.insert("1.0",self.error_message)

    def report_callback_exception(self, exc, val, tb):
        showerror("Error", message=str(val))

class TextFrame(ButtonFrame):
    def __init__(self, container):
        super().__init__(container)

if __name__ == '__main__':
    app = App()
    ButtonFrame(app)
    app.mainloop()
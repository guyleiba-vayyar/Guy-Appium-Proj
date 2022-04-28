from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
from tkinter import filedialog as fd




# This function will be used to open
# file in read mode and only APK files
# will be opened
def choose_file():
    global file_path
    file_path = filedialog.askopenfilename()
    return file_path


##This is the main window ''root'' and setting up its geometry
root = Tk()
root.geometry("500x320")
root.title('Login')

#configure the grid
root.columnconfigure(0, weight=5)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=2)
root.rowconfigure(2, weight=2)


frm = ttk.Frame(root, padding=10)

txt_frame = ttk.Frame(root).grid(column=2, row=3)
ttk.Label(frm, text="Hello World!").grid(column=0, row=0)

device_namebox = Text(root,width=60,height=20)
device_namebox.grid(column=0, row=0, padx=5, pady=5)



ttk.Button(root, text="Quit", command=root.destroy).grid(column=2, row=3, padx=10, pady=10)
file_path = ttk.Button(root, text="Browse", command=choose_file).grid(column=2, row=0, padx=10, pady=10)


root.mainloop()

print(file_path)
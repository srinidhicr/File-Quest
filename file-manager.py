"""
Title : File Explorer 
Team Members : Harini, Srinithi
"""

import os,configparser,re,sys,string
#from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk ,Image
from pathlib import Path
from send2trash import send2trash

#Size of the file
def find_size(name):
    fSize = os.stat(name).st_size
    if fSize < 1000:
        size = str(fSize) + " B"
    if fSize >= 1000:
        size = str(round(fSize/1000, 2)) + " KB"
    if fSize >= 1000000:
        size = str(round(fSize/1000000, 2)) + " MB"
    if fSize >= 1000000000:
        size = str(round(fSize/1000000000, 2)) + " GB"
    if fSize >= 1000000000000:
        size = str(round(fSize/1000000000000, 2)) + " TB"
    return [size, fSize]

#Updation of files and folders
def update_files_folders(dirname):
    global last_path
    size_list = []
    count = 0
    # files in current path
    file_list = os.listdir(dirname)

    # Reverse sorting
    if reverse == False:
        file_list.sort(key=str.lower)
    else:
        file_list.sort(key=str.lower, reverse=True)
        
    # Scan folders
    for fName in file_list:
        fullPath = os.path.join(dirname, fName)
        fName=f"   {fName}"
        size = find_size(fullPath)
        if os.path.isdir(fullPath):
            tree.insert("", tk.END, text=fName, values=["<dir>",fullPath], open=False, image=folder_icon)
            count += 1
        else:continue
    
    # Scan files
    for fName in file_list:
        fullPath = os.path.join(dirname, fName)
        fName=f"   {fName}"
        size = find_size(fullPath)  
        if sort_size == True:
            if os.path.isdir(fullPath):
                continue
            else:
                size_list = [size[1], fullPath, fName, size[0]]
                size_list.append(size_list)
        else:
            if os.path.isdir(fullPath):
                    continue
            else:
                tree.insert("", tk.END, text=fName, values=[size[0], fullPath], open=False, image=file_icon)
                count += 1
                
    #Sorting
    if sort_size == True:
        if reverse == False:
            size_list.sort(key=lambda size_list: size_list[0], reverse=True)
        if reverse == True:
            size_list.sort(key=lambda size_list: size_list[0])
        for s in size_list:
            tree.insert("", tk.END, text=s[2], values=[s[3], s[1]], open=False, image=file_icon)
            count += 1
        size_list.clear()
    
    entry.insert("end", dirname)
    label["text"]=f"   {str(count)} objects"
    last_path = dirname
    # Set title = folder name
    if re.match(r"\w:\\$", dirname):
        window.title(f"Disk ({dirname[0:2]})")
    elif dirname == "\\":
        window.title("Computer")
    else:
        window.title(dirname.rsplit("\\", 1)[1])
                
def drive_buttons():
    letters = string.ascii_uppercase
    letter_count = 0
    column = 2
    for i in range(26):
        drive = letters[letter_count]
        if os.path.exists(f"{drive}:{'/'}"):
            tk.Button(frame_b, text=drive.lower(), font=("Arial", 14), relief="flat", bg="pink", fg="black",command=lambda drive=drive:update_files_folders(f"{drive}:{'/'}")).grid(column=column, row=1)
            column += 1
        letter_count += 1
            
def select():
    if len(tree.selection()) > 0:
        right_menu.entryconfig("Open", state="normal")
        """
        right_menu.entryconfig("Copy", state="normal")
        right_menu.entryconfig("Rename", state="normal")
        right_menu.entryconfig("Delete in trash", state="normal")"""

def click():
    paths = [tree.item(i)["values"][1] for i in tree.selection()]
    for i in tree.selection():
        print(i)
    stop = False
    for path in paths:
        if os.path.isdir(path):
            if stop == False:
                update_files_folders(path)
                stop = True
        else:
            if sys.platform == "win32":
                os.startfile(path)
        
parent_path=str(Path.home())
last_path=None
reverse=False
sort_size=False


window=tk.Tk()
window.resizable(True, True)
window.iconphoto(True,tk.PhotoImage(file="imgFolder/icon.png"))
window.minsize(width=800, height=500)
frame_up = tk.Frame(window, border=1,bg="blue")
frame_up.pack(fill="x", side="top")


folder_icon = tk.PhotoImage(file="imgFolder/icon_folder.png")
file_icon = tk.PhotoImage(file="imgFolder/icon_file.png")
home_icon = tk.PhotoImage(file="imgFolder/icon_home.png")
up_icon = tk.PhotoImage(file="imgFolder/icon_up.png")
frame_b = tk.Frame(frame_up, border=2, relief="groove", bg="blue")
frame_b.pack(side="left")

tk.Button(frame_b, image=up_icon, width=25, height=32, relief="flat", bg="pink", fg="black").grid(column=0, row=1)
tk.Button(frame_b, image=home_icon, width=25, height=32, relief="flat", bg="pink", fg="black",command=lambda:update_files_folders(parent_path)).grid(column=1, row=1)
entry = tk.Entry(frame_up, font=("Arial", 12), justify="left", highlightcolor="white", relief="groove", border=2)
entry.pack(side="right",fill="both", expand=1)
label = tk.Label(window, font=("Arial", 12), anchor="w", bg="#856ff8", fg="black", border=2)
label.pack(side="bottom",fill="both")

treeFrame = tk.Frame(window, border=1, relief="flat", bg="blue")
treeFrame.pack(expand=1, fill="both")
tree =ttk.Treeview(treeFrame, columns=("#1"), selectmode="extended", show="tree headings")
tree.heading("#0", text="   Name", anchor="w")
tree.heading("#1", text="Size", anchor="w")
tree.column("#0", anchor="w")
tree.column("#1", anchor="e", stretch=False, width=120)
tree.pack(side="left", expand=1, fill="both")
treeStyle=ttk.Style()
treeStyle.theme_use("clam")
treeStyle.configure("Treeview.Heading",background="#856ff8")
scrollbar = ttk.Scrollbar(treeFrame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right",fill="y")


right_menu = tk.Menu(treeFrame, tearoff=0, font=("Arial", 12))
right_menu.add_command(label="Open", command=click, state="disabled")
#right_menu.add_command(label="Copy", command=copy, state="disabled")
#right_menu.add_command(label="Rename", command=rename, state="disabled")
#right_menu.add_command(label="Delete in trash", command=delete, state="disabled")
#right_menu.add_separator()
#right_menu.add_command(label="Paste", command=paste, state="disabled")
#right_menu.add_separator()
right_menu.bind("<FocusOut>", lambda event:right_menu.unpost())# Click elsewhere - close right click menu
right_menu.bind("<FocusOut>", lambda event:right_menu.unpost())
drive_buttons()
update_files_folders(parent_path)
tree.focus_set()

#bind keyboard keys to a function
tree.bind("<<TreeviewSelect>>", lambda event:select())
entry.bind("<Return>", lambda event:update_files_folders(entry.get()))
tree.bind("<Return>", lambda event:click())
tree.bind("<BackSpace>", lambda event:move_up())
tree.bind("<Up>", lambda event:up_down_focus())
tree.bind("<Down>", lambda event:up_down_focus())
tree.bind("<Delete>", lambda event:delete())
tree.bind("<Control-c>", lambda event: copy())
tree.bind("<Control-v>", lambda event: paste() if right_menu.entrycget(index=5, option="state") == "normal" else None)
#entry.bind("<KP_Enter>", lambda event:update_files_folders(entry.get()))
window.mainloop()

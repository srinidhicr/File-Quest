import os,re,string,shutil
import tkinter as tk
from tkinter import ttk , simpledialog
from PIL import ImageTk ,Image
from pathlib import Path
from tkinter.messagebox import askyesno
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

#Sorting 
def sort_name_reverse():
    global reverse
    global sort_size
    if sort_size == True:
        sort_size = False
    elif sort_size == False:
        if reverse == False:
            reverse = True
        elif reverse == True:
            reverse = False
    update_files_folders(entry.get())
    
def sort_size_reverse():
    global reverse
    global sort_size
    if sort_size == False:
        sort_size = True
    elif sort_size == True:
        if reverse == False:
            reverse = True
        elif reverse == True:
            reverse = False
    update_files_folders(entry.get())

#Right click Menu - PopUp
def open_right_menu(event):
    try:
        right_menu.tk_popup(event.x_root, event.y_root)
    finally:
        right_menu.grab_release()
        
#To Move to Previous folder
def move_up():
    global curr_folder
    up_path = entry.get().rsplit("\\", 1)
    curr_folder = up_path[1]
    if re.match(r"\w:$", up_path[0]) or up_path[0] == "":
        update_files_folders(up_path[0] + "\\")
    else:
        update_files_folders(up_path[0])

#To create a copy of a file
def copy():
    if len(tree.selection()) > 0:
        path_list = []
        for i in tree.selection():
            path = tree.item(i)["values"][1]  # [size[1], fullPath, fName, size[0]]
            if "\\" in path:
                path = path.replace("\\", "/")
            path_list.append(f"'{path}'")
        if len(path_list) > 1:
            items = ",".join(path_list)     
        else:
            items = path_list[0]
        os.system(f"powershell.exe Set-Clipboard -path {items}")
        right_menu.entryconfig("Paste", state="normal")

#To paste the copied file
def paste():
    clipboard = window.selection_get(selection="CLIPBOARD").replace("/", "\\").split("\n")
    for source in clipboard:
        edit = source.rsplit("\\", 1)
        
        # Search file/folder copies
        file_copies = 1
        for f in os.listdir(entry.get()):
            if f == edit[1]:
                file_copies += 1
        if file_copies > 1:
            while True:
                for f in os.listdir(entry.get()):
                    if f == f"({file_copies})" + edit[1]:
                        file_copies += 1
                        continue
                break
            destination = entry.get() + "\\" + f"({file_copies})" + edit[1]
        else:
            destination = entry.get() + "\\" + edit[1]
        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)
    update_files_folders(entry.get())
    
#To delete
def delete():
    try:
        del_list = []
        for i in tree.selection():
            del_path = tree.item(i)["values"][1]
            if os.path.exists(del_path):
                del_list.append(del_path)
        answer = askyesno(title="Files", message=f"Delete {len(tree.selection())} objects in trash?")
        if answer:
            for di in del_list:
                send2trash(di)
    except:pass
    update_files_folders(entry.get())
    
#To rename a file
def rename():
    for i in tree.selection():
        r_path = tree.item(i)["values"][1]
        e_path = r_path.rsplit("\\", 1)
        if os.path.exists(r_path):
            answer = simpledialog.askstring(title="Files", prompt=f"Rename '{e_path[1]}'", parent=treeFrame, initialvalue=e_path[1])
            if answer is not None:
                rename_str = e_path[0] + "\\" + answer
                os.rename(r_path, rename_str)
    update_files_folders(entry.get())
    
#Updation of files and folders
def update_files_folders(dirname):
    global last_path
    size_list = []
    count = 0
    # files in current path
    try:
        file_list = os.listdir(dirname)
    except Exception as e:
        if "Access is denied" in str(e):
            tk.messagebox.showerror(title="ERROR", message=e)
        dirname = parent_path
        if last_path != None:
            dirname = last_path
        file_list = os.listdir(dirname)
        
    # Clean old
    for item in tree.get_children():
        tree.delete(item)
    entry.delete(0, "end")
    
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
                size_list_1 = [size[1], fullPath, fName, size[0]]
                size_list.append(size_list_1)
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
    
    right_menu.entryconfig("Open", state="disabled")
    right_menu.entryconfig("Copy", state="disabled")
    right_menu.entryconfig("Rename", state="disabled")
    right_menu.entryconfig("Delete in trash", state="disabled")
    right_menu.entryconfig("Paste", state="disabled")
    
    # Focus on the folder from which you returned
    if tree.focus() == "" and curr_folder != None:
        for item in tree.get_children():
            if tree.item(item)["text"] == f"  {curr_folder}":
                tree.selection_set(item)
                tree.focus(item)
                tree.see(item)
                break
      
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
    right_menu.entryconfig("Open", state="normal")
    right_menu.entryconfig("Copy", state="normal")
    right_menu.entryconfig("Rename", state="normal")
    right_menu.entryconfig("Delete in trash", state="normal")

def remove_selection():
    tree.selection_remove(tree.focus())
    right_menu.entryconfig("Open", state="disabled")
    right_menu.entryconfig("Copy", state="disabled")
    right_menu.entryconfig("Rename", state="disabled")
    right_menu.entryconfig("Delete in trash", state="disabled")
    
def click():
    paths = [tree.item(i)["values"][1] for i in tree.selection()]#values list of col values - second col path
    stop = False
    for path in paths:
        if os.path.isdir(path):
            if stop == False:
                update_files_folders(path)
                stop = True
        else:
            os.startfile(path)

        
parent_path=str(Path.home())
curr_folder=None
last_path=None
reverse=False
sort_size=False

#Main Window
window=tk.Tk()
window.resizable(True, True)
window.iconphoto(True,tk.PhotoImage(file="imgFolder/icon.png"))
window.minsize(width=800, height=500)
frame_up = tk.Frame(window, border=1,bg="blue")
frame_up.pack(fill="x", side="top")

#Importing Images
folder_icon = tk.PhotoImage(file="imgFolder/icon_folder.png")
file_icon = tk.PhotoImage(file="imgFolder/icon_file.png")
home_icon = tk.PhotoImage(file="imgFolder/icon_home.png")
up_icon = tk.PhotoImage(file="imgFolder/icon_up.png")
frame_b = tk.Frame(frame_up, border=2, relief="groove", bg="blue")
frame_b.pack(side="left")

#Buttons
tk.Button(frame_b, image=up_icon, width=25, height=32, relief="flat", bg="pink", fg="black",command=move_up).grid(column=0, row=1)
tk.Button(frame_b, image=home_icon, width=25, height=32, relief="flat", bg="pink", fg="black",command=lambda:update_files_folders(parent_path)).grid(column=1, row=1)
entry = tk.Entry(frame_up, font=("Arial", 12), justify="left", highlightcolor="white", relief="groove", border=2)
entry.pack(side="right",fill="both", expand=1)
label = tk.Label(window, font=("Arial", 12), anchor="w", bg="#856ff8", fg="black", border=2)
label.pack(side="bottom",fill="both")

#Tree View
treeFrame = tk.Frame(window, border=1, relief="flat", bg="blue")
treeFrame.pack(expand=1, fill="both")
tree =ttk.Treeview(treeFrame, columns=("#1"), selectmode="extended", show="tree headings")
tree.heading("#0", text="   Name", anchor="w", command=sort_name_reverse)
tree.heading("#1", text="Size", anchor="w", command=sort_size_reverse)
tree.column("#0", anchor="w")
tree.column("#1", anchor="e", stretch=False, width=120)
tree.pack(side="left", expand=1, fill="both")
treeStyle=ttk.Style()
treeStyle.theme_use("clam")
treeStyle.configure("Treeview.Heading",background="#856ff8")
scrollbar = ttk.Scrollbar(treeFrame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right",fill="y")

#Right Click Menu
right_menu = tk.Menu(treeFrame, tearoff=0, font=("Arial", 12))
right_menu.add_command(label="Open", command=click, state="disabled")
right_menu.add_command(label="Copy", command=copy, state="disabled")
right_menu.add_command(label="Rename", command=rename, state="disabled")
right_menu.add_command(label="Delete in trash", command=delete, state="disabled")
right_menu.add_separator()
right_menu.add_command(label="Paste", command=paste, state="disabled")
right_menu.add_separator()
right_menu.bind("<FocusOut>", lambda event:right_menu.unpost())

drive_buttons()
update_files_folders(parent_path)
tree.focus_set()

#Linking Keyboard/Mouse buttons to functions
tree.bind("<<TreeviewSelect>>", lambda event:select())
tree.bind("<Double-Button-1>", lambda event:click())
tree.bind("<BackSpace>", lambda event:move_up())
tree.bind("<Button-3>", open_right_menu)
tree.bind("<Button-1>", lambda event:remove_selection())
tree.bind("<Return>", lambda event:click())
tree.bind("<Control-c>", lambda event: copy())
tree.bind("<Control-v>", lambda event:paste())
tree.bind("<Delete>", lambda event:delete())
entry.bind("<Return>", lambda event:update_files_folders(entry.get()))

window.mainloop()

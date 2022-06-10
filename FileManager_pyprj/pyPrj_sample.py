import os
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk ,Image
from tkinter.messagebox import showinfo
from datetime import datetime as dt

disp= Tk()  #creating an object of tkinter frame
disp.title('This Pc:')
disp.geometry("1450x1000")
#Listing out drives
def list_drives():
    driveList= [chr(x) + ':' for x in range(65, 90) if os.path.exists(chr(x) + ':')]
    drive=Tk()
    drive.title('Drives:')
    drive.geometry("500x500")
    driveButton={}
    for x in driveList:
        driveButton[x]=Button(drive,text=x)
        driveButton[x].pack()
    drive.mainloop()


"""def select_file(myFile):
    selected_fileNumber=myFile.curselection()
    selected_file=myFile.get(selected_fileNumber)
    options="1.Open File\n2.Rename File\n3.Delete File\n4.Properties of file\n";
    showinfo(fileName=selected_file,message=options)"""
    
#Listing out desktop
def list_desktop():
    desktopList=[]
    desktopList=os.listdir("C:/Users/dell/Desktop/")
    """while i<len(desktopList):
        os.path.splitext(desktopList[i])[0]
        i+=1"""
    desktop=Tk()
    desktop.title('Drives:')
    desktop.geometry("500x500")
    scroll_bar=Scrollbar(desktop)
    scroll_bar.pack(side=RIGHT,fill=Y)
    myDesktop=Listbox(desktop,yscrollcommand=scroll_bar.set,selectmode="single")
    desktopButton={}
    for x in desktopList:
        #desktopButton[x]=Button(desktop,text=x)
        #desktopButton[x].pack()
        myDesktop.insert(END,x)
    myDesktop.pack(side=LEFT,fill=BOTH,expand=True)
    scroll_bar.config(command=myDesktop.yview)
    desktop.mainloop()
    
    
#Listing out downloads
def list_downloads():
    downloadList=[]
    downloadButton={}
    downloadList=os.listdir("C:/Users/dell/Downloads/")
    download=Tk()
    download.title('Downloads:')
    download.geometry("500x500")
    scroll_bar=Scrollbar(download)
    scroll_bar.pack(side=RIGHT,fill=Y)
    myDownloads=Listbox(download,yscrollcommand=scroll_bar.set,selectmode="single")
    downloadButton={}
    for x in downloadList:
        #x=x.strip('.')
        myDownloads.insert(END,x)
    myDownloads.pack(side=LEFT,fill=BOTH,expand=True)
    scroll_bar.config(command=myDownloads.yview)
    #myDownloads.bind('<<ListboxSelect>>',select_file(myDownloads))
    download.mainloop()
    
    
img1=ImageTk.PhotoImage(Image.open ("C:/Users/dell/Desktop/Project_fileManager/driveImg.jpg"))
lab1=Label(image=img1).grid(row=1,column=0)
img2=ImageTk.PhotoImage(Image.open ("C:/Users/dell/Desktop/Project_fileManager/fileImg.png"))
lab2=Label(image=img2).grid(row=1,column=50)
img3=ImageTk.PhotoImage(Image.open ("C:/Users/dell/Desktop/Project_fileManager/download.jpg"))
lab3=Label(image=img3).grid(row=1,column=100)
button1=Button(disp,text='Drives',command=list_drives).grid(row=2,column=0)
button2=Button(disp,text='Desktop',command=list_desktop).grid(row=2,column=50)
button3=Button(disp,text='Downloads',command=list_downloads).grid(row=2,column=100)
current=dt.now()
dateButton=Button(disp,text=dt.today(),command=disp.quit)
dateButton.place(relx=1.0, rely=1.0, anchor="se")
timeButton=Button(disp,text=current.strftime("%H:%M"),command=disp.quit)
timeButton.place(relx=2.0, rely=1.0, anchor="se")

disp.mainloop()







import os
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk ,Image

disp= Tk()  #creating an object of tkinter frame
disp.title('This Pc:')

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

#Listing out downloads
def list_downloads():
    downloadList=[]
    downloadButton={}
    downloadList=os.listdir("C:/Users/dell/Downloads/")
    download=Tk()
    download.title('Downloads:')
    download.geometry("1000x1000")
    scroll_bar=Scrollbar(download)
    scroll_bar.pack(side=RIGHT,fill=Y)
    myList=Listbox(download,yscrollcommand=scroll_bar.set)
    downloadButton={}
    for x in downloadList:
        #myList.insert(downloadButton[x])
        #downloadButton[x]=Button(download,text=x)
        myList.insert(END,x)
        #downloadButton[x].pack()
    myList.pack(side=LEFT,fill=BOTH)
    scroll_bar.config(command=myList.yview)
    download.mainloop()
    
    
#img1=ImageTk.PhotoImage(Image.open ("D:/fileImg.png"))
img1=ImageTk.PhotoImage(Image.open ("/Users/srinidhicr/Downloads/fileImg.png"))
lab1=Label(image=img1).grid(row=1,column=0)
#img2=ImageTk.PhotoImage(Image.open ("D:/driveImg.jpg"))
img2=ImageTk.PhotoImage(Image.open ("/Users/srinidhicr/Downloads/driveImg.jpg"))
lab2=Label(image=img2).grid(row=1,column=5)
#img3=ImageTk.PhotoImage(Image.open ("D:/download.jpg"))
img3=ImageTk.PhotoImage(Image.open ("/Users/srinidhicr/Downloads/download.jpg"))
lab3=Label(image=img3).grid(row=1,column=10)
#img = ImageTk.PhotoImage(Image.open("D:/driveImg.jpg"))
img = ImageTk.PhotoImage(Image.open("/Users/srinidhicr/Downloads/driveImg.jpg"))
button1=Button(disp,text='Drives',command=list_drives,image=img).grid(row=2,column=0)
button2=Button(disp,text='Desktop',command=disp.quit).grid(row=2,column=5)
button3=Button(disp,text='Downloads',command=list_downloads).grid(row=2,column=10)


disp.mainloop()







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

def list_desktop():
    desktoplist = []
    desktopButton = {}
    desktoplist = os.listdir("/Users/srinidhicr/Desktop/")
    desktop = Tk()
    desktop.title('Desktop:')
    desktop.geometry("1000x1000")
    scroll_bar=Scrollbar(desktop)
    scroll_bar.pack(side=RIGHT,fill=Y)
    myList=Listbox(desktop,yscrollcommand=scroll_bar.set)
    downloadButton={}
    for x in desktoplist:
        myList.insert(END,x)
    myList.pack(side=LEFT,fill=BOTH, expand = 5)
    scroll_bar.config(command=myList.yview)
    desktop.mainloop()

def list_documents():
    documentList = []
    documentList = os.listdir("/Users/srinidhicr/Documents/")
    document = Tk()
    document.title('Documents:')
    document.geometry("1000x1000")
    scroll_bar=Scrollbar(document)
    scroll_bar.pack(side=RIGHT,fill=Y)
    myList=Listbox(document,yscrollcommand=scroll_bar.set)
    downloadButton={}
    for x in documentList:
        #myList.insert(downloadButton[x])
        #downloadButton[x]=Button(download,text=x)
        myList.insert(END,x)
        #downloadButton[x].pack()
    myList.pack(side=LEFT,fill=BOTH, expand = 5)
    scroll_bar.config(command=myList.yview)
    document.mainloop()

#Listing out downloads
def list_downloads():
    downloadList=[]
    downloadButton={}
    downloadList=os.listdir("/Users/srinidhicr/Downloads/")
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
    myList.pack(side=LEFT,fill=BOTH, expand=5)
    scroll_bar.config(command=myList.yview)
    download.mainloop()

#downloads
Label(disp, text = 'Downloads', font =('Verdana', 15)).grid(row=30, column = 0)
photo = PhotoImage(file = r"/Users/srinidhicr/Downloads/folder.png")
photoimage = photo.subsample(3, 3)
#desktop
Label(disp, text = 'Desktop', font =('Verdana', 15)).grid(row=30, column = 5)
photo = PhotoImage(file = r"/Users/srinidhicr/Downloads/folder.png")
#documents
Label(disp, text = 'Documents', font =('Verdana', 15)).grid(row=30, column = 10)
photo2 = PhotoImage(file = r"/Users/srinidhicr/Downloads/folder.png")
#drives
Label(disp, text = 'Drives', font =('Verdana', 15)).grid(row=30, column = 15)
photo2 = PhotoImage(file = r"/Users/srinidhicr/Downloads/drive.png")
photo2image = photo2.subsample(3, 3)
#displaying the buttons
Button(disp, image = photoimage, command=list_downloads).grid(row=20, column = 0)
Button(disp, image = photoimage, command=list_desktop).grid(row=20, column = 5) 
Button(disp, image = photoimage, command=list_documents).grid(row=20, column = 10) 
Button(disp, image = photo2image, command=list_drives).grid(row=20, column = 15)

#img1=ImageTk.PhotoImage(Image.open ("D:/fileImg.png"))
#img1=ImageTk.PhotoImage(Image.open ("/Users/srinidhicr/Downloads/fileImg.png"))
#lab1=Label(image=img1).grid(row=1,column=0)
#img2=ImageTk.PhotoImage(Image.open ("D:/driveImg.jpg"))
#img2=ImageTk.PhotoImage(Image.open ("/Users/srinidhicr/Downloads/driveImg.jpg"))
#lab2=Label(image=img2).grid(row=1,column=5)
#img3=ImageTk.PhotoImage(Image.open ("D:/download.jpg"))
#img3=ImageTk.PhotoImage(Image.open ("/Users/srinidhicr/Downloads/folder.png")) 
#lab3=Label(image=img3).grid(row=1,column=20)
#img = ImageTk.PhotoImage(Image.open("D:/driveImg.jpg"))
#img = ImageTk.PhotoImage(Image.open("/Users/srinidhicr/Downloads/driveImg.jpg"))
#button1=Button(disp,text='Drives',command=list_drives,image=img2).grid(row=2,column=0)
#button2=Button(disp,text='Desktop',command=disp.quit).grid(row=2,column=5)
#button3=Button(disp,text='Downloads', image= img3, command=list_downloads).grid(row=2,column=10)


disp.mainloop()







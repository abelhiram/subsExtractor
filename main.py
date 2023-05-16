from tkinter import *
from tkinter import ttk,IntVar,messagebox
import tkinter.filedialog as fd
import shutil
from controller.subtitlesController import subtitlesController
import sv_ttk
import os

subs = subtitlesController()



def openFile():
    filez = fd.askopenfilenames(parent=root, title='Choose a file')
    return filez

def copyFile():
    src_path = openFile()
    messageModal(src_path)
    comboSerie.config(values=subs.folderNames("subs/"))
    
def fillSeasonListbox(event):
    serie = comboSerie.get()
    filenames = subs.folderNames(f"subs/{serie}")
    listBoxSeason.delete(0,END)
    for file in filenames:
        listBoxSeason.insert(END,file)


def insertFilesInListbox(event):
    index =listBoxSeason.curselection()
    season =listBoxSeason.get(index[0])
    filenames = subs.getAllFiles(f"subs/{comboSerie.get()}/{season}")
    listBoxEpisodes.delete(0,END)
    for file in filenames:
        listBoxEpisodes.insert(END,file.replace("//","/")) 
    

def getSelectionListbox():
    episodeSelected =[listBoxEpisodes.get(i) for i in listBoxEpisodes.curselection()]
    return episodeSelected

def getSelectionListboxSeason():
    seasonSelected =[os.path.abspath(f'./subs/{listBoxSeason.get(i)}') for i in listBoxSeason.curselection()]
    return seasonSelected

def toDataFrame():
    checked =chk_value.get()
    file=None
    directory="subs"
    if checked:
        if comboSerie.get() !='':
            if listBoxSeason.curselection():
                if listBoxEpisodes.curselection():
                    file = getSelectionListbox()
                else:
                    season = listBoxSeason.get(listBoxSeason.curselection()[0])
                    file= subs.getAllFiles(f"subs/{comboSerie.get()}/{season}")
            else:
                file = subs.getAllFiles(f"subs/{comboSerie.get()}")
    else:
        if comboSerie.get() !='':
            directory = "subs/"+comboSerie.get()

    #print (file,directory)
    subs.ToDataFrame(folder = directory if file == None else None,file=file)
    

root = Tk()
root.minsize(600,450)
#frames
main_frame = Frame(width=350)
listBox_frame= Frame(main_frame)


def messageModal(src_path):
    def save_file():
        
        if checkIfNewOrExistingFolder.get():
            os.makedirs(os.path.abspath(f'./subs/{entryNewFolder.get()}/{entryNewSeason.get()}'))
            path = os.path.abspath(f'./subs/{entryNewFolder.get()}/{entryNewSeason.get()}')
        else:
            if checkIfNewSeason.get():
                os.makedirs(os.path.abspath(f'./subs/{comboFolder.get()}/{entrySeason.get()}'))
                path = os.path.abspath(f'./subs/{comboFolder.get()}/{entrySeason.get()}')
            else:
                path = os.path.abspath(f'./subs/{comboFolder.get()}/{comboSeason.get()}')

        for file in src_path:
            shutil.copy(file, path)

        messagebox.showinfo(title="Success",message=f"File Saved correctly in {path}")
        

    def checkIfSelected():
        checked =checkIfNewOrExistingFolder.get()
        nsChecked = checkIfNewSeason.get()
        if checked:
            comboFolder.config(state='disabled')
            comboSeason.config(state='disabled')
            entryNewFolder.config(state='normal')
            entryNewSeason.config(state='normal')
            entrySeason.config(state= 'disabled')
            chkNewSeason.config(state="disabled")
        else:
            comboFolder.config(state='normal')
            comboSeason.config(state='normal')
            entryNewFolder.config(state= 'disabled')
            entryNewSeason.config(state= 'disabled')
            chkNewSeason.config(state="normal")
            if nsChecked:
                entrySeason.config(state= 'normal')
                comboSeason.config(state='disabled')
            else:
                entrySeason.config(state= 'disabled')
                comboSeason.config(state='normal')
        

    global popup
    popup = Toplevel(root)
    popup.title("Chose folder to save subtitles or add a new one")
    popup.geometry("450x300")
    existingFolder = Frame(popup,pady=10)
    newFolder = Frame(popup,pady=10)
    lblCombo = ttk.Label(existingFolder,text="Chose folder to save",width=20)
    lblFolder = ttk.Label(existingFolder,text="Select folder",padding=10)
    lblSeason = ttk.Label(existingFolder,text="Select season",padding=10)
    comboFolder = ttk.Combobox(existingFolder,values=subs.folderNames("subs/"),width=40)
    comboFolder.bind("<<ComboboxSelected>>",lambda x: comboSeason.config(values=subs.folderNames(f"subs/{comboFolder.get()}")))
    comboSeason =ttk.Combobox(existingFolder,width=40)

    checkIfNewSeason = IntVar()
    chkNewSeason = ttk.Checkbutton(existingFolder, text="New season",variable=checkIfNewSeason,command=checkIfSelected)
    
    entrySeason = ttk.Entry(existingFolder,width=45,state='disabled')

    checkIfNewOrExistingFolder = IntVar()
    chkNewFolder = ttk.Checkbutton(newFolder, text="New serie",variable=checkIfNewOrExistingFolder,command=checkIfSelected)
    
    #button = ttk.Button(newFolder,Text="New Folder",command=checkIfSelected)
    entryNewFolder = ttk.Entry(newFolder,width=21,state='disabled')
    entryNewSeason = ttk.Entry(newFolder,width=21,state='disabled')
    lblNewFolder = ttk.Label(newFolder,text="Folder Name")
    lblNewSeason = ttk.Label(newFolder,text="Season Name")

    btnSaveData = ttk.Button(popup,text="Save Data",command=save_file,padding=10)

    lblCombo.grid(row=0,column=1)
    lblFolder.grid(row=1,column=0)
    lblSeason.grid(row=2,column=0)
    comboFolder.grid(row=1,column=1,columnspan=2)
    comboSeason.grid(row=2,column=1,columnspan=2)
    chkNewSeason.grid(row=3,column=0)
    entrySeason.grid(row=3,column=1,columnspan=2)
    lblNewFolder.grid(row=0,column=1)
    lblNewSeason.grid(row=0,column=2)
    #button.grid(row=1,column=0)
    chkNewFolder.grid(row=1,column=0)
    entryNewFolder.grid(row=1,column=1)
    entryNewSeason.grid(row=1,column=2)
    existingFolder.pack()
    newFolder.pack()
    btnSaveData.pack()
    popup.mainloop()


lblTitle = ttk.Label(main_frame,text="Word Extracter from subtitles")
comboSerie = ttk.Combobox(main_frame,values=subs.folderNames("subs/"))
comboSerie.bind("<<ComboboxSelected>>",fillSeasonListbox)
chk_value = IntVar()
chkInsertSelection = ttk.Checkbutton(main_frame, text="Insert selection?",variable=chk_value)
btnOpenFile = ttk.Button(main_frame,text="Open File",command=copyFile)

listBoxSeason = Listbox(listBox_frame,selectmode="extended",width=30,exportselection=False,)
listBoxSeason.bind('<<ListboxSelect>>',insertFilesInListbox)
listBoxEpisodes = Listbox(listBox_frame,selectmode="extended",width=50,exportselection=False)

btnToDataFrame = ttk.Button(main_frame,text="To DataFrame", command=toDataFrame)


lblTitle.pack()
comboSerie.pack()
chkInsertSelection.pack()
listBox_frame.pack()
listBoxSeason.grid(row=1,column=1)
listBoxEpisodes.grid(row=1,column=2)
btnOpenFile.pack()
btnToDataFrame.pack()
main_frame.pack()

sv_ttk.use_light_theme()


root.mainloop()


        




#https://www.geeksforgeeks.org/file-explorer-in-python-using-tkinter/
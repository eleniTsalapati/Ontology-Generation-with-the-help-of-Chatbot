from time import sleep
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

class UI:
    def __init__(self):
        self.txt=""
        self.msg=None
        self.win=None
        self.butTrue=None
        self.butFalse=None
        self.butPack=False
        self.entry=None
        self.entryPack=False
        self.frame1=None
        self.frame2=None
        self.flag=False
        self.answer=""
        self.rememberTxt=""

        self.butFile=None
        self.folderPath=None
        self.flagFile=True
        self.filePack=False

    def rememberOneTime(self,txt):
        self.rememberTxt+=txt

    def changeMessage(self,txt):
        self.txt=self.rememberTxt
        self.txt+=txt
        if self.msg!=None :
            self.msg.configure(text=self.txt) 

        self.rememberTxt=""

    def browse_button(self):
        # Allow user to select a directory and store it in global var
        # called folder_path
        filename = filedialog.askopenfilename(filetypes=(("Owl","*.owl"),))
        self.answer="file://"+filename
        self.entry.insert(END,self.answer)
        self.butFile.config(state="disable")
        self.entry.config(state="readonly")
        self.flag=False

    def gotText(self,event):
        self.answer=self.entry.get()
        print(self.answer)
        self.entry.config(state= "readonly")
        self.flag=False
        
    def gotTrue(self):
        self.answer="Yes"
        print(self.answer)
        self.butTrue.config(state= "disabled")
        self.butFalse.config(state= "disabled")
        self.flag=False
    
    def gotFalse(self):
        self.answer="No"
        print(self.answer)
        self.butTrue.config(state= "disabled")
        self.butFalse.config(state= "disabled")
        self.flag=False
    
    def create(self):
        self.win = Tk() 
        self.win.geometry("500x500") 

        self.frame1 = LabelFrame(self.win,text="ChatBot Messages:")
        self.frame1.pack()
        self.msg = Message(self.frame1, text = self.txt,anchor=CENTER,width=450) 
        self.msg.pack() 

        self.frame2 = LabelFrame(self.win,text="Your Answers:")
        self.frame2.pack()
        self.entry=Entry(self.frame2,width=500)

        self.entry.config(state= "readonly")
        self.entry.bind("<Return>", self.gotText)

        self.butTrue=Button(self.frame2,text="Yes",bg='green',fg="white",command=self.gotTrue)
        self.butFalse=Button(self.frame2,text="No",bg='red',fg="white",command=self.gotFalse)        
        self.butFile=Button(self.frame2,text="Find file",command=self.browse_button)

    def hearTrueOrFalse(self):
        if self.entryPack==True:
            self.entry.pack_forget()
            self.entryPack=False
        if self.filePack==True:
            self.butFile.pack_forget()
            self.filePack=False
        self.butPack=True
        self.flag=True
        self.butTrue.pack(side=LEFT,expand=True,fill=BOTH)
        self.butFalse.pack(side=RIGHT,expand=True,fill=BOTH)
        self.butTrue.config(state= "normal")
        self.butFalse.config(state= "normal")
        while self.flag:
            self.win.update_idletasks()
            self.win.update()
        return self.answer

    def hear(self):
        if self.butPack==True:
            self.butFalse.pack_forget()
            self.butTrue.pack_forget()
            self.butPack=False
        if self.filePack==True:
            self.butFile.pack_forget()
            self.filePack=False

        self.flag=True
        self.entryPack=True
        self.entry.pack() 
        self.entry.config(state= "normal")
        self.entry.delete(0,END)
        if self.flagFile==True:
            self.butFile.pack()
            self.filePack=True
            self.flagFile=False
        while self.flag:
            self.win.update_idletasks()
            self.win.update()
        return self.answer

    def close(self):
        messagebox.showinfo("Clossing...",  "I would like to thank you for using this ChatBot to develop your ontology!")
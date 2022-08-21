from tkinter import *
from turtle import right

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

    def rememberOneTime(self,txt):
        self.rememberTxt+=txt

    def changeMessage(self,txt):
        self.txt=self.rememberTxt
        self.txt+=txt
        if self.msg!=None :
            self.msg.configure(text=self.txt) 

        self.rememberTxt=""

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
        self.msg = Message(self.frame1, text = self.txt,anchor=CENTER,width=500) 
        self.msg.pack() 

        self.frame2 = LabelFrame(self.win,text="Your Answers:")
        self.frame2.pack()
        self.entry=Entry(self.frame2,width=500)

        self.entry.config(state= "readonly")
        self.entry.bind("<Return>", self.gotText)

        self.butTrue=Button(self.frame2,text="Yes",bg='green',fg="white",command=self.gotTrue)
        self.butFalse=Button(self.frame2,text="No",bg='red',fg="white",command=self.gotFalse)

    def hearTrueOrFalse(self):
        if self.entryPack==True:
            self.entry.pack_forget()
            self.entryPack=False

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

        self.flag=True
        self.entryPack=True
        self.entry.pack() 
        self.entry.config(state= "normal")
        self.entry.delete(0,END)
        while self.flag:
            self.win.update_idletasks()
            self.win.update()
        return self.answer
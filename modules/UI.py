from cgitb import text
from pickle import FRAME
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from turtle import left, right


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
        self.frame3=None
        self.frame4=None
        self.frame5=None
        self.flag=False
        self.answer=""
        self.rememberTxt=""

        self.butFile=None
        self.folderPath=None
        self.flagFile=True
        self.filePack=False

        self.subjectTable=None 
        self.relationsTable=None
        self.flagTable=True 
        self.rememberTable=False

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
        self.entry.config(state= "readonly")
        self.flag=False
        
    def gotTrue(self):
        self.answer="Yes"
        self.butTrue.config(state= "disabled")
        self.butFalse.config(state= "disabled")
        self.flag=False
    
    def gotFalse(self):
        self.answer="No"
        self.butTrue.config(state= "disabled")
        self.butFalse.config(state= "disabled")
        self.flag=False
    
    def create(self):
        self.win = Tk() 
        self.win.geometry("1000x500") 

        self.frame1 = LabelFrame(self.win,text="ChatBot Messages:")
        self.frame1.pack()
        self.msg = Message(self.frame1, text = self.txt,anchor=CENTER,width=450) 
        self.msg.pack() 

        self.frame2 = LabelFrame(self.win,text="Your Answer:")
        self.frame2.pack()
        self.entry=Entry(self.frame2,width=500)

        self.entry.config(state= "readonly")
        self.entry.bind("<Return>", self.gotText)

        self.butTrue=Button(self.frame2,text="Yes",bg='green',fg="white",command=self.gotTrue)
        self.butFalse=Button(self.frame2,text="No",bg='red',fg="white",command=self.gotFalse)        
        self.butFile=Button(self.frame2,text="Find file",command=self.browse_button)

        self.frame3= LabelFrame(self.win,text="Your Data")
        self.frame3.pack()

        self.frame6= Frame(self.frame3)
        self.frame6.pack()
        # One TABLE
        self.frame4=Frame(self.frame6)
        self.frame4.pack(side=LEFT)
        self.subjectTable= ttk.Treeview(self.frame4)


        # Scrollbar
        self.scroll1= Scrollbar(self.frame4,command = self.subjectTable.yview)
        self.scroll1.pack(side=RIGHT,fill=Y)
        self.subjectTable.configure(yscrollcommand = self.scroll1.set)
        
        # Definition of Columns
        self.subjectTable['columns']=("id","name","parent")
        self.subjectTable.column("#0",width=0,stretch=NO)
        self.subjectTable.column("id",anchor=CENTER,width=80,stretch=YES,)
        self.subjectTable.column("name",anchor=CENTER,width=120,stretch=YES)
        self.subjectTable.column("parent",anchor=CENTER,width=120,stretch=YES)

        # Definition of Headings
        self.subjectTable.heading("#0",text="",anchor=CENTER)
        self.subjectTable.heading("id",text="ID",anchor=CENTER)
        self.subjectTable.heading("name",text="Name",anchor=CENTER)
        self.subjectTable.heading("parent",text="Parent",anchor=CENTER)

        self.subjectTable.tag_configure('used', background='white')
        self.subjectTable.tag_configure('notUsed', background='orange')

        self.subjectTable.pack()

        # THE OTHER TABLE
        #  -------------

        self.frame5=Frame(self.frame6)
        self.frame5.pack(side=RIGHT)
        self.relationsTable= ttk.Treeview(self.frame5)

        # Scrollbar
        self.scroll2= Scrollbar(self.frame5,command = self.relationsTable.yview)
        self.scroll2.pack(side=RIGHT,fill=Y)
        self.relationsTable.configure(yscrollcommand = self.scroll2.set)

        # Definition of Columns
        self.relationsTable['columns']=("id","object1","relation","object2")
        self.relationsTable.column("#0",width=0,stretch=NO)
        self.relationsTable.column("id",anchor=CENTER,width=80)
        self.relationsTable.column("object1",anchor=CENTER,width=80)
        self.relationsTable.column("relation",anchor=CENTER,width=80)
        self.relationsTable.column("object2",anchor=CENTER,width=80)

        # Definition of Headings
        self.relationsTable.heading("#0",text="",anchor=CENTER)
        self.relationsTable.heading("id",text="ID",anchor=CENTER)
        self.relationsTable.heading("object1",text="Object 1",anchor=CENTER)
        self.relationsTable.heading("relation",text="Relation",anchor=CENTER)
        self.relationsTable.heading("object2",text="Object 2",anchor=CENTER)

        self.relationsTable.pack()    

        txt="The red rows have not yet been INSERTED\n"
        txt+="The orange rows have not yet been USED to make a relation with another object"
        self.msg2 = Message(self.frame3, text = txt,anchor=CENTER,width=450) 
        self.msg2.pack()

    def makeTables(self,data):
        # Add Data in subjectTable
        theList=list(self.subjectTable.get_children())
        last=len(theList)
        for key in data[0].keys():
            i=0
            for i in range(len(theList)):
                item=self.subjectTable.item(i)
                
                # change color
                if item["values"][1] == key:
                    if data[0][key][3]==1:
                        self.subjectTable.item(i,tags="used")
                    else:
                        self.subjectTable.item(i,tags="notUsed")
                    break
            if i == len(theList):   
                parent=""
                for item in  data[0][key][2]:
                    parent+=item+" "
                # insert them inside
                self.subjectTable.insert(parent="",index="end",iid=last,text="",
                values=(last,data[0][key][1],parent),tags="notUsed")
                if data[0][key][3]==1:
                    self.subjectTable.item(i,tags="used")
                last+=1


        # Add Data in relation
        theList=self.relationsTable.get_children()
        if  theList== ():
            start=0
        else:
            # find the last id number
            start=int(theList[-1])+1
        # for the keys from the start to the end
        keys=list(data[1].keys())
        last=len(keys)
        for i in range(start,len(keys)):
            for obj1 in data[1][keys[i]][1]:
                # insert them inside
                self.relationsTable.insert(parent="",index="end",iid=last,text="",
                values=(i+1,obj1,data[1][keys[i]][2],data[1][keys[i]][3]))
                last+=1
        self.rememberTable=True
        self.frame3.pack()

    def rememberTableOnce(self):
        self.rememberTable=True
        self.frame3.pack()

    def hearTrueOrFalse(self):
        if self.flagTable==True:
            self.frame3.pack_forget()
            self.flagTable=False
        
        if self.rememberTable==True:
            self.frame3.pack()
            self.rememberTable=False
            self.flagTable=True

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
        if self.flagTable==True:
            self.frame3.pack_forget()
            self.flagTable=False
        
        if self.rememberTable==True:
            self.frame3.pack()
            self.rememberTable=False
            self.flagTable=True

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

    
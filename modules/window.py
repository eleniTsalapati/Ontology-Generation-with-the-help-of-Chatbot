from owlready2 import *
from modules.searchOntology import *
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk,GLib
import modules.slowTextView as stv
from modules.mainFunction import *
import modules.creationFunctions as creationFunctions
from modules.dialogOptions import CheckDialog,SaveDialog,TextDialog
import modules.chatbotTalks as talk
import modules.ontologyManager as manager
from sys import platform
class C4OWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        self.whichTask=""
        self.secondCompetencyQuestion=[]
        
        super().__init__(*args, **kwargs)
        self.connect("delete-event", self.quitFunction)

        # make the application be at the maximum size of the screen
        self.file_name = "Untitled"
        # window properties
        #
        self.set_border_width(10)
        self.set_default_size(1000, 600)

        # headerbar
        #
        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.props.title = self.file_name+" - Ontology Genertion with Chatbot"
        self.set_titlebar(self.hb)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.hb.pack_start(box)

        file_button = Gtk.MenuButton.new()
        box.add(file_button)

        file_button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        file_button.add(file_button_box)

        file_label = Gtk.Label("File")
        down_arrow_image = Gtk.Arrow(arrow_type=Gtk.ArrowType.DOWN, shadow_type=Gtk.ShadowType.NONE)
        file_button_box.add(file_label)
        file_button_box.add(down_arrow_image)

        with open('modules/file_menu.xml', 'r') as f:
            menu_xml = f.read()
            builder = Gtk.Builder.new_from_string(menu_xml, -1)
            menu = builder.get_object("file-menu")
            file_button.set_menu_model(menu)

        # make a vertical box that is in all the space of the window
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # make a textview
        self.textview = stv.SlowTextView()
        text="ChatBot:\n\t"+"Greetings new user! This is the the ChatBot for Ontologies.\n\t"
        text+="To continue select a folder to create a new ontology or select an existing ontology to edit."
        self.textview.add_text(text,0)


        # make a scrollable textview
        scrollingTextView=Gtk.ScrolledWindow()
        scrollingTextView.add(self.textview)
        # add the textview+scrolling to the vertical box
        vbox.pack_start(scrollingTextView, True, True, 2)


        menu_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        consistency=Gtk.Button("Consistency")
        consistency.connect("clicked",self.Consistency)
        menu_box.pack_start(consistency, False, False, 2)

        broaden=Gtk.Button("Broaden")
        broaden.connect("clicked",self.MenuFunction,"Broaden")
        menu_box.pack_start(broaden, False, False, 2)

        narrow=Gtk.Button("Narrow")
        narrow .connect("clicked",self.MenuFunction,"Narrow")
        menu_box.pack_start(narrow, False, False, 2)

        trash=Gtk.Button()
        # add the image bin.png to the button and resize it to the size of the button
        theImage=None
        if platform == "win32":
            theImage='modules/trash.png'
        else:
            theImage='modules/trash.png'
        image = Gtk.Image.new_from_file(theImage)
        image.set_pixel_size(20)
        trash.add(image)
        trash.connect("clicked",self.MenuFunction,"Destroy Entity")
        menu_box.pack_start(trash,False, False, 2)

        # add a text entry
        self.entryMenu = Gtk.Entry()
        menu_box.pack_start(self.entryMenu,True, True, 5)

        competencyQuestion=Gtk.Button("Competency Question")
        competencyQuestion.connect("clicked",self.MenuFunction,"Sentence")
        menu_box.pack_start(competencyQuestion,False, False, 2)

        # add a button to the input field
        buttonTrue=Gtk.Button("True")
        buttonTrue.get_style_context().add_class("suggested-action")
        buttonFalse=Gtk.Button("False")
        buttonFalse.get_style_context().add_class("destructive-action")
        buttonTrue.connect("clicked", lambda x: self.textview.add_text("User:\n\tTrue"))
        buttonFalse.connect("clicked", lambda x: self.textview.add_text("User:\n\tFalse"))
        buttonTrue.colour="green"
        buttonFalse.colour="red"
        buttonsTrue_False=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        buttonsTrue_False.pack_start(buttonTrue,False, False, 2)
        buttonsTrue_False.pack_start(buttonFalse,False, False, 2)
        buttonsTrue_False.props.halign=Gtk.Align.CENTER

         # add a button to the input field
        buttonSearch=Gtk.Button("Search Online")
        buttonGiveDefinition=Gtk.Button("Give Definition")
        buttonNoDefinition=Gtk.Button("Keep Without Definition")
        buttonNoKeep=Gtk.Button("Do Not Keep Term")
        
        # set up the connections
        buttonSearch.connect("clicked",self.DefinitionMenu,"Search Online")
        buttonGiveDefinition.connect("clicked",self.DefinitionMenu,"Give Definition")
        buttonNoDefinition.connect("clicked",self.DefinitionMenu,"Keep Without Definition")
        buttonNoKeep.connect("clicked",self.DefinitionMenu,"Do Not Keep Term")

        # put them in a box
        definitionButtons=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        definitionButtons.pack_start(buttonSearch,False, False, 2)
        definitionButtons.pack_start(buttonGiveDefinition,False, False, 2)
        definitionButtons.pack_start(buttonNoDefinition,False, False, 2)
        definitionButtons.pack_start(buttonNoKeep,False, False, 2)
        definitionButtons.props.halign=Gtk.Align.CENTER

        self.entryNouns = Gtk.Entry()
        sendButton= Gtk.Button("Send")
        sendButton.connect("clicked",self.getAnswerNouns)
        getNouns=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        getNouns.pack_start(self.entryNouns,False,False,2)
        getNouns.pack_start(sendButton,False,False,2)
        getNouns.props.halign=Gtk.Align.CENTER

        self.input_field= Gtk.Stack()
        self.input_field.set_homogeneous(False)
        
        self.input_field.add_named(menu_box,"Menu")
        menu_box.set_visible(True)
        self.input_field.add_named(definitionButtons,"Definitions")
        definitionButtons.set_visible(True)
        self.input_field.add_named(getNouns,"getNouns")
        getNouns.set_visible(True)
        self.input_field.set_visible_child_name("Menu")

        self.entryMenu.connect("activate",self.getAnswerMenu)
        self.entryNouns.connect("activate",self.getAnswerNouns)
        # self.entry.connect("changed", self.EntryChanged)
        
        
        # TABLES
        paned=Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        paned.set_wide_handle(True)
        paned.set_position(500)
        self.storeTerm = Gtk.TreeStore(str)

        treeview = Gtk.TreeView(self.storeTerm)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Term", renderer, text=0)
        treeview.append_column(column)
        
        # # when a value is clicked in the treeview, add the title to the entry with the previous text
        # # and make the broaden button and narrow button active         
        treeview.connect("row-activated", self.TableActivated)
        # # if the entry is empty, make the broaden button and narrow button inactive

        # add a scrollable treeview
        scrollingTreeView1=Gtk.ScrolledWindow()
        scrollingTreeView1.add(treeview)

        paned.add1(scrollingTreeView1)

        self.storeRelationship = Gtk.TreeStore(str, str, str)
        treeview = Gtk.TreeView(self.storeRelationship)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Term1", renderer, text=0)
        treeview.append_column(column)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Connection", renderer, text=1)
        treeview.append_column(column)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Term2", renderer, text=2)
        treeview.append_column(column)
        # # when a value is clicked in the treeview, add the title to the entry with the previous text
        # # and make the broaden button and narrow button active         
        treeview.connect("row-activated", self.TableActivated2)

        # add a scrollable treeview
        scrollingTreeView2=Gtk.ScrolledWindow()
        scrollingTreeView2.add(treeview)
        # expand the scrollingTreeView to fill the window
        paned.add2(scrollingTreeView2)


        vbox.pack_start(self.input_field, False, True, 2)
        vbox.pack_start(paned, True, True, 2)
        # add the vertical box to the window
        self.add(vbox)
        self.DeactivateAll()
        self.Initialize()
        self.autosave_interval = 300  # 5 minutes in seconds
        self.autosave_id = GLib.timeout_add_seconds(self.autosave_interval, self.on_autosave)
        self.show_all()

    def TableActivated(self,x,y,z): 
        text=self.entryMenu.get_text()+", "
        if text==", ":
            text=""
        self.entryMenu.set_text(text+self.storeTerm[y][0])
        text=self.entryNouns.get_text()+", "
        if text==", ":
            text=""
        self.entryNouns.set_text(text+self.storeTerm[y][0])

    def TableActivated2(self,x,y,z): 
        text=self.entryMenu.get_text()+", "
        if text==", ":
            text=""
        self.entryMenu.set_text(text+"_".join(self.storeRelationship[y][0].split(" "))+"_"+self.storeRelationship[y][1]+"_"+"_".join(self.storeRelationship[y][2].split(" ")))
        text=self.entryNouns.get_text()+", "

    # destroy the window
    def destroyWindow(self):
        self.destroy()

    def Initialize(self):
        self.autoSaveOn=False
        self.data=[{},{}]
        self.secondCompetencyQuestion=[]
        self.inside=[]
        self.outside=[]
        self.rememberParentToAdd={}
        self.taskNouns=0
        self.nouns={}
        self.moreGeneralized=False
        self.noun=None
        self.parent=None
        self.definedBy=None
        self.entryTask=""
        self.file_path=""
        self.relationships={}
        self.FirstTime=True
        self.storeTermRows={}
        self.storeRelationshipRows={}
        self.storeTerm.clear()
        self.storeRelationship.clear()
        
    def DeactivateAll(self):
        self.input_field.get_visible_child().set_sensitive(False)

    def Menu(self):
        self.entryMenu.set_text("")
        if self.autoSaveOn==True:
            self.autoSaveOn=False
            self.SaveDialog(True)
        self.addTextChatBot(talk.Menu(),100)
        self.input_field.set_visible_child_name("Menu")
        self.input_field.get_visible_child().set_sensitive(True)
    
    def addTextChatBot(self,text,time=100):
        self.textview.add_text("ChatBot:\n\t"+text,time)
        
    def addTextUser(self,text):
        self.textview.add_text("User:\n\t"+text,0)

    def addError(self,text):
        self.addTextChatBot("ERROR:"+text,0)
        dialog = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.WARNING,
                                   buttons=Gtk.ButtonsType.OK, text=text)
        dialog.show_all()
        dialog.run()
        dialog.destroy()

    def rememberOneTime(self,text):
        self.textview.rememberOneTime(text)

    def MenuFunction(self,text,option,*args, **kwargs):
        self.getAnswer="Menu"
        self.DeactivateAll()
        text=self.entryMenu.get_text()
        self.entryMenu.set_text("")
        if option=="Sentence":
            self.textview.add_text("User:\n\tSentence with"+text,0)
            self.whichTask="Sentence"
            Sentence(text,self)
        elif option=="Broaden":
            self.textview.add_text("User:\n\tBroaden:"+text,0)
            self.whichTask="Broaden"
            broaden(text,self)
        elif option=="Narrow":
            self.whichTask="Narrow"
            self.textview.add_text("User:\n\tNarrow:"+text,0)
            narrow(text,self)
        elif option=="Destroy Entity":
            self.whichTask="Destroy Entity"
            self.textview.add_text("User:\n\tDestroy:"+text,0)
            destroy(text,self)

    def getAnswerMenu(self,*args, **kwargs):
        text=self.entryMenu.get_text()
        self.addTextUser(text)
        if "Broaden:" ==text[:8].title():
            self.whichTask="Broaden"
            broaden(text[8:],self)
        elif "Narrow:" ==text[:7].title():
            self.whichTask="Narrow"
            narrow(text[7:],self)
        elif "Destroy:"==text[:8].title():
            self.whichTask="Destroy Entity"
            destroy(text[8:],self)
        else:
            self.whichTask="Sentence"
            Sentence(text,self)

    def getAnswerNouns(self,*args, **kwargs):
        # make it so that when you press enter the text is added to the textview
        text=self.entryNouns.get_text()
        self.addTextUser(text)
        # empty the entry after each entry
        self.entryNouns.set_text("")
        self.inside,self.outside=hear.FindNounsInDataBase(text,self)
        self.iter=0
        self.addOutside()

    # this functions check Inheritance between parent and inside for Narrow and inside and noun for Broaden
    def addInside(self): 
        if self.iter==len(self.inside):
            self.iter=0
            if self.whichTask=="Narrow":
                self.taskNouns-=1
                self.checkTaskNarrow_Broaden()
            elif self.whichTask=="Broaden":
                self.taskNouns-=1
                self.checkTaskNarrow_Broaden()
        else:
            if self.whichTask=="Narrow":
                self.noun=self.inside[self.iter]
                creationFunctions.addInheritance(self.noun,[self.parent],self)
            else:
                self.parent=self.inside[self.iter]
                creationFunctions.addInheritance(self.noun,[self.parent],self)
            self.iter+=1
            self.addInside()

    # this function add the noun that is created
    def addOutside(self):
        if self.iter==len(self.outside):
            self.iter=0
            self.addInside()
        else:
            if self.whichTask=="Narrow":
                self.noun=self.outside[self.iter]
                creationFunctions.createNoun(self.noun,self.parent,self,False)            
            else:
                self.parent=self.outside[self.iter]
                creationFunctions.createNoun(self.parent,[],self,False)            
                # creationFunctions.addInheritance(self.noun,[self.parent],self)

    def checkTaskNarrow_Broaden(self):
        if self.taskNouns==0:
            self.Menu()
        else:
            if self.whichTask=="Narrow":
                self.parent=self.nouns[len(self.nouns)-self.taskNouns]
                self.addTextChatBot(talk.whatToNarrow(self.parent))
            else:
                self.noun=self.nouns[len(self.nouns)-self.taskNouns]
                self.addTextChatBot(talk.whatToBroaden(self.noun))
            self.input_field.set_visible_child_name("getNouns")
            self.entryNouns.set_text("")

    def checkTaskAddTerm(self):
        if self.taskNouns==0:
            options=[]
            for relation in self.relationships.keys():
                
                term1=self.relationships[relation][0]
                term2=self.relationships[relation][1]

                key=hear.stemmer.stem(relation.lower())
                if key!= []:
                    key =key.title()
                    self.rememberOneTime("Stemmed the \""+relation+"\" to \""+key+"\"\n")
                    relation=key
                combination=term1+"_"+relation+"_"+term2.title()
                # one object was not kept
                if term1 not in self.data[0].keys() or term2 not in self.data[0].keys():
                    continue
                options.append(combination)
            if options!=[]:
                dialog=CheckDialog(self,options,"Choose the relationships you want to keep")
                selectedRelationships = dialog.run()
                text="Selected:\n"
                for selected in selectedRelationships:
                    text+=selected+"\n"
                    theRelationship=selected.split("_")
                    term1=theRelationship[0]
                    relation=theRelationship[1]
                    term2=theRelationship[2]
                    creationFunctions.createRelation(self.data,self,term1,relation,term2)
                self.addTextUser(text)   
            if len(self.secondCompetencyQuestion)!=0:
                Sentence(self.secondCompetencyQuestion.pop(),self)
            else:
                self.Menu()
        else:
            self.input_field.set_sensitive(True)
            self.noun=list(self.nouns.keys())[len(self.nouns.keys())-self.taskNouns]
            self.parent=self.nouns[self.noun]
            creationFunctions.createNoun(self.noun,self.parent,self)

    def search(self):
        self.addTextChatBot(talk.FindDefinition(self.noun))
        self.input_field.set_visible_child_name("Definitions")

    def DefinitionMenu(self,*args, **kwargs):
        answer=args[1]
        self.addTextUser(answer)
        keep=True
        theNoun=self.noun
        theParents=self.parent
        if self.whichTask=="Broaden":
            theNoun=self.parent
            theParents=[]
        if answer=="Search Online":
            answer=searchForTerm(self.data,theNoun,theParents,self,self.moreGeneralized)            
            if answer==True:
                return
        elif answer=="Give Definition":
            self.definedBy="You"
            self.addTextChatBot(talk.GiveDefinition(theNoun))
            answer = TextDialog(self,talk.GiveDefinition(theNoun)).run()
            self.addTextUser(str(answer))
            if answer!="Cancel":
                # create the object
                self.data[0][self.noun]=[manager.CreateObject(self.data[2],self.noun,self),self.noun,[],0,0]
                self.AddToTableTerm(self.noun)
                # add definition
                manager.Explanation(self.data[2],self.data[0][self.noun][0],answer,self.definedBy,self)
                self.secondCompetencyQuestion.append(answer)
            else:
                keep=False
        elif answer=="Keep Without Definition":
            self.addTextChatBot(talk.KeepWithoutDefinition(theNoun))
            # create the object
            self.data[0][theNoun]=[manager.CreateObject(self.data[2],theNoun,self),theNoun,[],0,0]
            self.AddToTableTerm(theNoun)
            # add definition
            manager.Explanation(self.data[2],self.data[0][theNoun][0],"","",self)
        elif answer=="Do Not Keep Term":
            keep=False
            self.addTextChatBot(talk.DoNotKeep(answer))
        # if you keep the item then check for Inheritance
        if keep==True:
            creationFunctions.addInheritance(self.noun,[self.parent],self)
        # go to next noun
        if self.whichTask=="Sentence":
            self.taskNouns-=1
            self.checkTaskAddTerm()
        elif self.whichTask=="Narrow":
            self.iter+=1
            self.addOutside()
        elif self.whichTask=="Broaden":
            self.iter+=1
            self.addOutside()

    def error(self,error):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.CANCEL,
            text=error,
        )
        dialog.run()
        dialog.destroy()

    def helpfulFunctionAdding(self,total,thisFar):
        if total==len(thisFar):
            return
        for i in self.data[0].keys():
            term=i
            if i in thisFar:
                continue

            flag=False
            for parent in self.data[0][term][2]:
                if parent not in thisFar:
                    flag=True
                    break 
            if flag==True:
                continue
            self.storeTermRows[term]=[]
            if self.data[0][term][2]==[]:
                self.storeTermRows[term].append(self.storeTerm.append(None,[term]))
            else:
                for parent in self.data[0][term][2]:
                    for k in self.storeTermRows[parent]:
                        self.storeTermRows[term].append(self.storeTerm.append(k,[term]))
            break
        self.helpfulFunctionAdding(total,thisFar+[term])
        
    def AddToTableTerms(self):
        self.helpfulFunctionAdding(len(self.data[0].keys()),[])

    def AddToTableTerm(self,term):
        self.storeTerm.clear()
        self.storeTermRows={}
        self.AddToTableTerms()

    def AddToTableParent(self,noun,theParent):
        self.storeTerm.clear()
        self.storeTermRows={}
        self.AddToTableTerms()

    def AddToTableRelationship(self,relation):
        obj1=""
        for i in self.data[1][relation][1]:
            obj1+=i+" or "
        if obj1!="":
            obj1=obj1[:-4]
        obj2=""
        for i in self.data[1][relation][3]:
            obj2+=i+" or "
        if obj2!="":
            obj2=obj2[:-4]

        if relation not in self.storeRelationshipRows.keys(): 
            self.storeRelationshipRows[relation]=self.storeRelationship.append(None,[obj1,self.data[1][relation][2],obj2])
        else:
            self.storeRelationship.set_value(self.storeRelationshipRows[relation],0,obj1)
            self.storeRelationship.set_value(self.storeRelationshipRows[relation],2,obj2)

    def RemoveTerm(self,term):
        self.storeTerm.clear()
        self.storeTermRows={}
        for i in self.data[0].keys():
            self.AddToTableTerm(i)
        
    def RemoveRelationship(self,relationship):
        self.storeRelationship.remove(self.storeRelationshipRows[relationship])
        self.storeRelationshipRows.pop(relationship)

    def SaveDialog(self,flag=False):
        if flag==True:
            dialog=SaveDialog(self,"Auto")
        else:
            dialog=SaveDialog(self)
        response = dialog.run()
        if response == Gtk.ResponseType.YES and self.data!=[{},{}]:
            manager.SaveOntology(self.data[2],self.file_path,self)
        dialog.destroy()

    def quitFunction(self,widget, event):
        self.SaveDialog()
        self.destroy()
    
    def on_autosave(self):
        self.autoSaveOn=True
        return True

    def Consistency(self,*args):
        self.addTextUser("Consistency.")
        with self.data[2]:
            sync_reasoner()
        result=list(self.data[2].inconsistent_classes())
        if result!=[]:
            text="The inconsistent classes are the following:\n"
            text+=str(list(self.data[2].inconsistent_classes()))
            self.addTextChatBot(text)
            dialog = Gtk.MessageDialog(parent=self, flags=0,
                                buttons=Gtk.ButtonsType.OK, text=text)
        else:
            self.addTextChatBot("Your ontology is consistent!!")
            dialog = Gtk.MessageDialog(parent=self, flags=0,
                                buttons=Gtk.ButtonsType.OK, text="Your ontology is consistent!!")
        Gtk.Dialog.run(dialog)
        dialog.destroy()
    
                            
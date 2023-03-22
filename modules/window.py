from modules.searchOntology import *
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import modules.slowTextView as stv
from modules.mainFunction import *
import modules.creationFunctions as creationFunctions
from modules.dialogOptions import CheckDialog
import modules.chatbotTalks as talk
import modules.ontologyManager as manager

class C4OWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        self.whichTask=""
        super().__init__(*args, **kwargs)
        
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
        self.hb.props.title = self.file_name+" - C4O"
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


        input= Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        input.set_homogeneous(False)

        self.broaden=Gtk.Button("Broaden")
        self.broaden.set_sensitive(False)
        input.pack_start(self.broaden, False, False, 2)

        self.narrow=Gtk.Button("Narrow")
        self.narrow.set_sensitive(False)
        input.pack_start(self.narrow, False, False, 2)

        self.trash=Gtk.Button()
        # add the image bin.png to the button and resize it to the size of the button
        image = Gtk.Image.new_from_file("modules/trash.png")
        image.set_pixel_size(20)
        self.trash.add(image)
        self.trash.set_sensitive(False)
        input.pack_start(self.trash,False, False, 2)

        self.input_field= Gtk.Stack()
        # add a text entry
        self.entry = Gtk.Entry()

        # add a button to the input field
        buttonTrue=Gtk.Button("True")
        buttonTrue.get_style_context().add_class("suggested-action")
        buttonFalse=Gtk.Button("False")
        buttonFalse.get_style_context().add_class("destructive-action")
        buttonTrue.connect("clicked", lambda x: self.textview.add_text("User:\n\tTrue"))
        buttonFalse.connect("clicked", lambda x: self.textview.add_text("User:\n\tFalse"))
        buttonTrue.colour="green"
        buttonFalse.colour="red"
        bothButtons=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        bothButtons.pack_start(buttonTrue,False, False, 2)
        bothButtons.pack_start(buttonFalse,False, False, 2)
        bothButtons.props.halign=Gtk.Align.CENTER

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

        self.input_field.add_named(self.entry,"Entry")
        self.entry.set_visible (True)
        self.entry.connect("activate",self.getAnswer)
        self.input_field.add_named(bothButtons,"TrueOrFalse")
        bothButtons.set_visible (True)
        self.input_field.add_named(definitionButtons,"Definitions")
        definitionButtons.set_visible (True)
        self.input_field.set_visible_child_name("Entry")

        input.pack_start(self.input_field,True, True, 2)

        self.competencyQuestion=Gtk.Button("Competency Question")
        input.pack_start(self.competencyQuestion,False, False, 2)

        self.competencyQuestion.connect("clicked",self.MenuFunction,"Sentence")
        self.broaden.connect("clicked",self.MenuFunction,"Broaden")
        self.narrow .connect("clicked",self.MenuFunction,"Narrow")
        self.trash.connect("clicked",self.MenuFunction,"Destroy Entity")
        


        # TABLES
        paned=Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        paned.set_wide_handle(True)
        paned.set_position(500)
        self.storeTerm = Gtk.TreeStore(str, str, str)

        treeview = Gtk.TreeView(self.storeTerm)
        treeview.set_tooltip_column(2)
        treeview.set_hover_selection(True)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Term", renderer, text=0)
        treeview.append_column(column)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Parent", renderer, text=1)
        treeview.append_column(column)
        
        # # when a value is clicked in the treeview, add the title to the entry with the previous text
        # # and make the broaden button and narrow button active         
        treeview.connect("row-activated", self.TableActivated)
        # # if the entry is empty, make the broaden button and narrow button inactive
        self.entry.connect("changed", self.EntryChanged)

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


        vbox.pack_start(input, False, True, 2)
        vbox.pack_start(paned, True, True, 2)
        # add the vertical box to the window
        self.add(vbox)
        self.DeactivateAll()
        self.Initialize()
        self.show_all()

    def TableActivated(self,x,y,z): 
        text=self.entry.get_text()+", "
        if text==", ":
            text=""
        self.entry.set_text(text+self.storeTerm[y][0])
        self.broaden.set_sensitive(True)
        self.narrow.set_sensitive(True)
        self.trash.set_sensitive(True)
        self.competencyQuestion.set_sensitive(False)

    def TableActivated2(self,x,y,z): 
        text=self.entry.get_text()+", "
        if text==", ":
            text=""
        self.entry.set_text(text+self.storeRelationship[y][0]+"_"+self.storeRelationship[y][1]+"_"+self.storeRelationship[y][2])
        self.broaden.set_sensitive(True)
        self.narrow.set_sensitive(True)
        self.trash.set_sensitive(True)
        self.competencyQuestion.set_sensitive(False)

    def EntryChanged(self,x):
        self.broaden.set_sensitive(False)
        self.narrow.set_sensitive(False)
        self.trash.set_sensitive(False)
        self.competencyQuestion.set_sensitive(True)

    # destroy the window
    def destroyWindow(self):
        self.destroy()

    def Initialize(self):
        self.data=[{},{}]
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
        self.broaden.set_sensitive(False)
        self.narrow.set_sensitive(False)
        self.trash.set_sensitive(False)
        self.input_field.get_visible_child().set_sensitive(False)
        self.competencyQuestion.set_sensitive(False)

    def Menu(self):
        self.addTextChatBot(talk.Menu(),100)
        if self.FirstTime==True:
            self.FirstTime=False
            self.addTextChatBot(talk.Help(),100)
        manager.SaveOntology(self.data[2],self.file_path,self)
        self.broaden.set_sensitive(False)
        self.narrow.set_sensitive(False)
        self.trash.set_sensitive(False)
        self.input_field.set_visible_child_name("Entry")
        self.input_field.get_visible_child().set_sensitive(True)
        self.competencyQuestion.set_sensitive(True)
        self.entryTask="Menu"
    
    def TrueFalseAnswer(self):
        self.broaden.set_sensitive(False)
        self.narrow.set_sensitive(False)
        self.trash.set_sensitive(False)
        self.competencyQuestion.set_sensitive(False)    
        self.input_field.set_visible_child_name("TrueOrFalse")

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
        text=self.entry.get_text()
        self.entry.set_text("")
        if option=="Sentence":
            self.textview.add_text("User:\n\tSentence with"+text,0)
            self.whichTask="Sentence"
            Sentence(text,self)
        elif option=="Broaden":
            self.textview.add_text("User:\n\tBroaden with"+text,0)
            self.whichTask="Broaden"
            broaden(text,self)
        elif option=="Narrow":
            self.whichTask="Narrow"
            self.textview.add_text("User:\n\tNarrow with"+text,0)
            narrow(text,self)
        elif option=="Destroy Entity":
            self.whichTask="Destroy Entity"
            self.textview.add_text("User:\n\tDestroy:"+text,0)
            destroy(text,self)

    def getAnswer(self,*args, **kwargs):
        # make it so that when you press enter the text is added to the textview
        text=self.entry.get_text()
        self.addTextUser(text)
        # empty the entry after each entry
        self.entry.set_text("")
        if self.entryTask=="Menu":
            if self.competencyQuestion.get_sensitive()==True:
                self.whichTask="Sentence"
                Sentence(text,self)
            else:
                self.addTextChatBot(talk.CouldNotUnderstand()+"Please select a button!")
                self.Menu()
        elif self.entryTask=="definition":
            theNoun=self.noun
            if self.whichTask=="Broaden":
                theNoun=self.parent
            self.definedBy="You"
            # create the object
            self.data[0][theNoun]=[manager.CreateObject(self.data[2],theNoun,self),theNoun,[],0,0]
            self.AddToTableTerm(theNoun)
            
            # add definition
            manager.Explanation(self.data[2],self.data[0][theNoun][0],text,self.definedBy,self)
            creationFunctions.addInheritance(self.noun,[self.parent],self)
            if self.whichTask=="Sentence":
                self.taskNouns-=1
                self.checkTaskAddTerm()
            elif self.whichTask=="Narrow":
                self.iter+=1
                self.addOutside()
            elif self.whichTask=="Broaden":
                self.iter+=1
                self.addOutside()
        elif self.entryTask=="get nouns":
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
            self.input_field.set_visible_child_name("Entry")
            self.entryTask="get nouns"
            self.broaden.set_sensitive(False)
            self.narrow.set_sensitive(False)
            self.trash.set_sensitive(False)
            self.entry.set_sensitive(True)
            self.competencyQuestion.set_sensitive(False)

    def checkTaskAddTerm(self):
        if self.taskNouns==0:
            options=[]
            for relation in self.relationships.keys():
                
                term1=self.relationships[relation][0]
                term2=self.relationships[relation][1]
                combination=term1+"_"+relation.title()+"_"+term2.title()
                # one object was not kept
                if term1 not in self.data[0].keys() or term2 not in self.data[0].keys():
                    return
                if relation.title() in self.data[1].keys():
                    self.addTextChatBot("The relationship \""+combination+"\" is already in the dataBase")
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
            self.input_field.set_visible_child_name("Entry")
            self.entryTask="definition"
            self.addTextChatBot(talk.GiveDefinition(theNoun))
            return
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

    def GiveDefinition(self,definition):
        self.definedBy="You"
        # create the object
        self.data[0][self.noun]=[manager.CreateObject(self.data[2],self.noun,self),self.noun,[],0,0]
        self.AddToTableTerm(self.noun)
        # add definition
        manager.Explanation(self.data[2],self.data[0][self.noun][0],definition,self.definedBy,self)

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

    def AddToTableTerm(self,term):
        theParents=""
        for parent in self.data[0][term][2]:
            theParents+=parent+" "
        if theParents=="":
            theParents="None"
        else:
            theParents=theParents[:-1]
        self.storeTermRows[term]=self.storeTerm.append(None, [term,theParents,"Parents:\n"+str(self.data[0][term][2])])
        if term in self.rememberParentToAdd.keys():
            for i in self.rememberParentToAdd[term]:
                self.storeTerm.append(self.storeTermRows[term], ["Children",i,"Parents:\n"+str(self.data[0][term][2])])
            self.rememberParentToAdd.pop(term)  
        if theParents!="":
            theParents=theParents.split(" ")
        for parent in theParents:
            if parent in self.storeTermRows:
                self.storeTerm.insert_after(self.storeTermRows[parent],None, ["Children",term,"Parents:\n"+str(self.data[0][term][2])])
            else:
                if parent not in self.rememberParentToAdd.keys():
                    self.rememberParentToAdd[parent]=[] 
                self.rememberParentToAdd[parent].append(term)

    def AddToTableRelationship(self,term1,relation,term2):
        self.storeRelationshipRows[relation]=self.storeRelationship.append(None,[term1,relation,term2])
        
    def AddToTableParent(self,noun,theParent):
        theParents=""
        for parent in self.data[0][noun][2]:
            theParents+=parent+" "
        if theParents=="":
            theParents="None"
        else:
            theParents=theParents[:-1]
        print(theParents)
        self.storeTerm.set_value(self.storeTermRows[noun],1,theParents)
        self.storeTerm.set_value(self.storeTermRows[noun],2,"Parents:\n"+str(self.data[0][noun][2]))
        self.storeTerm.insert_after(self.storeTermRows[theParent],None, ["Children",noun,"Parents:\n"+str(self.data[0][noun][2])])

    def RemoveTerm(self,term):
        whatToRemove=[]
        for row in range(len(self.storeTerm)):
            values = [str(self.storeTerm[row][col]) for col in range(3)]
            parents=values[2][9:].strip('][').split('\'')
            total=""
            flag=False
            # check if the term is a parent
            for i in range(len(parents)):
                if i%2==1:
                    if term == parents[i]:
                        flag=True
                        continue
                    total+=parents[i]
            if flag==True:
                if total=="":
                    total="None"
                self.storeTerm.set_value(self.storeTerm[row].iter,1,total)
                self.storeTerm.set_value(self.storeTerm[row].iter,2,"Parents:\n"+str(total))
            # check if the term is in the child
            if self.storeTerm.iter_has_child(self.storeTerm[row].iter)==True:
                if term == self.storeTerm[self.storeTerm.iter_children(self.storeTerm[row].iter)][1]:
                    whatToRemove.append(self.storeTerm.iter_children(self.storeTerm[0].iter))

        for i in whatToRemove:
            self.storeTerm.remove(i)

        self.storeTerm.remove(self.storeTermRows[term])
        self.storeTermRows.pop(term)
        
    def RemoveRelationship(self,relationship):
        print(relationship)
        self.storeRelationship.remove(self.storeRelationshipRows[relationship])
        self.storeRelationshipRows.pop(relationship)

    # ΤΟ DO
    # fix relationship table
    # save save
    # Text: Broaden: list
    # insert grade out the buttons
    # give definition + button
    # None-> Thing as parent
    # kati [] []
    # na einai mia apli inheritane 
    # sync_reasoner() then inconsistent_classes() + button
    # save -> create save button, autosave, close ask
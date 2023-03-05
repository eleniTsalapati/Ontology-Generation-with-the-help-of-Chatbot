import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import modules.slowTextView as stv
from modules.mainFunction import *
from modules.shared_data import *
class C4OWindow(Gtk.ApplicationWindow):
    def __init__(self,file_path,file_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # make the application be at the maximum size of the screen
        self.file_path = file_path
        self.file_name = file_name
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
        buttonNoDefinition=Gtk.Button("Without Definition")
        buttonNoKeep=Gtk.Button("Do Not Keep Term")
        definitionButtons=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        definitionButtons.pack_start(buttonSearch,False, False, 2)
        definitionButtons.pack_start(buttonGiveDefinition,False, False, 2)
        definitionButtons.pack_start(buttonNoDefinition,False, False, 2)
        definitionButtons.pack_start(buttonNoKeep,False, False, 2)
        definitionButtons.props.halign=Gtk.Align.CENTER

        self.input_field.add_named(self.entry,"entry")
        self.entry.set_visible (True)
        self.input_field.add_named(bothButtons,"TrueOrFalse")
        bothButtons.set_visible (True)
        self.input_field.add_named(definitionButtons,"Definitions")
        definitionButtons.set_visible (True)
        self.input_field.set_visible_child_name("entry")

        input.pack_start(self.input_field,True, True, 2)

        self.competencyQuestion=Gtk.Button("Competency Question")
        input.pack_start(self.competencyQuestion,False, False, 2)

        self.competencyQuestion.connect("clicked",self.MenuFunction,"Sentence")
        self.broaden.connect("clicked",self.MenuFunction,"Generalized")
        self.narrow .connect("clicked",self.MenuFunction,"Specialize")
        self.trash.connect("clicked",self.MenuFunction,"Destroy Entity")
        


        # TABLES
        paned=Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        paned.set_wide_handle(True)
        paned.set_position(500)
        store = Gtk.TreeStore(str, str, str)

        treeview = Gtk.TreeView(store)
        treeview.set_tooltip_column(2)
        treeview.set_hover_selection(True)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Title", renderer, text=0)
        treeview.append_column(column)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Description", renderer, text=1)
        treeview.append_column(column)

        row1=store.append(None, ["Child", "This is the description for Item 1", "The child are:None\n The Parents are: Parent,GrandParent"])
        # row2=store.append(None, ["Parent", "This is the description for Item 2", "The child are:Child\n The Parents are: GrandParent"])
        # row3=store.append(None, ["GrandParent", "This is the description for Item 3", "The child are:Child,Parent\n The Parents are:None"])
        store.append(row1, ["Parent: Parent","",""])
        # store.append(row1, ["Parent: GrandParent","",""])
        # store.append(row2, ["Child: child","",""])
        # store.append(row2, ["Parent: GrandParent","",""])
        # store.append(row3, ["Child: child","",""])
        # store.append(row3, ["Child: Parent","",""])

        # # when a value is clicked in the treeview, add the title to the entry with the previous text
        # # and make the broaden button and narrow button active         
        # treeview.connect("row-activated", lambda x, y, z: entry.get_text() + " " +entry.set_text(store[y][0]))
        # treeview.connect("row-activated", lambda x, y, z: broaden.set_sensitive(True))
        # treeview.connect("row-activated", lambda x, y, z: narrow.set_sensitive(True))
        # treeview.connect("row-activated", lambda x, y, z: trash.set_sensitive(True))
        # treeview.connect("row-activated", lambda x, y, z: competencyQuestion.set_sensitive(False))
        # # if the entry is empty, make the broaden button and narrow button inactive
        # entry.connect("changed", lambda x: broaden.set_sensitive(False))
        # entry.connect("changed", lambda x: narrow.set_sensitive(False))
        # entry.connect("changed", lambda x: trash.set_sensitive(False))
        # entry.connect("changed", lambda x: competencyQuestion.set_sensitive(True))

        # add a scrollable treeview
        scrollingTreeView1=Gtk.ScrolledWindow()
        scrollingTreeView1.add(treeview)

        paned.add1(scrollingTreeView1)

        store = Gtk.TreeStore(str, str, str)
        treeview = Gtk.TreeView(store)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Term", renderer, text=0)
        treeview.append_column(column)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Connection", renderer, text=1)
        treeview.append_column(column)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Term", renderer, text=2)
        treeview.append_column(column)

        # row1=store.append(None, ["Child", "is_aasdasdsasdadsasadsadsdasdasadsdasaasddsasdasadsadsadsadasdasdsadsaddsadsdasadsdasadsdas", "Parent"])
        # row2=store.append(None, ["Parent", "is_a", "GrandParent"])
        # row3=store.append(None, ["GrandParent", "is_a", "GreatGrandParent"])

        # make the store have the values to be wrapped
        
        # add a scrollable treeview
        scrollingTreeView2=Gtk.ScrolledWindow()
        scrollingTreeView2.add(treeview)
        # expand the scrollingTreeView to fill the window
        paned.add2(scrollingTreeView2)


        vbox.pack_start(input, False, True, 2)
        vbox.pack_start(paned, True, True, 2)
        # add the vertical box to the window
        self.add(vbox)
        self.Start()
        self.show_all()

    
    # destory the window
    def destroyWindow(self):
        self.destroy()

    # create a new file
    def createNewWindow(self,file_path,file_name):
        win2 = C4OWindow(file_path,file_name,application=self.get_application())
        win2.show_all()

    def Start(self):
        self.broaden.set_sensitive(False)
        self.narrow.set_sensitive(False)
        self.trash.set_sensitive(False)
        self.input_field.get_visible_child().set_sensitive(False)
        self.competencyQuestion.set_sensitive(False)

    def Menu(self):
        self.broaden.set_sensitive(False)
        self.narrow.set_sensitive(False)
        self.trash.set_sensitive(False)
        self.input_field.get_visible_child().set_sensitive(True)
        self.competencyQuestion.set_sensitive(True)
    
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
        text=self.entry.get_text()
        self.textview.add_text("User:\n\t"+text,0)
        global answerUI,hearServer,dangerArea
        dangerArea.acquire()
        answerUI=option+";"+text
        dangerArea.release()
        hearServer.release()

    def getAnswer(self):
        # make it so that when you press enter the text is added to the textview
        self.entry.connect("activate", lambda x: self.textview.add_text("User:\n\t"+self.entry.get_text(),0))
        # empty the entry after each entry
        self.entry.connect("activate", lambda x: self.entry.set_text(""))
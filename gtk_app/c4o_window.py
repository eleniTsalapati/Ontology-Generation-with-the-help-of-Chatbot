import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import slowTextView as stv

class C4OWindow(Gtk.ApplicationWindow):
    def __init__(self,file_path,file_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # make the application be at the maximum size of the screen
        self.maximize()
        self.file_path = file_path
        self.file_name = file_name

        # window properties
        #
        self.set_border_width(10)
        self.set_default_size(400, 200)

        # headerbar
        #
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = self.file_name+" - C4O"
        self.set_titlebar(hb)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hb.pack_start(box)

        file_button = Gtk.MenuButton.new()
        box.add(file_button)

        file_button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        file_button.add(file_button_box)

        file_label = Gtk.Label("File")
        down_arrow_image = Gtk.Arrow(arrow_type=Gtk.ArrowType.DOWN, shadow_type=Gtk.ShadowType.NONE)
        file_button_box.add(file_label)
        file_button_box.add(down_arrow_image)

        with open('file_menu.xml', 'r') as f:
            menu_xml = f.read()
            builder = Gtk.Builder.new_from_string(menu_xml, -1)
            menu = builder.get_object("file-menu")
            file_button.set_menu_model(menu)

        # make a vertical box that is in all the space of the window
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # make a textview
        textview = stv.SlowTextView()
        if file_path == "":
            textview.add_text("ChatBot:\n\tGreetings new user! This is the the ChatBot for Ontologies.\n To continue select a folder to create a new ontology or select an existing ontology to edit.",0)
        else:
            textview.add_text("ChatBot:\n\tGreetings. The file "+file_name+" has been opened.",0)        

        # make a scrollable textview
        scrollingTextView=Gtk.ScrolledWindow()
        scrollingTextView.add(textview)
        # add the textview+scrolling to the vertical box
        vbox.pack_start(scrollingTextView, True, True, 2)


        grid= Gtk.Grid()
        grid.set_column_homogeneous(True)

        broaden=Gtk.Button("Broaden")
        broaden.set_sensitive(False)
        grid.attach(broaden,0,0,1,1)

        narrow=Gtk.Button("Narrow")
        narrow.set_sensitive(False)
        grid.attach(narrow,1,0,1,1)

        trash=Gtk.Button()
        # add the image bin.png to the button and resize it to the size of the button
        image = Gtk.Image.new_from_file("trash.png")
        image.set_pixel_size(20)
        trash.add(image)
        trash.set_sensitive(False)
        grid.attach(trash,2,0,1,1)

        # add a text entry
        entry = Gtk.Entry()
        # make it so that when you press enter the text is added to the textview
        entry.connect("activate", lambda x: textview.add_text("User:\n\t"+entry.get_text()))
        # empty the entry after each entry
        entry.connect("activate", lambda x: entry.set_text(""))
        grid.attach(entry,3,0,5,1)

        Competency_Question=Gtk.Button("Competency Question")
        if file_path == "":
            Competency_Question.set_sensitive(False)
        else:
            Competency_Question.set_sensitive(True)
        grid.attach(Competency_Question,8,0,3,1)

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
        row2=store.append(None, ["Parent", "This is the description for Item 2", "The child are:Child\n The Parents are: GrandParent"])
        row3=store.append(None, ["GrandParent", "This is the description for Item 3", "The child are:Child,Parent\n The Parents are:None"])
        store.append(row1, ["Parent: Parent","",""])
        store.append(row1, ["Parent: GrandParent","",""])
        store.append(row2, ["Child: child","",""])
        store.append(row2, ["Parent: GrandParent","",""])
        store.append(row3, ["Child: child","",""])
        store.append(row3, ["Child: Parent","",""])

        # when a value is clicked in the treeview, add the title to the entry with the previous text
        # and make the broaden button and narrow button active         
        treeview.connect("row-activated", lambda x, y, z: entry.get_text() + " " +entry.set_text(store[y][0]))
        treeview.connect("row-activated", lambda x, y, z: broaden.set_sensitive(True))
        treeview.connect("row-activated", lambda x, y, z: narrow.set_sensitive(True))
        treeview.connect("row-activated", lambda x, y, z: trash.set_sensitive(True))
        treeview.connect("row-activated", lambda x, y, z: Competency_Question.set_sensitive(False))
        # if the entry is empty, make the broaden button and narrow button inactive
        entry.connect("changed", lambda x: broaden.set_sensitive(False))
        entry.connect("changed", lambda x: narrow.set_sensitive(False))
        entry.connect("changed", lambda x: trash.set_sensitive(False))
        entry.connect("changed", lambda x: Competency_Question.set_sensitive(True))

        # add a scrollable treeview
        scrollingTreeView=Gtk.ScrolledWindow()
        scrollingTreeView.add(treeview)
        grid.attach(scrollingTreeView,0,1,7,1)


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

        row1=store.append(None, ["Child", "is_aasdasdsasdadsasadsadsdasdasadsdasaasddsasdasadsadsadsadasdasdsadsaddsadsdasadsdasadsdas", "Parent"])
        row2=store.append(None, ["Parent", "is_a", "GrandParent"])
        row3=store.append(None, ["GrandParent", "is_a", "GreatGrandParent"])

        # make the store have the values to be wrapped
        
        # add a scrollable treeview
        scrollingTreeView=Gtk.ScrolledWindow()
        scrollingTreeView.add(treeview)
        grid.attach(scrollingTreeView,7,1,4,1)

        vbox.pack_start(grid, True, True, 0)

        # add the vertical box to the window
        self.add(vbox)

        self.show_all()


    # destory the window
    def destroyWindow(self):
        self.destroy()

    # create a new file
    def createNewWindow(self,file_path,file_name):
        win2 = C4OWindow(file_path,file_name,application=self.get_application())
        win2.show_all()


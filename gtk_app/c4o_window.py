import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import slowTextView as stv

class C4OWindow(Gtk.ApplicationWindow):
    def __init__(self,file_path,file_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

        # make a textview
        textview = stv.SlowTextView()
        if file_path == "":
            textview.add_text("ChatBot:\n\tGreetings new user! This is the the ChatBot for Ontologies.\n To continue select a folder to create a new ontology or select an existing ontology to edit.",0)
        else:
            textview.add_text("ChatBot:\n\tGreetings. The file "+file_name+" has been opened.",0)
        textview.set_editable(False)
        # have the textview not clickable
        # have the textview be only 50% of the window
        textview.set_size_request(0, 100)
        self.add(textview)
        

        # make a scrollable textview
        scrollingTextView=Gtk.ScrolledWindow()
        scrollingTextView.add(textview)
        self.add(scrollingTextView)

        # add a text entry
        entry = Gtk.Entry()
        # make it so that when you press enter the text is added to the textview
        entry.connect("activate", lambda x: textview.add_text("User:\n\t"+entry.get_text()))
        # have the entry be only 50% of the window above the textview
        entry.set_size_request(0, 50)   
        self.add(entry)
        
        
        # TODO: ADD A VERTICAL BOX WIDGET IN THE WINDOW (self.add)

        #       ADD A TEXT VIEW IN THE VERTICAL BOX AND MAKE IT READ-ONLY (Gtk.TextView.props.editable)
        #       ADD A SCROLLABLE WINDOW AROUND THE TEXT VIEW (Gtk.ScrolledWindow)
        #       ADD AN ENTRY IN THE VERTICAL BOX
        #       MAKE IT SO EVERYTHING YOU WRITE IN THE ENTRY APPEARS IN THE TEXTVIEW (like a chat) (Gtk.Entry.signals.activate)

        self.show_all()


    # destory the window
    def destroyWindow(self):
        self.destroy()
        
    # create a new file
    def createNewWindow(self,file_path,file_name):
        win2 = C4OWindow(file_path,file_name,application=self.get_application())
        win2.show_all()


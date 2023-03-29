import modules.chatbotTalks as talk
import modules.ontologyManager as manager
from modules.mainFunction import *
import gi,os

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gio, Gtk

from modules.window import C4OWindow

class C4OApplication(Gtk.Application):
    def __init__(self,*args, **kwargs):
        
        super().__init__(
            *args,
            application_id="org.example.myapp",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
            **kwargs
        )

        self.window = None
        self.add_main_option(
            "test",
            ord("t"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            "Command line test",
            None,
        )

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

        action = Gio.SimpleAction.new("open_file", None)
        action.connect("activate", self.open_file)
        self.add_action(action)

        action = Gio.SimpleAction.new("create_file", None)
        action.connect("activate", self.create_file)
        self.add_action(action)

        action = Gio.SimpleAction.new("help", None)
        action.connect("activate", self.help)
        self.add_action(action)

        action = Gio.SimpleAction.new("save", None)
        action.connect("activate", self.save_ontology)
        self.add_action(action)
        

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = C4OWindow(application=self, title="Main Window")

        self.window.present()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        # convert GVariantDict -> GVariant -> dict
        options = options.end().unpack()

        if "test" in options:
            # This is printed on the main instance
            print("Test argument recieved: %s" % options["test"])

        self.activate()
        return 0

    def open_file(self,action,param):
        dialog=Gtk.FileChooserDialog("Please choose a file",self.window,
                                     Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN,Gtk.ResponseType.OK))
        
        # a filter that accepts only .owl files
        x = Gtk.FileFilter()
        x.set_name("OWL files")
        x.add_pattern("*.owl")
        dialog.add_filter(x)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            file_path = dialog.get_filename()
            dialog.destroy()
            self.fileOpened(file_path)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
            dialog.destroy()

    def create_file(self,action,param):
        dialog=Gtk.FileChooserDialog("Please choose a file",self.window,
                                     Gtk.FileChooserAction.SAVE,(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_SAVE,Gtk.ResponseType.OK))
        dialog.set_do_overwrite_confirmation(True)
        
        # a filter that accepts only .owl files
        x = Gtk.FileFilter()
        x.set_name("OWL files")
        x.add_pattern("*.owl")
        dialog.add_filter(x)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            file_path = dialog.get_filename()
            # check if it has ".owl" extension
            if not file_path.endswith(".owl"):
                file_path += ".owl"
            # remove the file if it already exists
            if os.path.exists(file_path):
                os.remove(file_path)
            # create the file
            open(file_path, 'x').close()
            dialog.destroy()
            self.fileOpened(file_path)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
            dialog.destroy()

    def help(self, action, param):
        dialog = Gtk.MessageDialog(parent=self.window, flags=0,
                               buttons=Gtk.ButtonsType.OK, text=talk.Help())

        Gtk.Dialog.run(dialog)
        dialog.destroy()

    def on_about(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self.window)
        # add text to the about dialog
        about_dialog.set_program_name("C4O")
        about_dialog.set_version("0.1")
        about_dialog.set_authors(["Lionis Emmanouil Georgios(Akis)","Tsalapati Eleni","Sergios - Anestis Kefalidis","Koubarakis Manolis"])
        # set no icon for the about dialog
        about_dialog.set_logo_icon_name(None)
        about_dialog.set_comments("A simple ontology editor that uses communication with a chatbot to help the user create ontologies.")
        about_dialog.present()

    def on_quit(self, action, param):
        self.window.SaveDialog()
        self.quit()

    def save_ontology(self,action,param):
        manager.SaveOntology(self.window.data[2],self.window.file_path,self.window)

    def fileOpened(self,path):
        # opening the path
        path="file://"+path
        self.window.Initialize()
        self.window.file_path=path
        answer=manager.LoadOntology(path,self.window.addError)
        if answer!=None:
            self.window.data.append(answer)
            manager.addData(self.window.data[2],self.window.data,self.window)
            # rename the UI
            file_name = path.split("/")[-1]
            self.window.hb.props.title = file_name + "- C4O"
            self.window.addTextUser("Open"+ path)
            self.window.addTextChatBot("Openning the file \""+path+"\". Wait for a moment...")
            self.window.Menu()
    

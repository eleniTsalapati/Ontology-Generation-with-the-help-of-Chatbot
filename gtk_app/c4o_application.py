import sys

import gi,os

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gio, Gtk

from c4o_window import C4OWindow

class C4OApplication(Gtk.Application):
    def __init__(self, *args, **kwargs):
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

        action = Gio.SimpleAction.new("save_file", None)
        action.connect("activate", self.save_file)
        self.add_action(action)

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = C4OWindow("","Untitled Document",application=self, title="Main Window")

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
            # get the file name
            file_name = file_path.split("/")[-1]
            # delete the dialog
            dialog.destroy()
            # create a new window and destroy the previous
        
            self.window.hb.props.title = " - 213"
            # self.window.createNewWindow(file_path,file_name)
            # self.window.destroyWindow()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
            dialog.destroy()

    def save_file(self,action,param):
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
            # get the file name
            file_name = file_path.split("/")[-1]

            # delete the dialog
            dialog.destroy()
            # create a new window and destroy the previous
            self.window.createNewWindow(file_path,file_name)
            self.quit()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
            dialog.destroy()

    def on_about(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self.window)
        # add text to the about dialog
        about_dialog.set_program_name("C4O")
        about_dialog.set_version("0.1")
        about_dialog.set_authors(["Lionis Emmanouil Georgios(Akis)","Tsalapati Eleni","Koubarakis Manolis"])
        # set no icon for the about dialog
        about_dialog.set_logo_icon_name(None)
        about_dialog.set_comments("A simple ontology editor that uses communication with a chatbot to help the user create ontologies.")
        about_dialog.present()

    def on_quit(self, action, param):
        self.quit()


if __name__ == "__main__":
    app = C4OApplication()
    app.run(sys.argv)


# https://lazka.github.io/pgi-docs/Gtk-3.0/classes/Stack.html
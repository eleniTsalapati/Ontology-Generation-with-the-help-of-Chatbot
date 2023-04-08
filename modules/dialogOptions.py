import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class RadioDialog(Gtk.Dialog):
    def __init__(self, parent,options,header):
        Gtk.Dialog.__init__(self, header, parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        parent.addTextChatBot(header)
        self.set_default_size(150, 100)
        self.selected_option = None
        # Create a box to hold the radio buttons
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.get_content_area().add(box)
        previousButton=None
        buttons=[]
        i=0
        for option in options:
            buttons.append(Gtk.RadioButton.new_with_label_from_widget(previousButton,option))
            buttons[i].connect("toggled", self.on_button_toggled, option)
            box.pack_start(buttons[i], False, False, 0)
            if previousButton==None:
                previousButton=buttons[i]
                self.selected_option=option
            i+=1
        self.show_all()

    def on_button_toggled(self, button, name):
        if button.get_active():
            self.selected_option = name

    def run(self):
        Gtk.Dialog.run(self)
        self.destroy()

        return self.selected_option

class CheckDialog(Gtk.Dialog):
    def __init__(self, parent, options,header):
        self.parent=parent
        Gtk.Dialog.__init__(self, header, parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        parent.addTextChatBot(header)
        self.set_default_size(200, 200)
    
        self.selected_options = []
        # Create a box to hold the check buttons
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.get_content_area().add(box)


        # Create the check buttons and add them to the box
        for option in options:
            button = Gtk.CheckButton.new_with_label(option)
            button.get_child().props.wrap=True
            button.connect("toggled", self.on_button_toggled, option)
            box.pack_start(button, False, False, 0)


        self.show_all()

    def on_button_toggled(self, button, name):
        if button.get_active():
            self.selected_options.append(name)
        else:
            self.selected_options.remove(name)

    def run(self):
        Gtk.Dialog.run(self)
        self.destroy()
        return self.selected_options
    
class SaveDialog(Gtk.Dialog):

    def __init__(self, parent,autosave=""):
        Gtk.Dialog.__init__(self, autosave+"Save Changes?", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_SAVE, Gtk.ResponseType.YES))

        self.set_default_size(150, 100)

        label = Gtk.Label("Do you want to save changes?")
        box = self.get_content_area()
        box.add(label)
        self.show_all()

class TextDialog(Gtk.Dialog):

    def __init__(self, parent, header):
        Gtk.Dialog.__init__(self, header, parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(200, 100)

        # Create an entry widget and add it to the dialog
        self.entry = Gtk.Entry()
        self.entry.set_text("")
        self.entry.connect("activate", self.on_entry_activate)
        box = self.get_content_area()
        box.add(self.entry)

        self.show_all()

    def get_text(self):
        return self.entry.get_text()

    def on_entry_activate(self, widget):
        self.response(Gtk.ResponseType.OK)

    def run(self):
        response = Gtk.Dialog.run(self)
        text=""
        if response == Gtk.ResponseType.OK:
            text= self.get_text()
        self.destroy()
        return text
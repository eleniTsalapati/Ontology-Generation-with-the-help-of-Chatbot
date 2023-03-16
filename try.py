import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class RadioDialog(Gtk.Dialog):

    selected_option = None

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Radio Dialog", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        # Create a box to hold the radio buttons
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.get_content_area().add(box)

        # Create the radio buttons and add them to the box
        button1 = Gtk.RadioButton.new_with_label_from_widget(None, "Option 1")
        button1.connect("toggled", self.on_button_toggled, "Option 1")

        button2 = Gtk.RadioButton.new_with_label_from_widget(button1, "Option 2")
        button2.connect("toggled", self.on_button_toggled, "Option 2")

        button3 = Gtk.RadioButton.new_with_label_from_widget(button1, "Option 3")
        button3.connect("toggled", self.on_button_toggled, "Option 3")

        box.pack_start(button1, False, False, 0)
        box.pack_start(button2, False, False, 0)
        box.pack_start(button3, False, False, 0)

        self.show_all()

    def on_button_toggled(self, button, name):
        if button.get_active():
            self.selected_option = name

    def run(self):
        response = Gtk.Dialog.run(self)

        if response == Gtk.ResponseType.OK:
            print("Option {} selected!".format(self.selected_option))
        else:
            print("Dialog closed")

        self.destroy()

        return self.selected_option


dialog = RadioDialog(None)
selected_option = dialog.run()
print("Selected option: {}".format(selected_option))

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class C4OWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # window properties
        #
        self.set_border_width(10)
        self.set_default_size(400, 200)

        # headerbar
        #
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "C4O"
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

        # app content
        #

        # TODO: ADD A VERTICAL BOX WIDGET IN THE WINDOW (self.add)
        #       ADD A TEXT VIEW IN THE VERTICAL BOX AND MAKE IT READ-ONLY (Gtk.TextView.props.editable)
        #       ADD AN ENTRY IN THE VERTICAL BOX
        #       MAKE IT SO EVERYTHING YOU WRITE IN THE ENTRY APPEARS IN THE TEXTVIEW (like a chat) (Gtk.Entry.signals.activate)

        self.show_all()

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class TreeViewWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="TreeView Hover Example")

        self.store = Gtk.TreeStore(str, str, str)
        row1=self.store.append(None, ["Child", "This is the description for Item 1", "The child are:None\n The Parents are: Parent,GrandParent"])
        row2=self.store.append(None, ["Parent", "This is the description for Item 2", "The child are:Child\n The Parents are: GrandParent"])
        row3=self.store.append(None, ["GrandParent", "This is the description for Item 3", "The child are:Child,Parent\n The Parents are:None"])
        self.store.append(row1, ["Parent: Parent","",""])
        self.store.append(row1, ["Parent: GrandParent","",""])
        self.store.append(row2, ["Child: child","",""])
        self.store.append(row2, ["Parent: GrandParent","",""])
        self.store.append(row3, ["Child: child","",""])
        self.store.append(row3, ["Child: Parent","",""])

        self.treeview = Gtk.TreeView(self.store)
        self.treeview.set_tooltip_column(2)
        self.treeview.set_hover_selection(True)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Title", renderer, text=0)
        self.treeview.append_column(column)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Description", renderer, text=1)
        self.treeview.append_column(column)
        
        # # Create the TreeView
        # self.treeview = Gtk.TreeView()
        # self.treeview.set_hover_selection(True)

        # # Create the TreeView columns
        # renderer = Gtk.CellRendererText()
        # column = Gtk.TreeViewColumn("Title", renderer, text=0)
        # self.treeview.append_column(column)

        # renderer = Gtk.CellRendererText()
        # column = Gtk.TreeViewColumn("Description", renderer, text=1)
        # self.treeview.append_column(column)

        # # Add the data to the TreeView
        # self.liststore = Gtk.ListStore(str, str,str)
        # self.liststore.append(["Item 1", "This is the description for Item 1", "This is the helper for Item 1"])
        # self.liststore.append(["Item 2", "This is the description for Item 2", "This is the helper for Item 2"])
        # self.treeview.set_model(self.liststore)

        # self.treeview.set_tooltip_column(2)

        # Create a tooltip and set the tooltip for the TreeView for only the first row
        
        # Add the TreeView to the window
        self.add(self.treeview)

        # self.liststore.append(["Item 3", "This is the description for Item 3", "This is the helper for Item 3"])

win = TreeViewWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

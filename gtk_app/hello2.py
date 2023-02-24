# TreeStore
import gi           
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MainWindow(Gtk.Window):
    """docstring for ClassName"""
    def __init__(self):
        
        Gtk.Window.__init__(self,title="peple finder")
        self.set_title("TreeView with TreeStore")
        self.set_size_request(400,200)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        vbox = Gtk.VBox(False,5)
        
        # TreeStore with one column
        store = Gtk.TreeStore(str)
        
        # Name1 row
        row1 = store.append(None,['Name1'])
        
        # Add child to the row
        store.append(row1,['Age1'])
        store.append(row1,['Profesion1'])
        
        # Name2 row
        row2 = store.append(None,['Name2'])
        
        # Add child to the row
        store.append(row2,['Age2'])
        store.append(row2,['Profesion2'])
        
        
        #TreeView is the item that is displayed
        treeview = Gtk.TreeView(store)
        tvcolumn = Gtk.TreeViewColumn('GUI Toolkits')
        treeview.append_column(tvcolumn)
        
        cell_editable = Gtk.CellRendererText()
        cell_editable.set_property("editable",True)
        
        cell_editable.connect("edited", self.text_edited)
        
        tvcolumn.pack_start(cell_editable,True)
        tvcolumn.add_attribute(cell_editable,'text',0)
        
        vbox.add(treeview)
        self.add(vbox)

    def text_edited(self, widget, text):
        self.store = text

window = MainWindow()
window.connect("delete-event",Gtk.main_quit)
window.show_all()
Gtk.main() 
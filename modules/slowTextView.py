import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import modules.log as log

class SlowTextView(Gtk.TextView):

    def __init__(self):
        Gtk.TextView.__init__(self)
        self.text = ""
        self.current_pos = 0
        self.timeout_id = None
        self.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)  # Set wrap-mode to WORD_CHAR
        self.set_editable(False)  # Set editable to False
        self.set_cursor_visible(False)  # Set cursor_visible to False
        self.remember="ChatBot:\n\t"
    def rememberOneTime(self,text):
        self.remember+=text
    
    def add_text(self,text,add_delay=100):
        if self.remember!="ChatBot:\n\t":
            self.add_text_Remember(self.remember,50)
        self.add_text_Normal(text,50)
        self.remember="ChatBot:\n\t"
    
    # add text to the previous text slowly
    def add_text_Normal(self, text, add_delay=100):
        # scroll to the end of the text
        self.scroll_to_iter(self.get_buffer().get_end_iter(), 0.0, False, 0.0, 0.0)
        # if the previous text does not change line
        if self.text!="" and self.text[-1] != '\n':
            # add a space
            self.text = self.text + '\n'
        # add text to the previous text
        self.text = self.text + text
        log.addToLog(text)
        self.set_sensitive(False)
        self.start(add_delay)
    
    def add_text_Remember(self, text, add_delay=100):
        # scroll to the end of the text
        self.scroll_to_iter(self.get_buffer().get_end_iter(), 0.0, False, 0.0, 0.0)
        # if the previous text does not change line
        if self.text!="" and self.text[-1] != '\n':
            # add a space
            self.text = self.text + '\n'
        # add text to the previous text
        self.text = self.text + text
        log.addToLog(text)
        self.set_sensitive(False)
        self.start(add_delay)
    def start(self,add_delay):
        # Start adding text one character at a time
        self.timeout_id = GLib.timeout_add(add_delay, self._add_char)

    def stop(self):
        # Stop adding text
        if self.timeout_id is not None:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
            self.set_sensitive(True)

    def _add_char(self):
        # Add the next character to the text buffer
        if self.current_pos < len(self.text):
            # if it is not scrolled to the end, scroll to the end
            if self.get_vadjustment().get_value() != self.get_vadjustment().get_upper() - self.get_vadjustment().get_page_size():
                self.scroll_to_iter(self.get_buffer().get_end_iter(), 0.0, False, 0.0, 0.0)

            self.get_buffer().insert_at_cursor(self.text[self.current_pos])
            self.current_pos += 1
            return True
        else:
            self.stop()
            return False
    

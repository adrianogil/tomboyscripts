'''
Created on Mar 11, 2010

@author: adriano
'''
import dbus, time, datetime 
        
BUS_NAME = 'org.gnome.Tomboy'
OBJ_PATH = '/org/gnome/Tomboy/RemoteControl'
IFACE_NAME = 'org.gnome.Tomboy.RemoteControl'

class RemoteControl:
    def __init__(self):
        bus = dbus.SessionBus()
        obj = bus.get_object(BUS_NAME,OBJ_PATH)
        self.remote = dbus.Interface(obj,IFACE_NAME)
        
    def version(self):
        return self.remote.Version()
        
    def open_search(self,text=None):
        if text:
            self.remote.DisplaySearchWithText(text)
        else:
            self.remote.DisplaySearch()
            
    def open_note(self, uri):
        self.remote.DisplayNote(uri)

    def open_named_note(self, name, search=None):
        uri = self.remote.FindNote(name)
        if search:
            self.remote.DisplayNoteWithSearch(uri, search)
        else:
            self.remote.DisplayNote(uri)

    def create_note(self, name=None):
        if name:
            new_uri = self.remote.FindNote(name)
        
            if (not new_uri) or new_uri == "":
                new_uri = self.remote.CreateNamedNote(name)
        else:
            new_uri = self.remote.CreateNote()
        return new_uri
            
    def delete_note(self, uri):
        return self.remote.DeleteNote(uri)
        
    def note_exists(self, uri):
        return self.remote.NoteExists(uri)
        
    def list_all_notes(self, title=False):
        results = self.remote.ListAllNotes()
        
        if title:
            tmp = []
            for uri in results:
                tmp.append(self.get_note_title(uri))
            results = tmp
            
        return results

    def get_note_title(self, uri):
        return self.remote.GetNoteTitle(uri)

    def get_note_contents(self, uri):
        return self.remote.GetNoteContents(uri)
    
    def get_note_contents_xml(self, uri):
        return self.remote.GetNoteContentsXml(uri)
        
    def set_note_contents(self, uri, text):
        max = 5
        while self.get_note_contents(uri) != text and max > 0:
            self.remote.SetNoteContents(uri, text)
            time.sleep(1)
            max = max - 1
#        print instance.get_note_contents(new_note)
        
    def set_note_contents_xml(self, uri, xml):
        return self.remote.SetNoteContentsXml(uri, xml)
        
    def get_note_create_date(self, uri):
        return datetime.datetime.fromtimestamp(self.remote.GetNoteCreateDate(uri))
        
    def get_note_change_date(self, uri):
        return datetime.datetime.fromtimestamp(self.remote.GetNoteChangeDate(uri))
        
#if __name__ == "__main__":
#    instance = RemoteControl()
#    for i in instance.list_all_notes():
#        print i
#        print instance.get_note_title(i)
#        print instance.get_note_change_date(i)
        
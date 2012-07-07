'''
Created on Mar 10, 2010

@author: adriano
'''

import dbus, gobject, dbus.glib, time, TomboyRemoteControl


class Tomboy:
    def createNote(self, title, contents):
        tomboy = TomboyRemoteControl.RemoteControl()
        new_note = tomboy.create_note(title)
        tomboy.open_note(new_note)
        tomboy.set_note_contents(new_note, contents)
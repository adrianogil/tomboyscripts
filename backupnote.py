import datetime, sys
import TomboyManager
import TomboyRemoteControl
import commands

mainpath = '/home/adriano/Documents/BackupTomboy/'

print 'Arguments received: ',sys.argv

if len(sys.argv) == 3:
    tomboyNoteTitle= sys.argv[1]
    dateBackup = sys.argv[2]

    print 'Searching for  %s note on folder %s' % (tomboyNoteTitle, dateBackup)

#    now = datetime.datetime.now().date()
#    while int(now.day()) != int(dateBackup):
#        now = now - datetime.timedelta(1)

    path = mainpath + 'BackupDay_' + dateBackup
    r = TomboyManager.findNote(tomboyNoteTitle, path)
    if r[0]:
         print r[1]
         contents = commands.getoutput('cat ' + r[1])
         n = TomboyManager.findNote(tomboyNoteTitle)
         if n[0]:
             print n[1]
             note = open(n[1],'wb' )
             note.write(contents)
             note.close()
#             tomboy = TomboyRemoteControl.RemoteControl()
#             tomboy.open_named_note(tomboyNoteTitle)

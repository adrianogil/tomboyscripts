'''
Created on Mar 8, 2010

@author: adriano
'''

import os, glob, commands, xml.dom.minidom, TomboyManager, sys

if len(sys.argv) > 1:
    argsNotes = sys.argv[1]
#    print argsNotes
    if argsNotes == 'p':
        # First Quest: Sync the Planning note about the current day with my N810
        TomboyManager.syncTodayPlanningNote2N810()
    elif argsNotes == 'f':
        # Creating the notes of 'Le Mot: %s' based on the today 'Mots du Jour'
        TomboyManager.searchMotsDuJour()
    elif argsNotes == 'a':
	#Transfer all notes
	TomboyManager.syncAllNotes2N810()
else:
    print ' Usage: manageTomboyNotes [OPTION] ' 
            
            
            
            
            

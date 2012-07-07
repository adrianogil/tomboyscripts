#!/usr/bin/env python
'''
Created on Apr 27, 2011

@author: Adriano
'''
import datetime, commands

# Get the backup folder name according current date
now = datetime.datetime.now()
day = now.day

backupMainFolder = '/home/adriano/Documents/BackupTomboy/BackupDay_' + str(day)
pathTomboyNotes = '/home/adriano/.local/share/tomboy'

# Just copy files
print commands.getoutput(" mkdir -p "  + backupMainFolder)
print commands.getoutput(" cp -r "  + pathTomboyNotes + "/*  "  + backupMainFolder)

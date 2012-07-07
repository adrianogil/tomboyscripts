#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Mar 8, 2010

@author: adriano
'''

import os, glob, commands, xml.dom.minidom, datetime, re, locale
from xml.dom.minidom import Node
import urllib
from Tomboy import Tomboy

# Configuration Values
n810_ip = "192.168.0.100"
n810_path = "/home/user/.conboy"
n810_backup = "/home/user/ConboyBackup"
pathTomboyNotes = '/home/adriano/.local/share/tomboy'
my_sshkey_path = "/home/adriano/Security/Gil"

def getTitle(file):
    title = ''
    if os.stat(file).st_size != 0:
        doc = xml.dom.minidom.parse(file)
        for node in doc.getElementsByTagName('note'):
            node2 = node.getElementsByTagName('title')
            for n in node2:

                for node3 in n.childNodes:
                    if node3.nodeType == Node.TEXT_NODE:
                        title += node3.data
    return title

def getNoteList(file):
    list = []
    doc = xml.dom.minidom.parse(file)
    for node in doc.getElementsByTagName('note'):
        node2 = node.getElementsByTagName('text')
        for n in node2:
            for n2 in n.getElementsByTagName('note-content'):
                for n3 in n2.getElementsByTagName('list'):
                    for n4 in n3.getElementsByTagName('list-item'):
                        dataList = ''
                        for node3 in n4.childNodes:
                            if node3.nodeType == Node.TEXT_NODE:
                                dataList += node3.data
                        list += [dataList]
    return list

def getTitleUsingGrep(file):
    title = commands.getoutput('cat ' + file + '| grep "<title>"')
    if title != "":
        print "current file has the title: " + title
    else: print "Can't read the title of " + file

def syncTodayPlanningNote2N810():
    ''' Sync with N810. Transfer the Today Planning Note '''
    print '\nSearching for the Today Planning Note\n'
    title = ""
    found = False
    for infile in glob.glob( os.path.join(pathTomboyNotes, '*.note') ):
        #print 'Getting title via XML Parsing: ' + getTitle(infile)
        title = getTitle(infile)
        today = datetime.date.today()
        current_title = "Planning the day " + today.strftime("%Y.%m.%d")
        if title == current_title:
            found = True
            print 'I found the Planning Note for Today'
            if raw_input('Do you want to see the contents of the file? (Y/N) ') == 'Y':
                print commands.getoutput('cat ' + infile)
            if raw_input('Do you want to sync with your N810? ') == 'Y':
                # Backup the old notes
                commands.getoutput("ssh -i " + my_sshkey_path + " root@" + n810_ip + " cp " + n810_path + "/* " + n810_backup)
                commands.getoutput("scp -i " + my_sshkey_path + " " + infile + " root@" + n810_ip + ":" + n810_path + "/")
                print 'Completed Successfully!'
    if not found:
        print 'Sorry, but I didn\'t find the Planning Note for Today'
    return found

def syncAllNotes2N810():
	''' Sync with N810. Transfer all Notes '''
	# Backup the old notes
	print commands.getoutput("ssh -i " + my_sshkey_path + " root@" + n810_ip + " mv " + n810_path + "/* " + n810_backup)
	print commands.getoutput("scp -i " + my_sshkey_path + " " + pathTomboyNotes + "/* root@" + n810_ip + ":" + n810_path + "/")
	print 'Completed Successfully!'

def findNote(title,path = pathTomboyNotes):
    ''' Find the filename of a note by its title '''
    print path
    found = False
    path_file = ''
    for infile in glob.glob( os.path.join(path, '*.note') ):
#        print 'Getting title via XML Parsing: ' + getTitle(infile)
        title_found = getTitle(infile)
        if title_found == title:
            found = True
            path_file = infile
            break
    return [found, path_file]

def parseMotsMeaning(meaning, word):
    print 'Got that meaning :'
    if meaning.find("Aucun mot trouvé") != -1 or meaning.find("Résultat de la recherche:") != -1:
        # Didn't found the world
        print 'No meaning found'
        return [False]
    else:
        print meaning

        dict_meaning = {}
        parse_success = False
        # Find out the type of the word
        print word.replace('É','é')
        find_type_world = re.findall(r"Définition du mot :\s*" + word.lower() + "\s*[\>é\w\s]*.puce.", meaning)
        print 'Parsing Results 1'
        print find_type_world
        print 'Finish Parsing 1'
#        print 'Parsing Results 2'
#        find_type_world = re.findall(r"\n[ é\w]*\n\s*\[", find_type_world[0])
#        if len(find_type_world) > 0:
#            parse_success = True
#            find_type_world[0] = find_type_world[0][0:(len(find_type_world[0])-1)]
#            print find_type_world[0].strip()
#            # Found grammatical class of the world
#            type_world = find_type_world[0].strip()
#            dict_meaning['type'] = type_world
#            print 'Finish Parsing 2'
#            print 'Parsing Results 3'
#            definition_list = []
#            for definition in re.findall(r'\[puce\].*\n', meaning):
#                mot_definition = definition[6:].strip()
#                print 'Definition:', mot_definition
#                definition_list += [mot_definition]
#            dict_meaning['list_definition'] = definition_list
#            print 'Finish Parsing 2'
#
#        return [True, parse_success, dict_meaning]

def generateNoteContents2NoteFR(results, title):
    contents = title
    contents += "\n\n"
    for x in results['list_definition']:
        contents += " - " + x + "\n"
    return contents

def getXmlList(results, title):
    xmlList = "<list><list-item dir=\"ltr\">" + results['type'] + "<list>"
    for x in results['list_definition']:
        xmlList += "<list-item dir=\"ltr\">" + x + "</list-item>"
    xmlList += "</list></list-item><\list>"

    totalxml = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    totalxml += "<note version=\"0.3\" xmlns:link=\"http://beatniksoftware.com/tomboy/link\" "
    totalxml += "xmlns:size=\"http://beatniksoftware.com/tomboy/size\""
    totalxml += "xmlns=\"http://beatniksoftware.com/tomboy\">"
    totalxml += "<title>" + title + "</title>"
    totalxml += "<text xml:space=\"preserve\"><note-content version=\"0.1\">" + title + "\n\n" + xmlList
    totalxml += "</note-content></text>"
    totalxml += "<last-change-date>2010-03-10T17:29:52.2448190-04:00</last-change-date>"
    totalxml += "<last-metadata-change-date>2010-03-10T17:29:52.2448190-04:00</last-metadata-change-date>"
    totalxml += "<create-date>2010-03-10T08:35:11.6179920-04:00</create-date>"
    totalxml += "<cursor-position>65</cursor-position>"
    totalxml += "<width>450</width>"
    totalxml += "<height>360</height>"
    totalxml +=  "<x>665</x>"
    totalxml += "<y>247</y>"
    totalxml += "<tags>"
    totalxml += "<tag>system:notebook:French</tag>"
    totalxml += "</tags>"
    totalxml += "<open-on-startup>False</open-on-startup>"
    totalxml += "</note>"
    return totalxml


def getTodayNoteTitle():
    now = datetime.datetime.now()
    month = now.month
    if month < 10:
        month = '0' + str(month)
    else:
        month = str(month)
    day = now.day
    if day < 10:
        day = '0' + str(day)
    else:
        day = str(day)
    title = str(now.year) + '.' + month + '.' + day
    return title

def searchMotsDuJour():
    ''' Follow these steps:
            1 - Find the note "Mot du jour %Date"
            2 - Find inside that note the list of "Le Mot: %s"
            3 - Using the w3m and cat commands to grab the meaning of each word
            4 - Create note "Le Mot: %s"
            5 - Overwrite each new note with the respectiv result
    '''

    # 1 - Find the note "Mot du jour %Date"
    print '\nSearching for the today \'Mots du Jour\'\n'
    current_title = "Mots du Jour " + getTodayNoteTitle()
    find_note = findNote(current_title)
    if not find_note[0]:
        print 'I didn\'t find the note', current_title
    else:
        print 'I found the note', current_title
        if raw_input('Do you want to see the contents of the file? (Y/N) ') == 'Y':
                print commands.getoutput('cat ' + find_note[1])
        # Find inside that note the list of "Le Mot: %s"
        print '\nTrying to get the list of mots from that note:\n'
        list_Mots_du_Jour = getNoteList(find_note[1])
        print 'Current list Mots du Jour', list_Mots_du_Jour
        for mot in range(len(list_Mots_du_Jour)):
            list_Mots_du_Jour[mot] = (list_Mots_du_Jour[mot][8:])
        print 'Current list Mots du Jour', list_Mots_du_Jour[1]
        # Using the w3m and cat commands to grab the meaning of each word
        print list_Mots_du_Jour
        for mot in list_Mots_du_Jour:
            print mot.encode('utf-8')
            mot = mot.strip()
            url = "http://www.le-dictionnaire.com/definition.php?mot=" + urllib.quote(mot.encode('latin-1'))
            print url
            meaning = commands.getoutput("w3m \'" + url + "\'")
            results = parseMotsMeaning(meaning, mot.encode('utf-8'))
#            if not results[0]:
#                print 'I didn\'t found the world', mot
#            elif results[1]:
#                # Create note "Le Mot: %s"
#                title = "Le Mot: " + mot.encode('utf-8')
#                tomboy = Tomboy()
#                contents = generateNoteContents2NoteFR(results[2], title)
#                tomboy.createNote(title, contents)

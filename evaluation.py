#!/usr/bin/python3
import json
import sys
import os
import pickle
from random import randint

# Base dir
sBaseDir="events_out"

sUsername = (input("Please, enter a username (used to anonymously identify you across sessions\n")).strip().lower()
if sUsername == "":
    sUsername = str(abs(randint(0,1000)))
    print("Assigning random name: %s"%(sUsername))
print("\nImportant: Please note down the name to reuse if needed!")

aLastSession = []
aVisitedIds = []
# TODO: Load data
sLastSessionFilename = "lastSession.pickle"
if os.path.isfile(sLastSessionFilename):
    try:
        with open(sLastSessionFilename, 'rb') as sessionFile:
            aLastSession = pickle.load(sessionFile)
            print("Previous session loaded...")
    except Exception as e:
        print("Could not load previous session. Error:\n%s\nIgnoring..."%(str(e)))

# See if this user has alread evaluated this
aVisitedIds = [tCurEvaluation[1] for tCurEvaluation in aLastSession if tCurEvaluation[0] == sUsername]

# For every file in dir
aAllFiles = os.listdir(sBaseDir)
# Sort filenames using Python to make sure they're the same order in all OSes
aAllFiles.sort()

print("+++ Found %d event files" % (len(aAllFiles)))
for sFile in aAllFiles:
    with open(sBaseDir + "/" + sFile, "rb") as fCur:
        # Read event JSON
        event=json.load(fCur)
    # Get data for event
    sId = event['id']
    sTitle = event['title']

    if sId in aVisitedIds:
        print("+ Ignoring article with id %s and title \"%s\", because the user has already evaluated it..."%(sId, sTitle.strip()))
        continue


    print("+++  Next event (ID %s) - %d left to go!" % (sId, len(aAllFiles) - len(aLastSession)))
    lArticles = event['articles']
    # Display articles
    print("++ Please check the following %d articles:"%(len(lArticles)))
    for idx, sArticle in enumerate(lArticles):
        print("+ -----%d\n"%(idx) + sArticle['content'][:500] + "\n+ -----%d\n"%(idx))
    # Ask whether they appear to represent a single event
    bSingleEvent = ""
    while (bSingleEvent == "") or (str(bSingleEvent).upper() not in ['Y', 'N']):
        bSingleEvent = input("Do the above articles appear to represent a single event? (please answer [Y]es / [N]o) \n")
    sSingleEvent = str(bSingleEvent).upper()
    # Ask how many articles are irrelevant
    sIrrelevant = ""
    iIrrelevants = list()
    while (sIrrelevant == ""):
        sIrrelevant = input("Which articles do you feel are irrelevant to the others? (please answer by giving the article numbers separated by commas, e.g.: 1,3,6 or - for none) \n")
        
        # If user found no irrelevant articles...
        if sIrrelevant == "-":
          break
        
        # User might have found irrelevant articles
        try:
            given_ids = sIrrelevant.split(",")
            
            for idIrr in given_ids:
              iIrrelevant = int(idIrr.strip())
              iIrrelevants.append(iIrrelevant)
              if (iIrrelevant < 0) or (iIrrelevant > len(lArticles) - 1):
                  sIrrelevant = ""
        except:
            iIrrelevants = list()
            sIrrelevant = ""

    # Ask how well the title represents the event (1-3)
    sTitleRepresentsWell = ""
    aOptions = ['B', 'O', 'W']
    while (sTitleRepresentsWell == "") or (str(sTitleRepresentsWell).upper() not in aOptions):
        sTitleRepresentsWell = input("How well do you believe the following title reflects the event? \n%s\n (please answer [B]adly / [O]K / [W]ell enough)\n"%(sTitle))
    iTitleRepresentsWell =  aOptions.index(str(sTitleRepresentsWell).upper())

    aLastSession.append((sUsername, sId, sTitle, sSingleEvent, iIrrelevants, sTitleRepresentsWell))
    # Save current state
    with open(sLastSessionFilename, 'wb') as sessionFile:
        pickle.dump(aLastSession, sessionFile, pickle.HIGHEST_PROTOCOL)
        print("+ Session saved!")

    print("+++  Thank you! (ID %s)" % (sId))

#!/usr/bin/python3
import os
import pickle
import hashlib
import json
import sys

if len(sys.argv) > 0:
    sLastSessionFilename = sys.argv[1]
else:    
    sLastSessionFilename = "lastSession.pickle"
sOutputFile = "out.csv"
# Base dir
sBaseDir="events_out"

# Read event sizes from files
dEventSizes= {}
# For every file in dir
aAllFiles = os.listdir(sBaseDir);
# Sort filenames using Python to make sure they're the same order in all OSes
aAllFiles.sort()

print("+++ Found %d event files" % (len(aAllFiles)))
for sFile in aAllFiles:
    with open(sBaseDir + "/" + sFile, "rb") as fCur:
        # Read event JSON
        event=json.load(fCur)
    # Get data for event
    sId = event['id']
    lArticles = event['articles']
    dEventSizes[sId] = len(lArticles)

if os.path.isfile(sLastSessionFilename):
    try:
        with open(sLastSessionFilename, 'rb') as sessionFile:
            aLastSession = pickle.load(sessionFile)
            print("Previous session loaded...")

            with open(sOutputFile, "wt") as fOutFile:
                # Add header
                print("userId,eventId,singleEventDescribed,listOfIrrelevantArticles,totalArticles,titleRepresentativeness"
                      , file=fOutFile
                      )
                # for each line
                for tTuple in aLastSession:
                    # Get fields
                    (sUsername, sId, sTitle, sSingleEvent, lIrrelevant, sTitleRepresentsWell) = tTuple
                    aOptions = ['B', 'O', 'W']
                    # Get numeric quality indication from categorical
                    iTitleRepresentsWell = aOptions.index(str(sTitleRepresentsWell).upper())
                    # Output to file
                    print("%s,%s, %s, \"%s\", %d, %d"%(str(hashlib.md5(sUsername.encode('utf8')).hexdigest()), sId, sSingleEvent, str(lIrrelevant), dEventSizes[sId], iTitleRepresentsWell)
                          , file=fOutFile
                          )
    except Exception as e:
        print("Could not load previous session. Error:\n%s\nQuitting..."%(str(e)))
else:
    print("Session file not found. Quitting.")

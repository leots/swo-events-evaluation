#!/usr/bin/python3
import os
import pickle
import hashlib
import json

sLastSessionFilename = "lastSession.pickle"
sOutputFile = "out.csv"
# Base dir
sBaseDir="events_out"

# Read event sizes from files
dEventSizes= {}
# For every file in dir
aAllFiles = os.listdir(sBaseDir);
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
                print("userId,eventId,singleEventDescribed,numOfIrrelevantArticles,totalArticles,titleRepresentativeness"
                      , file=fOutFile
                      )
                # for each line
                for tTuple in aLastSession:
                    # Get fields
                    (sUsername, sId, sTitle, sSingleEvent, iIrrelevants, sTitleRepresentsWell) = tTuple
                    print(iIrrelevants)
                    iIrrelevants.sort()
                    sIrrelevants = ",".join([str(irr) for irr in iIrrelevants])
                    print(sIrrelevants)
                    aOptions = ['B', 'O', 'W']
                    # Get numeric quality indication from categorical
                    iTitleRepresentsWell = aOptions.index(str(sTitleRepresentsWell).upper())
                    # Output to file
                    print("%s,%s, %s, \"%s\", %d, %d"%(str(hashlib.md5(sUsername.encode('utf8')).hexdigest()), sId, sSingleEvent, sIrrelevants, dEventSizes[sId], iTitleRepresentsWell)
                          , file=fOutFile
                          )
    except Exception as e:
        print("Could not load previous session. Error:\n%s\nQuitting..."%(str(e)))
else:
    print("Session file not found. Quitting.")
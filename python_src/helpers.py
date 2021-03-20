from datetime import datetime
import numpy as np
import re

entityTypes = ["PERSON", "LOCATION", "ORGANIZATION", "MISC", "MONEY", "NUMBER", 
    "ORDINAL", "PERCENT", "DATE", "TIME", "DURATION", "SET", "EMAIL", "URL", "CITY", 
    "STATE_OR_PROVINCE", "COUNTRY", "NATIONALITY", "RELIGION", "TITLE", "IDEOLOGY", 
    "CRIMINAL_CHARGE", "CAUSE_OF_DEATH", "HANDLE"]

# coverts a datetime string with format "YYYY-MM-DDTHH:MM:SS.ms" to a UNIX timestamp
def sotimeToTimestamp(datetimestr):
   parts = datetimestr.split("T")
   date = parts[0]
   time = parts[1]

   dateparts = date.split("-")
   year = int(dateparts[0])
   month = int(dateparts[1])
   day = int(dateparts[2])

   timeparts = time.split(":")
   hour = int(timeparts[0])
   minute = int(timeparts[1])
   secNms = timeparts[2]

   sec = int(secNms.split(".")[0])
   ms = int(secNms.split(".")[1])

   dt = datetime(year,month,day,hour,minute,sec,ms*1000)
   return datetime.timestamp(dt)

# THIS FUNCTION CAN BE EXPANDED TO INCLUDE ANY FUTURE ADDITIONAL PREPROCESSING NEEDED FOR THE STRING
def convertStringToNER(string, client):
    string = cleanXML(string)
    ann = client.annotate(string)
    nerVector = buildNERVector(ann)
    return nerVector

# builds an NER occurences vector from an annotation
def buildNERVector(ann):
    nerVector = np.zeros(24)
    sentences = ann.sentence

    for sent in sentences:
        tokens = sent.token
        for tok in tokens:
            if tok.ner != 'O':
                index = entityTypes.index(tok.ner)
                nerVector[index] += 1

    return nerVector


"""
you need to think this through, but I suggest this might be something to consider:
- popularity = 0,1-2,3-5,5-10,10-50,50+
- notoriety = 0,1-2,3-5,5-10,10-50,50+
- edit_activity = 1min_ago,1hour_ago,1day_ago,1week_ago,ages_ago,never
 
the you have:
"""

# takes a feature that has a numeric representation and returns a range binned representation based on the thresholds passed in
# If for example the thresholds list pased in is [0,2,5,10,20,50] then it is binned into [0, 1-2, 3-5, 6-10, 11-20, 21-50]
def range_bin_num_feature(num, thresholds):
    rbinvec = np.zeroes(len(thresholds)+ 1)
    inRange = False
    for i in range(len(thresholds)):
        if num > thresholds[i]:
            continue
        else:
            rbinvec[i] = 1
            inRange = True
    
    if not inRange:
        rbinvec[-1] = 1

    return rbinvec
    



# basic naive regex xml tag remover
def cleanXML(string):
    return re.sub('<.*?>', '', string)

def flatten(listofLists):
    return [item for sublist in listofLists for item in sublist]
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


# basic naive regex xml tag remover
def cleanXML(string):
    return re.sub('<.*?>', '', string)

def flatten(listofLists):
    return [item for sublist in listofLists for item in sublist]
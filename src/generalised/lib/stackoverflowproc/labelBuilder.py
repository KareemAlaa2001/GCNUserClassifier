# from lib.stackoverflowproc.extraction import recentComments, recentPosts, recentUsers
from os import O_NOFOLLOW
import xml.etree.ElementTree as ET
import html5lib
# from html5_parser import parse
# This module will have functions for the implementations of different types of labels. Some will be dependent on the data I've extracted, 
# while others will be based on other stuff extracted from the website
from selenium import webdriver


# function to get the label of a user according to diamond mod status ( sheriff badgeholders )


def getSheriffBadgeUserIds(users):
    sheriffNames = getSheriffBadgeDisplayNames()
    namesToIds = {}
    for user in users:
        userDisName = user.get('DisplayName')

        if userDisName in sheriffNames:
            if namesToIds.get(userDisName) is not None:
                idlist = namesToIds.get(userDisName)
                idlist.append(user.get('Id'))
                namesToIds[userDisName] = idlist

            else:
                namesToIds[userDisName] = [user.get('Id')]

    namesToIds["Kev"] = ['419']
    namesToIds["Max"] = ['189572']

    idList = []

    for name in namesToIds:
        idList.append(namesToIds.get(name)[0])

    return idList

        
def buildUserLabelsDict(users, indexGuide, sheriffIds):
    labelDict = {}

    for user in users:
        userid = user.get('Id')
        userIndex = indexGuide.get('user').get(userid)
        
        if userid in sheriffIds:
            # print("userid", userid, "was found to be a sheriff, adding +ve label for index", userIndex)
            labelDict[userIndex] = [1,0]
        
        else:
            labelDict[userIndex] = [0,1]

    return labelDict

def buildAllLabelsDict(indexGuide, userLabels, labelLength):
    allLabels = {}

    for nodetype in indexGuide:
        for nodeid in indexGuide[nodetype]:
            nodeindex = indexGuide[nodetype][nodeid]

            if userLabels.get(nodeindex) is not None:
                allLabels[nodeindex] = userLabels.get(nodeindex)

            else:
                allLabels[nodeindex] = [0] * labelLength

    return allLabels

def buildUnlabbelledLabelsDict(indexGuide, labelledDict, labelLength):
    allLabels = {}

    for nodetype in indexGuide:
        for nodeid in indexGuide[nodetype]:
            nodeindex = indexGuide[nodetype][nodeid]

            if labelledDict.get(nodeindex) is not None:
                # allLabels[nodeindex] = labelledDict.get(nodeindex)
                pass

            else:
                allLabels[nodeindex] = [0] * labelLength

    return allLabels

# take training set size between 0 and 1
def splitDatasetLabels(realLabels, dummyLabels, training_set_size):

    if training_set_size < 0 or training_set_size > 1:
        raise ValueError(training_set_size)

    numrealTrainingLabels = int(training_set_size* len(realLabels))

    realLabelsItems = list(realLabels.items())

    realLabelsTraining  = realLabelsItems[:numrealTrainingLabels]

    realLabelsTest = realLabelsItems[numrealTrainingLabels:]


    numDummyTrainingLabels = int(training_set_size( len(dummyLabels)))

    dummyLabelsItems = list(realLabels.items())

    dummyLabelsTraining  = dummyLabelsItems[:numDummyTrainingLabels]

    dummyLabelsTest = dummyLabelsItems[numDummyTrainingLabels:]

    labels_train = dict(realLabelsTraining)
    labels_test = { **dict(realLabelsTest), **dict(dummyLabelsTest) }
    labels_train_all = {**dict(realLabelsTraining), **dict(dummyLabelsTraining)}

    return labels_train, labels_train_all, labels_test


def getSheriffBadgeDisplayNames():
    sheriffDisplayNames = ["Journeyman Geek", "Yaakov Ellis", "Mendy Rodriguez", "Ham Vocke",
    "Jane Willborn", "Tinkeringbell", "Laura Campbell", "Sara Chipps", "Aaron Shekey", "Ben Kelly", "g3rv4", "Vasudha Swaminathan", "kristinalustig", 
    "Horia Coman", "Ted Goas", "Benjamin Hodgson", "Des", "Tom Floyd", "Nicolas Chabanovsky", "Kurtis Beavers",
    "Donna", "Alex Miller", "Dean Ward", "Alex Warren", "Jon Chan", "Brian Nickel", "Tom Limoncelli", "Juice", "Hynes", "Kasra Rahjerdi", "ChrisF", "Gordon",
    "Flexo", "Andrew Barber", "Max", "Steven Murawski", "ThiefMaster", "Brad Larson", "George Stocker", "jjnguy", "Adam Lear", "casperOne", "NullUserException อ_อ", "BoltClock's a Unicorn",
    "Kev", "Lasse V. Karlsen", "Alex Miller", "Nick Craver", "random", "Sampson", "Ivo Flipse", "mmyers", "Gumbo"]
    return sheriffDisplayNames
   
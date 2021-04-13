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
            print("userid", userid, "was found to be a sheriff, adding +ve label for index", userIndex)
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
   

"""
Train GCN with SO stuff

Test out inference to make sure it works 

Create some different labels to classify the users/posts

USE SEGMENTATION TO CLASSIFY USERS WITH A SUBSET OF THE TEST SET
- this will allow me to show weaknesses on smaller datasets with short posts? with long posts? with X? with Y?

- can use posts by n00b users vs experts

- can use short vs long posts

- can be able to breakdown the performance of GCN on different contexts and understand in what ways its strong vsv weak and why
"""


"""
could have a core benchmark to extract users as we said for classification

can then do an extra benchmark of adding domain specific regex (regex on java/python function or module names) to the features


evaluate performance with F1 score

Run analysis with different types of user groupings - see if the graph is better or worse of diff types of users

Run analysis with different types of posts
"""

"""

Stuart idea for regex-based stuff like URLs and namespaces:

Go the regex as a preproc step before corenlp runm and replace all instances with a combination of chars of my own, 
then if it is recognized add it as muy own feature later - might be a way to use stanza and avoid corenlp slowness

"""


"""

Different Runs:

Class for moderators 

Class for expert/novice - multiclass by number of years

Class for upvote/downvote
"""

"""
Stuart usually does scripts, take in dataset/model name, test set to run everything for me
"""

"""
Write up the report with placeholders to describe the experiments


allow for tables with the different F1 scores - precision - recall - F1 - 
Start writing ASAP
Skeleton - bullet points fillout -  

"""


"""
My demo might have a presentation with the problem, GCN architecture, run it, initial results, 

IDEA: Show graphs and results connected with the data in a meaningful way while narrating and demostrating my understanding
"""
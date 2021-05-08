# from lib.stackoverflowproc.extraction import recentComments, recentPosts, recentUsers
from os import O_NOFOLLOW
import xml.etree.ElementTree as ET
# from html5_parser import parse
# This module will have functions for the implementations of different types of labels. Some will be dependent on the data I've extracted, 
# while others will be based on other stuff extracted from the website


# function to get the label of a user according to diamond mod status ( sheriff badgeholders )

"""
GENERAL PURPOSE
"""

def buildAllLabelsDict(indexGuide, userLabels, labelLength):
    allLabels = {}

    for nodetype in indexGuide:
        for nodeid in indexGuide[nodetype]:
            nodeindex = indexGuide[nodetype][nodeid]

            if userLabels.get(nodeindex) is not None:
                allLabels[nodeindex] = userLabels.get(nodeindex)

            else:
                allLabels[nodeindex] = [0 for i in range(labelLength)]

    return allLabels

def getAllUserIndexesWithBadge(badgename, badges, indexGuide):
    userIndexes = {}

    for badge in badges:
        if badge.get('Name') == badgename:
            userid = badge.get('UserId')
            userindex = indexGuide.get('user').get(userid)
            userIndexes[userindex] = badgename

    return userIndexes

"""
NICE POST/ANSWER BASED LABELS
"""


##  MULTICLASS
#   Label definition:
#   [0,0,0,1] -> Has both nice question and a nice answer badges
#   [0,0,1,0] -> Has a nice answer but not a nice question
#   [0,1,0,0] -> Has a nice question but not a nice answer
#   [1,0,0,0] -> Neither has a nice question nor a nice answer

def getAllLabelsUsingNiceQuestionAnswerMulticlass(users, badges, indexGuide):
    niceQuestionUsers = getAllUserIndexesWithBadge("Nice Question", badges, indexGuide)
    niceAnswerUsers = getAllUserIndexesWithBadge("Nice Answer", badges, indexGuide)
    userLabels = getMulticlassLabelsFromNiceQA(niceQuestionUsers, niceAnswerUsers, users, indexGuide)
    print("Label distribution for users in Multiclass [noNicePosts, NiceQuestionOnly, NiceAnswerOnly, Both]:",getLabelDistribution(userLabels, 4))
    allLabels = buildAllLabelsDict(indexGuide, userLabels, 4)
    return allLabels, userLabels
    
    


def getMulticlassLabelsFromNiceQA(niceQuestionUsers, niceAnswerUsers, users, indexGuide):
    both = (set(niceAnswerUsers.keys()) & set( niceQuestionUsers.keys()))
    userLabels = {}

    for user in users:
        userindex = indexGuide['user'][user.get('Id')]
        
        if userindex in both:
            userLabels[userindex] = [0,0,0,1]

        elif userindex in niceAnswerUsers:
            userLabels[userindex] = [0,0,1,0]

        elif userindex in niceQuestionUsers:
            userLabels[userindex] = [0,1,0,0]

        else:
            userLabels[userindex] = [1,0,0,0]

    return userLabels


##  BINARY
#   Label definition
#   Nice Post (Q/A) -> [0,1]
#   No Nice Post -> [1,0]

def getAllLabelsUsingNiceQuestionAnswerBinary(users, badges, indexGuide):
    niceQuestionUsers = getAllUserIndexesWithBadge("Nice Question", badges, indexGuide)
    niceAnswerUsers = getAllUserIndexesWithBadge("Nice Answer", badges, indexGuide)
    userLabels = getBinaryLabelsFromNiceQA(niceQuestionUsers, niceAnswerUsers, users, indexGuide)
    print("Label distribution for users in binary [noniceposts, nicepost]:",getLabelDistribution(userLabels, 2))
    allLabels = buildAllLabelsDict(indexGuide, userLabels, 2)
    return allLabels, userLabels

def getBinaryLabelsFromNiceQA(niceQuestionUsers, niceAnswerUsers, users, indexGuide):
    either = niceAnswerUsers.copy()
    either.update(niceQuestionUsers)
    userLabels = {}

    for user in users:
        userindex = indexGuide['user'][user.get('Id')]

        if userindex in either:
            userLabels[userindex] = [0,1]
        
        else:
            userLabels[userindex] = [1,0]

    return userLabels
            

"""
BADGE CLASS LABELS
"""
def getUserLabelsUsingBadgeClass(users,badges, indexGuide):
    userClasses = buildUserBadgeClassDict(badges)
    userLabels = getBadgeClassBasedLabelDict(users, indexGuide, userClasses)
    return userLabels

def getAllLabelsUsingBadgeClass(users, badges, indexGuide):
    userClasses = buildUserBadgeClassDict(badges)
    userLabels = getBadgeClassBasedLabelDict(users, indexGuide, userClasses)
    print("Number of user labels", len(userLabels))
    allLabels = buildAllLabelsDict(indexGuide, userLabels, 4)
    return allLabels, userLabels

def getBadgeClassBasedLabelDict(users, indexGuide, userClasses):
    labelDict = {}
    userclasscounts = [0,0,0,0]
    for user in users:
        userid = user.get('Id')
        userIndex = indexGuide.get('user').get(userid)
        userClass = userClasses.get(userid)

        # using numerical indexing in userClasses, class 1 is bronze, class 2 is silver, class 3 is gold
        if userClass is not None:
            label = [0,0,0,0]
            label[userClass] = 1
            labelDict[userIndex] = label
            userclasscounts[userClass] += 1
        else:
            labelDict[userIndex] = [1,0,0,0] # put in label for 1,0,0,0 
            userclasscounts[0] += 1
        # best way to do this is to iterate ofver badges first and get dicts for gold, silver and bronze users
    print("Numbers of [lurker, bronze, silver, gold] users: ", userclasscounts)
    return labelDict
# 1 = Gold
# 2 = Silver
# 3 = Bronze
# NOTE could have made this cleaner if there were more classes but oh well
def buildUserBadgeClassDict(badges):
    userClasses = {}

    for badge in badges:
        userid = badge.get('UserId')
        badgeclass = badge.get('Class')
        badgename = badge.get('Name')
        if badgeclass == '1': # gold 
            userClasses[userid] = 3

        elif badgeclass == '2': # silver, not yearling since yearling GREATLY skews results
            if badgename == "Yearling":
                continue
            if userClasses.get(userid) == 3:
                continue
            else:
                userClasses[userid] = 2

        elif badgeclass == '3': # bronze
            if userClasses.get(userid) == 2 or userClasses.get(userid) == 3:
                continue
            else:
                userClasses[userid] = 1

        else:
            raise ValueError("Invalid badge class!")

    return userClasses


"""
SHERIFF BASED LABELS
"""

def buildSheriffBasedLabelsDict(users, indexGuide, sheriffIds):
    labelDict = {}

    for user in users:
        userid = user.get('Id')
        userIndex = indexGuide.get('user').get(userid)
        
        if userid in sheriffIds:
            # print("userid", userid, "was found to be a sheriff, adding +ve label for index", userIndex)
            labelDict[userIndex] = [0,1]
        
        else:
            labelDict[userIndex] = [1,0]

    return labelDict


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

def getSheriffBadgeDisplayNames():
    sheriffDisplayNames = ["Journeyman Geek", "Yaakov Ellis", "Mendy Rodriguez", "Ham Vocke",
    "Jane Willborn", "Tinkeringbell", "Laura Campbell", "Sara Chipps", "Aaron Shekey", "Ben Kelly", "g3rv4", "Vasudha Swaminathan", "kristinalustig", 
    "Horia Coman", "Ted Goas", "Benjamin Hodgson", "Des", "Tom Floyd", "Nicolas Chabanovsky", "Kurtis Beavers",
    "Donna", "Alex Miller", "Dean Ward", "Alex Warren", "Jon Chan", "Brian Nickel", "Tom Limoncelli", "Juice", "Hynes", "Kasra Rahjerdi", "ChrisF", "Gordon",
    "Flexo", "Andrew Barber", "Max", "Steven Murawski", "ThiefMaster", "Brad Larson", "George Stocker", "jjnguy", "Adam Lear", "casperOne", "NullUserException อ_อ", "BoltClock's a Unicorn",
    "Kev", "Lasse V. Karlsen", "Alex Miller", "Nick Craver", "random", "Sampson", "Ivo Flipse", "mmyers", "Gumbo"]
    return sheriffDisplayNames
   



"""
MISC
"""

def getLabelDistribution(userLabels, num_classes):
    labelRates = [0 for i in range(num_classes)]

    for userindex in userLabels:
        label = userLabels[userindex]
        labelclass = label.index(1)

        labelRates[labelclass] += 1

    return labelRates



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
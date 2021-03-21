import numpy
import xml.etree.ElementTree as ET
import os
import matplotlib.pyplot as plt

# class DataExtractor:

# checking if a post was made in 2019 or later
def isCreatedAfter2019(post):
    creationDate = post.get('CreationDate')
    year = int(creationDate[:4])
    if year >= 2019:
        return True
    else:
        return False    


def getFilteredChildrenDict(filterFunc, root):
    relevant = []

    for child in root:
        if (filterFunc(child.attrib)):
            relevant.append(child.attrib)

    return relevant

#   Gets list of relevant badges according to the list of users we are using
#   changed to a hashed implementation. users is a dict with the ids as the keys
def getRelevantBadges(badgesRoot, users):
    relevant = []

    for child in badgesRoot:
        if (isRelevantBadge(child.attrib, users)):
            relevant.append(child.attrib)

    return relevant

def isRelevantBadge(badge, users):
    badgeuserid = badge.get('UserId')
    
    relevantUser = users.get(badgeuserid)
    if relevantUser is not None:
        return True
    else:
        return False    

def user_accessed_recently(user):
    last_access = user.get('LastAccessDate')

    year = int(last_access[:4])
    
    if year >= 2019:
        return True
    else:
        return False   

def getRecentlyAccessedusers(root):
    relevant = []
    userdict = {}
    for child in root:
        if (user_accessed_recently(child.attrib)):
            relevant.append(child.attrib)
            userdict[child.attrib.get('Id')] = child.attrib.get('DisplayName')

    return relevant, userdict

def extractConnectedUsers(root, useriddict):
    connectedUsers = []

    for child in root:
        userid = child.attrib.get('Id')
        if useriddict.get(userid) is not None:
            connectedUsers.append(child.attrib)

    return connectedUsers

def listChildrenAttrib(node):
    childAttrib = []
    for child in node:
        childAttrib.append(child.attrib)

    return childAttrib
        
def extractAttribList(dictlist, attrib):
    if dictlist[0].get(attrib) is None:
        raise Exception("Passed attrib is not an attribute of the dictionaries in the list!")

    attList = []

    for entry in dictlist:
        attList.append(entry.get(attrib))

    return attList

def constructRelevantUserIdDict(posts, comments):
    relevantUsers = {}

    for post in posts:
        relevantUsers[post.get('OwnerUserId')] = 1

    for comment in comments:
        relevantUsers[comment.get('UserId')] = 1

    return relevantUsers


metaFolder = "../datasets/meta.stackoverflow.com/"
toTruncate = ["Posts", "Comments", "PostHistory", "Votes", "PostLinks"]
# Files to truncate by CreationDate: Posts, Comments, PostHistory, Votes, PostLinks
# Users will be truncated by last access date
    # Files to filter by ids of users that have been included: Badges
    # no edits: Tags

recentPosts = getFilteredChildrenDict(isCreatedAfter2019, ET.parse("../datasets/meta.stackoverflow.com/Posts.xml").getroot())
print("extracted posts")

recentComments = getFilteredChildrenDict(isCreatedAfter2019, ET.parse("../datasets/meta.stackoverflow.com/Comments.xml").getroot())
print("extracted comments")

# TODO change the way users are extracted to reflect the comment and post lists we're working with, current list has too many isolated nodes
recentUsers, userDict = getRecentlyAccessedusers( ET.parse("../datasets/meta.stackoverflow.com/Users.xml").getroot())
print("extracted users")

connectedUsers = extractConnectedUsers(ET.parse("../datasets/meta.stackoverflow.com/Users.xml").getroot(), constructRelevantUserIdDict(recentPosts, recentComments))
print("extracted connected users")
# extract a list of all the instances of the specified attribute in the list of dicts


# recentPostHistory = filter2019Later(ET.parse("../datasets/meta.stackoverflow.com/PostHistory.xml").getroot())
# print("ye3")

# recentVotes = filter2019Later(ET.parse("../datasets/meta.stackoverflow.com/Votes.xml").getroot())
# print("ye4")

# recentPostLinks = filter2019Later(ET.parse("../datasets/meta.stackoverflow.com/PostLinks.xml").getroot())
# print("ye5")


# print(len(recentUsers))
# print(recentUsers[0].get('Id'), userDict.get(recentUsers[0].get('Id')))

# recentBadges = getRelevantBadges(ET.parse("../datasets/meta.stackoverflow.com/Badges.xml").getroot(), userDict)
# print("ye7")

# recentTags = listChildrenAttrib(ET.parse("../datasets/meta.stackoverflow.com/Tags.xml").getroot())
# print("ye8")

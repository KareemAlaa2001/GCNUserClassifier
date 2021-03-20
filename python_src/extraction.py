from collections import UserDict
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


def filter2019Later(root):
    relevant = []

    for child in root:
        if (isCreatedAfter2019(child.attrib)):
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

def listChildrenAttrib(node):
    childAttrib = []
    for child in node:
        childAttrib.append(child.attrib)

    return childAttrib
        

metaFolder = "../datasets/meta.stackoverflow.com/"
toTruncate = ["Posts", "Comments", "PostHistory", "Votes", "PostLinks"]
# Files to truncate by CreationDate: Posts, Comments, PostHistory, Votes, PostLinks
# Users will be truncated by last access date
    # Files to filter by ids of users that have been included: Badges
    # no edits: Tags

# recentPosts = filter2019Later(ET.parse("../datasets/meta.stackoverflow.com/Posts.xml").getroot())
# print("extracted posts")
# recentComments = filter2019Later(ET.parse("../datasets/meta.stackoverflow.com/Comments.xml").getroot())
# print("extracted comments")

recentUsers, userDict = getRecentlyAccessedusers(ET.parse("../datasets/meta.stackoverflow.com/Users.xml").getroot())
print("extracted users")

# extract a list of all the instances of the specified attribute in the list of dicts
def extractAttribList(dictlist, attrib):
    if dictlist[0].get(attrib) is None:
        raise Exception("Passed attrib is not an attribute of the dictionaries in the list!")

    attList = []

    for entry in dictlist:
        attList.append(entry.get(attrib))

    return attList

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








    


  
    








"""
stanza.download('en')
nlp = stanza.Pipeline('en')

test_str = "<xml>Stanford University is located in California. It is a great university.</xml>"


doc = nlp(test_str)
print(doc)
print(doc.entities)

# def getRelevantComments(commentsRoot, relevantPosts):
#     relevantComments = []

#     for comment in commentsRoot:

#         if (isCreatedAfter2019(comment.attrib)):
#             parentid = comment.attrib.get('PostId')

#             # check in the relevant posts list for a post with the id
#             relevantParentPost = next((post for post in relevantPosts if post["Id"] == parentid), None)
#             if relevantParentPost is not None:
#                 relevantComments.append(comment.attrib)

#     return relevantComments
"""
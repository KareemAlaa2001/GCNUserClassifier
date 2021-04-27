import numpy
import xml.etree.ElementTree as ET
import os
import matplotlib.pyplot as plt
from lib.stackoverflowproc.helpers import *
# class DataExtractor:

# checking if a post was made in the cutoff year or later
def isCreatedAfterYear(post, cutoffYear):
    creationDate = post.get('CreationDate')
    year = int(creationDate[:4])
    if year >= cutoffYear:
        return True
    else:
        return False    

def isCreatedAfter2019(post):
    return isCreatedAfterYear(post, 2019)



# builds a list of dicts of children attributes based on satisfaction of the filtering function
def getFilteredChildrenList(filterFunc, root):
    relevant = []

    for child in root:
        if (filterFunc(child.attrib)):
            relevant.append(child.attrib)

    return relevant

#   Gets list of relevant badges according to the list of users we are using
#   changed to a hashed implementation. users is a dict with the ids as the keys
def getRelevantBadges(badgesRoot, userDict):
    relevant = []

    for child in badgesRoot:
        if (isRelevantBadge(child.attrib, userDict)):
            relevant.append(child.attrib)

    return relevant

def isRelevantBadge(badge, users):
    badgeuserid = badge.get('UserId')
    
    relevantUser = users.get(badgeuserid)
    if relevantUser is not None:
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

def extractAttribListIgnoreNones(dictlist, attrib):
    attList = []

    for entry in dictlist:
        if entry.get(attrib) is not None:
            attList.append(entry.get(attrib))

    return attList

def constructRelevantUserIdDict(posts, comments):
    relevantUsers = {}

    for post in posts:
        relevantUsers[post.get('OwnerUserId')] = 1

    for comment in comments:
        relevantUsers[comment.get('UserId')] = 1

    return relevantUsers

"""
POSTS
FUNCTIONS FOR EXTRACTING AND PREPROCESSING POST DICTIONARIES
"""

def buildPostDict(posts):
    postDict = {}

    for post in posts:
        postDict[post.get('Id')] = post

    return postDict

def removePostsWithMissingParents(posts, postsDict):
    linkedPosts = []

    for post in posts:
        if post.get('PostTypeId') == '2':
            parent = postsDict.get(post.get('ParentId'))

            if parent is not None:
                linkedPosts.append(post)

        else:
            linkedPosts.append(post)
    
    return linkedPosts




def givePostsParentViews(posts, postsDict):
    editedPosts = []
     
    for post in posts:
        if post.get('PostTypeId') == '2':
            parent = postsDict.get(post.get('ParentId'))
            if parent is not None:
                postCopy = post.copy()

                post['ViewCount'] = parent['ViewCount'] 
                
                postsDict.get(post.get('Id'))['ViewCount'] = parent['ViewCount']

            else:
                raise Exception("There should not be any orphan answer posts in this list!!")
                
    return posts, postsDict

def addAcceptedAnswerStatus(posts):

    acceptedAnswerIds = {}

    for post in posts:
        
        if post.get('AcceptedAnswerId') is not None:
            answerid = post.get('AcceptedAnswerId')
            acceptedAnswerIds[answerid] = '1'

    for post in posts:
        if acceptedAnswerIds.get(post.get('Id')) is not None:
            post['IsAcceptedAnswer'] = '1.0'

        else:
            post['IsAcceptedAnswer'] = '0.0'

    postsDict = buildPostDict(posts)
    return posts, postsDict

    

def extractPosts(filterfunc,root):
    initialPostList = getFilteredChildrenList(filterfunc, root)

    postsDict = buildPostDict(initialPostList)

    withoutOrphans = removePostsWithMissingParents(initialPostList, postsDict)

    # posts dict now built in here
    acceptedAnswers, pdict = addAcceptedAnswerStatus(withoutOrphans)

    viewsAdded, pdict = givePostsParentViews(acceptedAnswers, pdict)
    

    return viewsAdded, pdict


'''
COMMENTS
FUNCTIONS FOR EXTRACTING AND PREPROCESSING COMMENT DICTIONARIES
'''
def removeUnlinkedComments(comments, postDict):
    linkedComments = []

    for comment in comments:
        if postDict.get(comment.get('PostId')) is not None:
            linkedComments.append(comment)

    return linkedComments

def addCommentsLastActivityFromParent(comments, postDict):

    for comment in comments:
        parentPost = postDict.get(comment.get('PostId'))
        comment['LastActivityDate'] = parentPost.get('LastActivityDate')

    return comments

def pre_preprocessCommentsList(comments, postDict):
    filtered = removeUnlinkedComments(comments, postDict)
    activityadded = addCommentsLastActivityFromParent(filtered, postDict)
    return activityadded

def extractComments(filteringfunc, commentsroot, postsDict):
    initialCommentsList = getFilteredChildrenList(filteringfunc, commentsroot)
    commentsList = pre_preprocessCommentsList(initialCommentsList, postsDict)
    return commentsList

metaFolder = "../datasets/meta.stackoverflow.com/"
toTruncate = ["Posts", "Comments", "PostHistory", "Votes", "PostLinks"]
# Files to truncate by CreationDate: Posts, Comments, PostHistory, Votes, PostLinks
# Users will be truncated by last access date
    # Files to filter by ids of users that have been included: Badges
    # no edits: Tags

# OG recentposts
recentPosts, postDict = extractPosts(isCreatedAfter2019, ET.parse("../../datasets/meta.stackoverflow.com/Posts.xml").getroot())

# trying a smaller set, created 2020 or later
# recentPosts, postDict = extractPosts((lambda post: int(post.get('CreationDate')[:4]) >= 2020), ET.parse("../../datasets/meta.stackoverflow.com/Posts.xml").getroot())
print("extracted posts")

# OG recentComments
recentComments = extractComments(isCreatedAfter2019, ET.parse("../../datasets/meta.stackoverflow.com/Comments.xml").getroot(), postDict)
# recentComments = extractComments((lambda comment: int(comment.get('CreationDate')[:4]) >= 2020), ET.parse("../../datasets/meta.stackoverflow.com/Comments.xml").getroot(), postDict)
print("extracted comments")

# OLDrecentUsers, userDict = getRecentlyAccessedusers( ET.parse("../datasets/meta.stackoverflow.com/Users.xml").getroot())
# print("extracted users")

# updated list of recent users to reflect those involved in comments and posts above rather than everyone that logged in 2019 or later
relevantUserIdDict = constructRelevantUserIdDict(recentPosts, recentComments)
recentUsers = extractConnectedUsers(ET.parse("../../datasets/meta.stackoverflow.com/Users.xml").getroot(), relevantUserIdDict)
print("extracted connected users")
# extract a list of all the instances of the specified attribute in the list of dicts

# print(len(recentPosts))
# print(len(recentComments))
# print(len(recentUsers))

# recentPostHistory = filter2019Later(ET.parse("../datasets/meta.stackoverflow.com/PostHistory.xml").getroot())
# print("ye3")

# recentVotes = filter2019Later(ET.parse("../datasets/meta.stackoverflow.com/Votes.xml").getroot())
# print("ye4")

# recentPostLinks = filter2019Later(ET.parse("../datasets/meta.stackoverflow.com/PostLinks.xml").getroot())
# print("ye5")


# print(len(recentUsers))
# print(recentUsers[0].get('Id'), userDict.get(recentUsers[0].get('Id')))

recentBadges = getRelevantBadges(ET.parse("../../datasets/meta.stackoverflow.com/Badges.xml").getroot(), relevantUserIdDict)
print("Extracted the relevant badges")

# recentTags = listChildrenAttrib(ET.parse("../datasets/meta.stackoverflow.com/Tags.xml").getroot())
# print("ye8")

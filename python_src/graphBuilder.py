import numpy as np
import random
from extraction import recentComments, recentPosts, recentUsers
from helpers import *

#  appending all 3 lists into a big list and shuffling it
def shuffleData(posts, users, comments):
    
    masterList = posts + users + comments
    random.shuffle(masterList)

    return masterList

def buildIndexGuide(posts, users, comments):
    shuffledData = shuffleData(posts, users, comments)

    indexGuide = {
        'posts':{},
        'users':{},
        'comments':{}
    }

    for i in range(len(shuffledData)):
        entry = shuffledData[i]
        entId = entry.get('Id')

        if entId is None:
            raise Exception("This entry should have an id! Something is seriously wrong.")
        
        # probably could replace this with a cleaner implementation that has the "type" returned from the helper func
        if isPost(entry):
            indexGuide['posts'][entId] = i
        elif isUser(entry):
            indexGuide['users'][entId] = i
        elif isComment(entry):
            indexGuide['comments'][entId] = i
        else:
            raise Exception("Should either be a post, user or comment!")

    return indexGuide


# Should probably build the interaction graph using just the ids, then using the indexguide to convert ids to indexes
# Can do this by looping over all posts, users and comments and building one sided interaction graphs, 
# then looping over that graph to put the corresponding second sides to complete the graph
def buildIdNeighbourhoodDict(posts, users, comments):
    # will contain entries such as posts: {id: {neighbourid: 'post'|'user'|'comment'}}, 
    idNeighbourhoods = {'post':{},'user':{},'comment':{}}

    for post in posts:
        neighbours = constructPostNeighbours(post)
        postid = post.get('Id')
        idNeighbourhoods['post'][postid] = neighbours

    for comment in comments:
        neighbours = constructCommentNeighbours(comment)
        commentid = comment.get('Id')
        idNeighbourhoods['comment'][commentid] = neighbours

    for user in users:
        neighbours = constructUserNeighbours(user)
        userid = post.get('Id')
        idNeighbourhoods['user'][userid] = neighbours
    
    idNeighbourhoods = buildLikewiseRelationships(idNeighbourhoods)

    return idNeighbourhoods

# takes a graph with one-sided relationships and makes them two-sided
def buildLikewiseRelationships(neighbourhoods):
    
    for nodetype in neighbourhoods:
        for nodeid in neighbourhoods[nodetype]:
            nodeneighbourhood = neighbourhoods[nodetype][nodeid]
            for neighbourid in nodeneighbourhood:
                neighbourtype = nodeneighbourhood[neighbourid]
                neighbourhoods[neighbourtype][neighbourid][nodeid] = nodetype
    
    return neighbourhoods

"""

Functions for getting the neighbours of different types of nodes

TODO Build links BOTH ways in the neighbourhood dicts

Neighbours of a POST:
    If Post is a response:
        ParentId
    If Post is a parent:
        ChildrenIds

    - CommentIds for any comments
    - OwnerUserId (If present, if not then user was deleted)
    - (LastEditorUserId - not being used since we're not reaaally capturing edit history rn)
    - Possibly any entries in PostLinks that links this either with another post or with a duplicate

Neighbours of a USER:
    - PostIds of any posts that link to this user
    - CommentIds of any comments that link to this user
    Nothing to construct from this end so far, but users are included in links from other types


Neighbours of a COMMENT:
    - PostId
    - UserId (If present, if not then user was deleted) 

"""

# NOTE functions to construct neighbourhood dicts belonging to individual posts

def constructPostNeighbours(post):
    neighbours = {}

    if post.get('PostTypeId') == '2':
        neighbours[post.get('ParentId')] = 'post'

    if post.get('OwnerUserId') is not None:
        neighbours[post.get('OwnerUserId')] = 'user'

    # TODO implement postlinks here

    return neighbours

def constructUserNeighbours(user):
    return {}

def constructCommentNeighbours(comment):
    neighbours = {}

    if comment.get('UserId') is not None:
        neighbours[comment.get('UserId')] = 'user'

    if comment.get('PostId') is not None:
        neighbours[comment.get('PostId')] = 'post'


    return neighbours

def main():
    pass

if __name__ == '__main__':
    main()

"""


Should I include PostLinks info in my data????
    They encode info about which posts reference other posts, and which posts are duplicates (probably tbh)

How will I build these:

    Place all post, user and comment dicts in one list, then shuffle that list. I can then place their ids in the indexGuide

    Then when constructing the neighbours of a post/user/comment, I just pass that individual one and the indexguide to build up the neighbours

What I currently have: 
    Separate lists of posts, users and comments. Each post has an associated id, BUT they're not indexed in order.
    Ids also don't start from 0, which can be problematic. 


Also needed:

    I need to shuffle them all together, since I want it
    to be easier to split into training/testing with roughly proportional amounts of nodes

IDEA:
    Can keep a dict with the following structure:
    {
        posts: {
            id1:index1
            id2:index2 
        },
        users: {
            id: index
        },
        comments: {
            like above
        }

    }

What GCN utils expects:
    Loads input data from gcn/data directory

    ind.dataset_str.x => the feature vectors of the training instances as scipy.sparse.csr.csr_matrix object;
    ind.dataset_str.tx => the feature vectors of the test instances as scipy.sparse.csr.csr_matrix object;
    ind.dataset_str.allx => the feature vectors of both labeled and unlabeled training instances
        (a superset of ind.dataset_str.x) as scipy.sparse.csr.csr_matrix object;
    ind.dataset_str.y => the one-hot labels of the labeled training instances as numpy.ndarray object;
    ind.dataset_str.ty => the one-hot labels of the test instances as numpy.ndarray object;
    ind.dataset_str.ally => the labels for instances in ind.dataset_str.allx as numpy.ndarray object;
    ind.dataset_str.graph => a dict in the format {index: [index_of_neighbor_nodes]} as collections.defaultdict
        object;
    ind.dataset_str.test.index => the indices of test instances in graph, for the inductive setting as list object.

    All objects above must be saved using python pickle module.

"""
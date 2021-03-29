import numpy as np
import random
from genhelpers import initEmptyTypesDict
# from fvBuilder import *
# from extraction import recentComments, recentPosts, recentUsers
# from helpers import *

# def buildFeatureVectorList(data, client):
#     pass


def main():
    # TODO test the buildGCNGraph Function with a tricky masterdict & accompanying schema
    # TODO verificationnnnnnnnn
    masterdict = {
        'typeA': [
            {
                'identifier': '1',
                'daughter': '2',
                'son':['25', '69'],
                'feature2': 'Ya bish'
            },
            {
                'identifier': '2',
                'daughter': '1',
                'featureA': 'lmaooo'
            }

        ], 'typeB': [
            {
                'identifierB': '25',
                'daddy': ['1','2']

            },
            {
                'identifierB': '69',
                'mommy': '25'
            }

        ]
    }

    # TODO build a nice fat verification function for any schemas passed in by library users
    schema = {
        'typeA': {
            'toptype': True, # I might leave the toptype out of the schema, depending on how I format the masterdict builder 
            'idAtt': 'identifier',
            'featureAtts': ['featureA', 'feature2','feature3'],
            'linkAtts': {
                'daughter': 'typeA',
                'son': 'typeB',
                'child':'typeA'
                
            }
        },
        'typeB': {
            'idAtt': 'identifierB',
            'featureAtts': ['featureA', 'feature2','feature3'],
            'linkAtts': {
                'mommy': 'typeB',
                'daddy': 'typeA'
                
            }
        },
    }
    buildGCNGraph(masterdict, schema)

# takes individual lists of posts, users and comments and builds the corresponding adjacency matrices in dict form
def buildGCNGraph(masterdict, schema):
    # data = shuffleData(masterdict)
    # indexGuide = buildIndexGuide(data)
    indexGuide = buildShuffledIndexGuide(masterdict, schema)
    idGraph = buildIdNeighbourhoodDict(masterdict, schema)
    gcngraph = convertIdGraphToIndexGraph(idGraph, indexGuide)
    print('Masterdict:')
    print(masterdict)
    print('Index guide:')
    print(indexGuide)
    print('Id Graph:')
    print(idGraph)
    print('Index Graph:')
    print(gcngraph)
    
    return gcngraph # data # uncomment this once I figure out what Im doing with data


# Builds an indexGuide containing mappings of id:index for each type in the dataset
def buildShuffledIndexGuide(masterdict, schema):
    # list of indexes of length - number of entries in the masterdict
    indexes = [i for i in range(len(shuffleData(masterdict)))]
    random.shuffle(indexes)

    indexGuide = initEmptyTypesDict(schema)

    i = 0

    for nodetype in masterdict:
        # print(nodetype)
        # looping over the list of entries in the respective type in the masterdict
        for entry in masterdict.get(nodetype):
            # print(entry)
            entId = entry.get(schema.get(nodetype).get('idAtt'))

            if entId is None:
                raise Exception("This entry should have an id! Something is seriously wrong.")

            indexGuide[nodetype][entId] = indexes[i]
            i += 1

    return indexGuide




#  appending all 3 lists into a big list and shuffling it
def shuffleData(masterdict):
    masterlist = []
    for type in masterdict:
        masterlist += masterdict[type]

    random.shuffle(masterlist)

    return masterlist

# def buildIndexGuide(data, schema):
#     indexGuide = {}

#     for nodetype in schema:
#         indexGuide[nodetype] = {}
    
#     for i in range(len(data)):
#         entry = data[i]
#         entId = entry.get('Id')

#         if entId is None:
#             raise Exception("This entry should have an id! Something is seriously wrong.")
        
#         # probably could replace this with a cleaner implementation that has the "type" returned from the helper func
#         if isPost(entry):
#             indexGuide['post'][entId] = i
#         elif isUser(entry):
#             indexGuide['user'][entId] = i
#         elif isComment(entry):
#             indexGuide['comment'][entId] = i
#         else:
#             raise Exception("Should either be a post, user or comment!")

#     return indexGuide


# Should probably build the interaction graph using just the ids, then using the indexguide to convert ids to indexes
# Can do this by looping over all posts, users and comments and building one sided interaction graphs, 
# then looping over that graph to put the corresponding second sides to complete the graph
def buildIdNeighbourhoodDict(masterdict, schema):
    # will contain entries such as posts: {id: {neighbourid: 'post'|'user'|'comment'}}, 
    idNeighbourhoods = initEmptyTypesDict(schema)

    # NOTE need to make sure the masterdict structure im using inside is consistent with the one I will be constructing
    for nodetype in schema:
        for node in masterdict[nodetype]:
            neighbours = constructNeighbours(node, nodetype, schema)
            nodeid = node.get(schema.get(nodetype).get('idAtt'))
            idNeighbourhoods[nodetype][nodeid] = neighbours

    
    # for post in posts:
    #     neighbours = constructPostNeighbours(post)
    #     postid = post.get('Id')
    #     idNeighbourhoods['post'][postid] = neighbours

    # for comment in comments:
    #     neighbours = constructCommentNeighbours(comment)
    #     commentid = comment.get('Id')
    #     idNeighbourhoods['comment'][commentid] = neighbours

    # for user in users:
    #     neighbours = constructUserNeighbours(user)
    #     userid = post.get('Id')
    #     idNeighbourhoods['user'][userid] = neighbours
    
    idNeighbourhoods = buildLikewiseRelationships(idNeighbourhoods)

    return idNeighbourhoods

# takes a graph with one-sided relationships and makes them two-sided
def buildLikewiseRelationships(neighbourhoods):
    
    for nodetype in neighbourhoods:
        for nodeid in neighbourhoods[nodetype]:
            nodeneighbourhood = neighbourhoods[nodetype][nodeid]
            for neighbourtype in nodeneighbourhood:
                for neighbourid in nodeneighbourhood[neighbourtype]:
                    neighboursofneighbour = neighbourhoods[neighbourtype][neighbourid][nodetype]
                    if nodeid not in neighboursofneighbour:
                        neighboursofneighbour.append(nodeid)
                
    
    return neighbourhoods


# loops ovr all of the connections in the id graph and builds their equivalents from the entry indexes in the whole shuffled dataset
def convertIdGraphToIndexGraph(idGraph, indexGuide):
    indexGraph = {}

    for nodetype in idGraph:

        for nodeid in idGraph[nodetype]:

            nodeneighbourhood = idGraph[nodetype][nodeid]
            neighbourlist = []

            for neighbourtype in nodeneighbourhood:
                for neighbourid in nodeneighbourhood[neighbourtype]:
                    neighbourlist.append(indexGuide[neighbourtype][neighbourid])


            nodeindex = indexGuide[nodetype][nodeid]
            indexGraph[nodeindex] = neighbourlist
    
    return indexGraph

"""
Neighbourdict foramt:
nodeneighbourhood = {
    typeA: [id1,id2,id3,id4],
    typeB: [id1,id2,id3,id4]
}
"""


def constructNeighbours(node, nodetype, schema):
    neighbours = {}

    for nt in schema:
        neighbours[nt] = []
    

    linkatts = schema[nodetype]['linkAtts']

    for att in linkatts:
        if node.get(att) is not None:
            neightype = linkatts[att]

            neighbourid = node.get(att)

            if isinstance(node.get(att),list):
                for neighid in node.get(att):
                    neighbours[neightype].append(neighid)

            else:
                neighbours[neightype].append(neighbourid)

    return neighbours





def constructPostNeighbours(post):
    neighbours = {}

    if post.get('PostTypeId') == '2':
        # TODO change this to nrighbours['post'] = comment.get('ParentId') OR 'ParentId' = comment.get('ParentId') to avoid overwrites from the same id in diff types
        neighbours[post.get('ParentId')] = 'post'

    # TODO same as above
    if post.get('OwnerUserId') is not None:
        neighbours[post.get('OwnerUserId')] = 'user'

    # TODO implement postlinks here

    return neighbours

def constructUserNeighbours(user):
    return {}

def constructCommentNeighbours(comment):
    neighbours = {}

    if comment.get('UserId') is not None:
        # TODO change this to nrighbours['user'] = comment.get('UserId') to avoid overwrites from the same id in diff types
        neighbours[comment.get('UserId')] = 'user'

    # TODO same as above 
    if comment.get('PostId') is not None:
        neighbours[comment.get('PostId')] = 'post'


    return neighbours



if __name__ == '__main__':
    main()


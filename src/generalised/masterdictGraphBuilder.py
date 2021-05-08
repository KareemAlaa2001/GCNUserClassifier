from re import L
import numpy as np
import random
from genhelpers import initEmptyTypesDict
from indexGraphBuilder import buildTransitivesMultipleTypedGraph
# from fvBuilder import *
# from extraction import recentComments, recentPosts, recentUsers
# from helpers import *

# def buildFeatureVectorList(data, client):
#     pass


def main():
    masterdict = {
        'typeA': [
            {
                'identifier': '1',
                'daughter': '2',
                'son':['25', '69'],
                'feature2': 'Ya boi'
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

    schema = {
        'typeA': {
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
    buildGCNGraphFromMasterdict(masterdict, schema)


class MasterdictGraphProcessor:
    def __init__(self, transitive=False):
        self.transitive = transitive

    def buildGraphsFromMasterDict(self, masterdict, schema):
        indexGuide = buildShuffledIndexGuide(masterdict, schema)
        idGraph = buildIdNeighbourhoodDict(masterdict, schema)

        if (self.transitive):
            idGraph = buildTransitivesMultipleTypedGraph(idGraph)

        gcngraph = convertIdGraphToIndexGraph(idGraph, indexGuide)

        return gcngraph, idGraph, indexGuide # returns indexGCNGraph, idGraph, indexGuide


# takes individual lists of posts, users and comments and builds the corresponding adjacency matrices in dict form
def buildGCNGraphFromMasterdict(masterdict, schema):
    # data = shuffleData(masterdict)
    # indexGuide = buildIndexGuide(data)
    indexGuide = buildShuffledIndexGuide(masterdict, schema)
    idGraph = buildIdNeighbourhoodDict(masterdict, schema)
    gcngraph = convertIdGraphToIndexGraph(idGraph, indexGuide)
    
    return gcngraph # data # uncomment this once I figure out what Im doing with data


# Builds an indexGuide containing mappings of id:index for each type in the dataset
def buildShuffledIndexGuide(masterdict, schema):
    # list of indexes of length - number of entries in the masterdict
    indexes = [i for i in range(len(shuffleData(masterdict)))]
    random.seed(123)
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

# Should probably build the interaction graph using just the ids, then using the indexguide to convert ids to indexes
# Can do this by looping over all nodetypes and building one sided interaction graphs, 
# then looping over that graph to put the corresponding second sides to complete the graph
def buildIdNeighbourhoodDict(masterdict, schema):
    idNeighbourhoods = initEmptyTypesDict(schema)
    
    for nodetype in schema:
        for node in masterdict[nodetype]:
            neighbours = constructNeighbours(node, nodetype, schema)
            nodeid = node.get(schema.get(nodetype).get('idAtt'))
            idNeighbourhoods[nodetype][nodeid] = neighbours
    
    idNeighbourhoods = buildLikewiseRelationships(idNeighbourhoods)

    commentneighbourhoods = idNeighbourhoods['comment']
    numcommentlinks = 0
    commentneighbourhoodprinted = False
    for commentid in commentneighbourhoods:
        
        for nodetype in commentneighbourhoods[commentid]:
            numcommentlinks += len(commentneighbourhoods[commentid][nodetype])

        if not commentneighbourhoodprinted:
            print(commentneighbourhoods[commentid])
            commentneighbourhoodprinted = True
    
    print("Number of comment links:",numcommentlinks)
    return idNeighbourhoods

# takes a graph with one-sided relationships and makes them two-sided
def buildLikewiseRelationships(neighbourhoods):
    
    for nodetype in neighbourhoods:
        for nodeid in neighbourhoods[nodetype]:
            nodeneighbourhood = neighbourhoods[nodetype][nodeid]
            for neighbourtype in nodeneighbourhood:
                for neighbourid in nodeneighbourhood[neighbourtype]:
                    intermediate1 = neighbourhoods[neighbourtype]
                    intermediate2 = intermediate1[neighbourid]
                    neighboursofneighbour = intermediate2[nodetype]
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

if __name__ == '__main__':
    main()

"""
"""
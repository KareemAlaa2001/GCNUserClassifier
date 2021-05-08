import masterdictGraphBuilder
import genhelpers
import random
from corpusreader import *

class GraphProcessor:
    def __init__(self, build_transitive):
        self.transitive = build_transitive

    def processMultiTypeGraph(self, graph):

        if verifyReadCorpusResultFormat(graph):
            return processAdjacenciesMultipleTypes(graph, self.transitive) # returns indexGCNGraph, idGraph, indexGuide
        else:
            raise ValueError("The result of the corpus reading in the processor passed in does not fit the format accepted by any of the graphbuilder module!")
        
    def processIndexedGraph(self, graph):
        if verifyReadCorpusResultFormat(graph):
            return processAdjacenciesIndexed(graph, self.transitive) # returns indexGCNGraph, idGraph, indexGuide
        else:
            raise ValueError("The result of the corpus reading in the processor passed in does not fit the format accepted by any of the graphbuilder module!")
        


# takes in a graph in the format {type:{nodeid: {neighbourtype: [neighbourids]}}}
# indexes the graph and returns: an indexguide, an idgraph and indexgraph - basically the same as the masterdict graphbuilder but without a schema 
def processAdjacenciesMultipleTypes(graph, transitive=False, shuffle=False):
    indexGuide = buildIndexGuide(graph, shuffle)

    missingsfilled = masterdictGraphBuilder.buildLikewiseRelationships(graph)

    if transitive:
        missingsfilled = buildTransitivesMultipleTypedGraph(missingsfilled) 

    gcngraph = masterdictGraphBuilder.convertIdGraphToIndexGraph(missingsfilled)

    return gcngraph, missingsfilled, indexGuide



# NOTE O(N^2) runtime, could optimise later/ leave as an optional addition - AVOID unless necessary
def buildTransitivesMultipleTypedGraph(graph):
    for nodetype in graph:
        for nodeid in graph[nodetype]:
            neighbourstoadd = genhelpers.initEmptyTypesDict(graph)

            for neighbourtype in graph[nodetype][nodeid]:
                for neighbourid in graph[nodetype][nodeid][neighbourtype]:
                    linkstoAdd = buildLinksToAdd(graph,nodeid, nodetype, neighbourid, neighbourtype)

                    for linktype in linkstoAdd:
                        for link in linktype:
                            if link not in neighbourstoadd[linktype]:
                                neighbourstoadd[linktype].append(link)

            for ntype in neighbourstoadd:
                for nid in neighbourstoadd[ntype]:
                    graph[nodetype][nodeid][ntype].append(nid)
                            
    return masterdictGraphBuilder.buildLikewiseRelationships(graph)       


                    


def buildLinksToAdd(graph, nodeid, nodetype,  neighbourid, neighbourtype):

    neighbourlinks = graph[neighbourtype][neighbourid]

    linkstoAdd = genhelpers.initEmptyTypesDict

    existingneighbours = graph[nodetype][nodeid]

    for linktype in neighbourlinks:
        for link in neighbourlinks[linktype]:
            if link not in existingneighbours[linktype]:
                linkstoAdd[linktype].append(link)

    return linkstoAdd


def buildIndexGuide(graph, shuffle=False):
    indexGuide = {}

    indexes = [i for i in range(len(masterdictGraphBuilder.shuffleData(graph)))]

    if shuffle:
        random.seed(123)
        random.shuffle(indexes)

    indexGuide = genhelpers.initEmptyTypesDict(graph)

    i = 0

    for nodetype in graph:
        # print(nodetype)
        # looping over the list of entries in the respective type in the masterdict
        for entry in graph.get(nodetype):
            # print(entry)
            entId = entry

            indexGuide[nodetype][entId] = indexes[i]
            i += 1

    return indexGuide


# takes in a graph with format {nodeid: [neighbourids]}
# will process it to complete links both ways and to add transitive connections if necessary
def processAdjacenciesIndexed(indexGraph, build_transitive=False):
    missingfilled = buildIndexGraphLikewiseRelationships(indexGraph)

    if build_transitive:
        return buildTransitiveRelationships(missingfilled)

    # NOTE could add more ways to process if necessary

    return missingfilled

# much simpler to handle than the nodeid graph
def buildIndexGraphLikewiseRelationships(indexGraph):

    for nodeindex in indexGraph:
        neighbours = indexGraph[nodeindex]

        for neighbourindex in neighbours:

            if nodeindex not in indexGraph[neighbourindex]:
                indexGraph[neighbourindex].append(nodeindex)

    return indexGraph

# NOTE O(N^2) runtime, could optimise later/ leave as an optional addition
def buildTransitiveRelationships(indexGraph):
    for index in indexGraph:
        neighbours = indexGraph[index]
        newneighbours = neighbours.copy()

        for neighbourid in neighbours:
            neighbourlinks = indexGraph[neighbourid]

            for link in neighbourlinks:
                if link not in neighbours:
                    newneighbours.append(link)

        indexGraph[index] = newneighbours

    return buildIndexGraphLikewiseRelationships(indexGraph)

        



"""
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
"""

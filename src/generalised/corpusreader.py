from abc import ABC, abstractmethod
from fileExtraction import *
from masterdictBuilder import buildMasterDict
from masterdictGraphBuilder import MasterdictGraphProcessor
from genhelpers import *

class CorpusReader:

    def __init__(self, schema_based):

        if not isinstance(schema_based, bool):
            raise Exception("Value passed into schema_based is not a boolean!")

        self.schema_based = schema_based

    def readCorpus(self, data, schema=None, toptypes=None, proc=None):
        if self.schema_based:
            if schema is None:
                raise Exception("This CorpusReader object was set to be schema based, but no schema was passed in!")
            
            proc = SchemaBasedCorpusProcessor(data, toptypes, schema)

            masterdict = proc.readCorpus()

            return masterdict
        
        else:
            if proc is None:
                raise Exception("This CorpusReader object was set to be non-schema based and thus requires a corpusprocessor instance, but none was passed in!")
            
            if not isinstance(proc, AbstractCorpusProcessor):
                raise Exception("This CorpusReader object was set to be non-schema based and thus requires a corpusprocessor instance, but the one passed in was not an AbstractCorpusProcessor subclass!")

            result = proc.readCorpus()

            if verifyReadCorpusResultFormat(result):
                return result
            else:
                raise Exception("The result of the corpus reading in the processor passed in does not fit the format accepted by any of the graphbuilder module!")


class AbstractCorpusProcessor(ABC):

    @abstractmethod
    def readCorpus(self):
        pass

class SchemaBasedCorpusProcessor(AbstractCorpusProcessor):
    def __init__(self, data, toptypes, schema):
        self.schema = schema
        self.data = data
        self.toptypes = toptypes


    def readCorpus(self):
        return buildMasterDict(self.data, self.schema, self.toptypes)


# TODO if time exists (prob not), can make this more sophisticated
# can flesh out XML extraction OR can figure out a way to extend to support mult files
class FileExtractor:
    def __init__(self, fileformat):

        if fileformat != "XML" and fileformat != "JSON":
            estr = "Filetype " + self.fileformat + " not supported, this module only supports \"XML\" and \"JSON\" formats"
            raise Exception(estr)

        self.fileformat = fileformat

    def extractData(self, filename):
        
        if self.fileformat == "XML":
            fileData = extractXMLFileToDict(filename)
        elif self.fileformat == "JSON":
            fileData = extractJSONFileToDict(filename)
        else:
            estr = "Filetype " + self.fileformat + " not supported, this module only supports \"XML\" and \"JSON\" formats"
            raise Exception(estr)

        return fileData

        

# TODO deal with the FVs


# want to be able to accommodate multiple node types
# Accepted formats: {nodeid: [neighbourids]} - no types
# typed - {nodetype: {nodeid: {neighbourtype: [neighbourids]}}}
def verifyReadCorpusResultFormat(data):
    if isinstance(data, dict):
        isAllLists = alldictvaluesatisfytype(data,list)

        if isAllLists:
            if alldictkeysarepositiveints(data):
                for nodeid in data:
                    neighlist = data[nodeid]
                    if alllistmembersarepositiveints(neighlist):
                        return True
                    else:
                        estr = "Values mapped to node ids were not all positive integers, so werent all neighbour indexes"
                        raise Exception(estr)
            else:
                raise Exception("Not all node keys are positive integers! They are supposed to represent node indexes")

        else:
            if verifyMultipeTypeGraph(data):
                return True
            else:
                raise Exception("There was a problem with the format that you entered!")
    else:
        estr = "Data is not in a dictionary format!"
        raise Exception(estr)



# verifies format {nodetype: {nodeid: {neighbourtype: [neighbourids]}}}
def verifyMultipeTypeGraph(graph):
    

    if isinstance(graph, dict):
        if allkeyssatisfytype(graph, str):
            nodetypes = []

            for nodetype in graph:
                nodetypes.append(nodetype)


            for nodetype in graph:
                if isinstance(graph[nodetype], dict):
                    nodetypenodes = graph[nodetype]
                    if alldictkeysarepositiveints(nodetypenodes):
                        if alldictvaluesatisfytype(nodetypenodes,dict):
                            for nodeid in nodetypenodes:
                                neighbourhood = nodetypenodes[nodeid]

                                if allkeyssatisfytype(neighbourhood, str):
                                    for ntype in neighbourhood:
                                        if ntype not in nodetypes:
                                            estr = "Node type " + ntype + " passed into neighbours of node " + nodeid + " is not one of the recognised types!"
                                            raise Exception(estr)

                                    if alldictvaluesatisfytype(neighbourhood, list):
                                        for ntype in neighbourhood:
                                            if alllistmembersarepositiveints(neighbourhood[ntype]):
                                                return True

                                            else:
                                                raise Exception("Non-int index neighbours entered")

                                else:
                                    estr = "Node types passed in for nodeid " + nodeid + " were not all strings, invalid format"
                                    raise Exception(estr)
                        else:
                            estr = "Nodetype " + nodetype + " mapping for some of its children was not a dict"
                            raise Exception(estr)
                    else:
                        estr = "Nodetype " + nodetype + " had a key which was not a node id! Was not a positive integer"
                        raise Exception(estr)
                else:
                    estr = "Nodetype " + nodetype + " mapping was not a dict"
                    raise Exception(estr)
        else:
            raise Exception("Suppsoed to have string nodetypes passed in at the top")
    else:
        raise Exception("Data is not in a dictionary format!")



"""
Can make a class to deal with node indexing as an intermediate, that can then return the indexGuide. 
This can make the graphbuilder only have to deal with nodes already indexed among all typesx

 and not hav

"""






"""
STUART'S EMAIL:

As discussed you need to think about the following for your software (to make it re-usable across two domains).
 
Below is what I was thinking listening to your description, simplified so its clean to my eyes. You need to think about it in the context of the work you have already done on schema, so you get the best value from the work you have done so far.
 
(a) corpus reader class (to load a corpus and create a graph ready for processing)
 
CorpusReaderStackOverflow.init( filename, stackflow_schema )
CorpusReaderIntelViz.init( filename )
 
CorpusReaderAbstract() {
  def init()
  def read_corpus() -> GCN input structures
 
(b) GCN input structures (which your code will use to run GCN)
 
graph = { node_id : [ node_id, node_id, ... ] }
node type index = { node_id : node_type }
node spec index = { node_id : <node spec> }
<node spec> = { feature_attribute : value, ... }
 
(c) GCN output structures (which your code will return after GCN has run)
 
connection matrix = { node_id : [ node_id, node_id ... ] }
 
the user will have the (b) structures already, so can simply lookup what each node_id means as they use the GCN connection data.
 
Best wishes,
Stuart
"""





"""
MY THOUGHTS:

If I reduce the library to the format that stuart is suggesting, then I'm not actually doing that much pre-processing,
and it would need my library to do more in terms of running GCN. I can't actually hand-craft the featurevectors myself though,
so that would need them to pass in the FVs as well. But then what am I doing? Am I just setting up a framework within which they can work? 
What am I actually simplifying? 


"""

"""
Thinking up a full use case scenario for my library. Ideally, it takes in the data in the original files and 
either uses the corpusreader input function of their own with the full variability to produce SOMETHING, that I can then use to elaborate

I think the whole point of my library is to prep data for GCN use, either with both FVs AND Adj or just Adj
"""



"""
Based on this, I should integrate the CorpusReader into my library to allow for full cusomtisability by the library user.

I think I should keep the schema though, since a lot of work has already gone into it.

How would I do this then? I could make my API have 2 classes: SchemaReader and AbstractCorpusReader

both do the same thing, both reading the dataset passed in (in file form) and outputting the relevant dicts with the information needed
to run GCN and for the libraey usser to interpret what's actually been produced
"""

"""
Perhaps SchemaReader can maintain the role of automatically dealing with any dataset that has fixed attribute names for nodes. 
This would cover datasets like stackoverflow where the db column names are used as the 
"""



"""
LIB MODULES:
"CorpusReader" -> Either Schema-based "CorpusReaderSchema" or based on subclass built
 - IDEA: INDEX NODES HERE RATHER THAN AT THE NEXT STAGE (FOR THE SCHEMA LIB), 
 CAN ALLOW FOR THE NEXT MODULE TO JUST DEAL WITH HOMOGENISED NODE IDS WITHOUT HAVING TO ACCOM FOR DIFFERENT 


This produces 

DATA FORMAT: {node_id: [neighbourid]}
   
[DATA FORMAT] - - should allow for EITHER multiple separated node types OR just a massive list of nodes directly indexed.
                - this should be a format capable of dealing with both ways the previous module was used

So we got 2 things - we can edit the masterdict to just use normal node ids. If that's the case though, then the data I want from the 

Passed into

"GraphBuilder" -> takes in that data format to build the completed adj matrix (since many links might be incomplete 
like those going both ways ), 


outputting the data formats as discussed with Stuart: 


graph = { node_id : [ node_id, node_id, ... ] }
node type index = { node_id : node_type }
node spec index = { node_id : <node spec> }
<node spec> = { feature_attribute : value, ... }

EL MOHEM --- EL PYTHON DICT elly fiha each node id and neighbourid lists

I can then have ANOTHER module, (smallboi) to convert to the exact types 
    - could take in featurevectors and convert them to a csr_matrix object - could build the listoflists by taking in {node_id: fv} OR just the list of lists to prod mat

Need to also be able to handle gold truth dataaaaaaaaaaa

CAN SPIT OUT THE DATA ITSELF FOR CUSTOM GCN IMPLEMENTATIONS
CAN HAVE ANOTHER MODULE AS A WRAPPER TO RUN THIS DATA WITH VANILLA GCN 

I NEED TO GET ALL THIS SHIT DONE IN A COUPLE OF DAYS BOIIIIIIII - necessary to allow for enough time to test out with GCN

"""
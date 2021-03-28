import xml.etree.ElementTree as ET
import json
from genhelpers import *

"""
Helper Module for extracting data from a selection of file types into the dictionary format used internally
"""

def generateAdjacencyDictFromStuartJson(datadict):
    adjdict = {} # THhis will deal with the specific stuart case


# loads an entire json file into memory
def extractJSONFileToDict(filename):
    file = open(filename)
    dataDict = json.load(file)
    return dataDict




# extracting data from XML files into the list of dicts format I got
def extractXMLFileToDict(filename):
    root = ET.parse(filename).getroot()
    
    # simple case for XML file structure (that it matches the SO Dump files)
    return listChildrenAttrib(root)
    
def listChildrenAttrib(node):
    childAttrib = []
    for child in node:
        childAttrib.append(child.attrib)

    return childAttrib


def main():
    print("testing different extraction functions")
    datadict = extractJSONFileToDict("testjson.json")
    # print(datadict)
    print(datadict['website_A_thread_1_post_100'])

    print(extractThreadId('website_A_thread_1_post_100'))
    print(extractPostId('website_A_thread_1_post_100'))



if __name__ == '__main__':
    main()

"""
Some ramblings i need to write down:
    In my original dataset, we had a list of individual entries with attributes that I extracted to both determine features and links.
    In that dict format, a generalisation would have been:

    data_schema {
        type1: {
            featureAtts: ['Att1Key', 'Att2Key'.....]
            linkAtts: {
                att1Key: neighbourtype,
                att2Key: neighhbourtype,
                ...
            }
        },
        type2: {
            featureAtts: ['Att1Key', 'Att2Key'.....]
            linkAtts: {
                att1Key: neighbourtype,
                att2Key: neighhbourtype,
                ...
            }
        }...

    }

    Then for each node we could construct: 
    Could do this by looping over linkatts in the schema in order to get all of the attributes linked to each type

    neighbours {
        typeA: [id1,id2,id3]
        typeB: [id1,id2,id3]
        ...
    }

"""

"""
In any format where we automatically want children nodes to be counted as neighbours ( like stuart), could do this:

WE STILL NEED A LIST OF ALL THE MF ENTRIES DAWG
master

produces graph: 
node_neighbours = {
    typeA: [id1,id2,id3]
    typeB: [id1,id2,id3]
    ...
}

Could allow for the customisation of atts:
data_schema {
        type1: {
            idAtt: 'attname' (in SO this was 'Id')
            featureAtts: ['Att1Key', 'Att2Key'.....]
            linkAtts: {
                att1Key: neighbourtype,
                att2Key: neighhbourtype,
                ...
            }
        },
        type2: {
            idAtt: 'attname' (in SO this was 'Id')
            featureAtts: ['Att1Key', 'Att2Key'.....]
            linkAtts: {
                att1Key: neighbourtype,
                att2Key: neighhbourtype,
                ...
            }
        }...

    }

In Stuart's thing's case:

Need to go through the dict, and based on a walk down the tree, 
use the data schema to identify each node type and build its instance of the data_schema 
then place those children in a BFS queue to explore them and build their instances into the master dict


thread needs its own treatment since its not actually a node in the graph and is rather parsed from the names

data_schema = {
    post: {
        idAtt: we don't have a specific att name, unlike stackoverflow - can ignore for now
        featureAtts: seebak
        linkAtts: {
            "author": person
            "page_url": page_url
            int: "Sentence" not an actual type in our graph???
            Yeahhhhh in this case would need to either keep checking the keys or maybe could take a hybrid approach:

        }
    }
}

def efhamfiEh(nodeid, node, nodetype, dataschema, filteringfunctions=None, actionFunctions=None, masterlist):
    # filteringfunctions: [String -> Bool] - list of string to bool functions supposed to identify special keys
    # actionFunctions: list of functions with the same length as filteringfunctions in order to identify what to do with each repsective key
    features = {}

    for child in node:

        
        if node[child] is a dict:
            add node[child] to explorationqueue
            continue

        if node[child] is a list:
            add *node[child] (unpacked list) to explorationqueue
            continue



        if dataschema[nodetype][idAtt] containskey child:
            7ot el id wel type fel masterlist faaaaast
        elif dataschema[nodetype][featureAtts] containskey child:
            features[child] = node[child]
        elif dataschema[nodetype][linkAtts] containskey child:
            features['neighbours'][node[child] (child Value (id))] = dataschema[child] (type of child)
        else:
            for function in filteringfunctions:
                if (filteringfunctions)

    # hat ba2a el nodeid ya fale7 wenta da5el, its the label for this dict
    masterlist[nodetype][nodeid] = features


SO I HAVE ONE OF THREE OPTIONS FOR STUART: 

- Going with the generalised dict idea without the filtering and action functions, which means that attribute names have to be 
consistent in the dataset. This will mean that he can use the generalised library but will have to adjust his output. 

- Giving his dataset "special treatment" in parsing, while still implementing the generalised dict idea. This means that he will not 
have to change the format of his data, but it also means that any future changes to the format will need to be reflected in the library, 
which isn't sustainable. 

- Going with the much more complex idea of allowing 'filtering' and 'action' functions, which will need much more input from the library user 
as well as a much more complex coding task from my end, but will allow for maximum customisability with regards to the data formats passed in.










POTENTIAL SOLUTION IN STUART'S CASE:
While doing the walk down the dict tree, can take the keys and identify their types based on functions of my own. 
This, however, is a very specific solution to this dataset. 
Could make that a way to parse datasets by using a factory func on that thing
"""



"""
IDEA: 
    I noticed that to make it meta here for the graph construction side I'm basically doing the same thing I did with the
    stackoverflow data. The same basic idea: we have different types of nodes, each with a different way to connect to other nodes.
    
    One way to look at the SO data I had was that it was a master dict, with each key being a nopdetype containing a list of 
    the dicts, each representing an individual instance

    Each dict contained information about 2 separate things that I had to customise based on the attributes, the actual features themselves, 
    and the separate link info. In my case, they were all jhumbled up in one big list of atts together, but what I could do is make it so that
    I can also pass in a data structure containing:

    {
        nodetype1: {
            identifyingattName: 'attname' (in SO this was 'Id')
            featureAttribs: {
                attribfeatureA: typeA, 
                attribFeatureB: typeB,
                attribFeatureC: typeC....
            }

            NOTE SHOULD FIRST FOCUS ON THESE BEFORE CONSIDERING FEATURE FLEXIBILITY, 
                SINCE COULD JUST RETURN INDEX: ENRTY MAPS AND ALLOW USER TO PASS THE FEATUREVECTORS THEMSELVES
            linkAttribs: {
                attribLinkA: nodeTypeLinkedA,
                attribLinkB: nodeTypeLinkedB,
                attribLinkC: nodeTypeLinkedC...
            }
        }
    }

"""

# TODO support Stuart's JSON output
"""
What I could do is convert stuart's graph representation to the lists of dicts structures I had, 
where each list would correspond to a certain nodetype


How is stuart's graph constructed? 

    QUICK N EZ SOLUTION, node links to all nodes under it in the tree

NodeTypes:

Thread:
    identifier: thread_threadid (can be regexed from the name)
    links:
        author: person
        posts: post

Post:
    identifier: post_postid
    links: 

Person:
    
    
OtherEntity:



{
    <website>_thread_<thread_id>_post_<post_id>: {
        "author": <author_name>,
        "page_url": <post_uri>,
        <sentence_index>: [
            {
                "entity": [
                    <NER-label>:<phrase>,
                    <NER-label>:<phrase>,
                    ...
                ]
            }
        ],
        <sentence_index>: [
            {
                "entity": [
                    <NER-label>:<phrase>,
                    <NER-label>:<phrase>,
                    ...
                ]
            }
        ],
        ...
    },
    <website>_thread_<thread_id>_post_<post_id>: {
        "author": <author_name>,
        "page_url": <post_uri>,
        <sentence_index>: [ ... ],
        ...
    }
}
"""
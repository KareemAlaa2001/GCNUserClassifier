from queue import Queue

"""
masterdict format: ( the whole point of this is to keep track of which items exist and what they link to, since this could then be used to build the graph dicts)
{
    typeA: [ (list of entries in that type)
        {
            Id: its id
            Features: {
                featureAName: value,
                featureBName: value,
                featureCName: value
            },
            Links: {
                typeA: [linkedid1, linkedid2, linkedid3]
                typeB: [linkedid1, linkedid2, linkedid3]
            }
            
        },
        {
            ....
        }
    }

}


alternative format:
{
    typeA: [ (list of entries in that type)
        {
            identifier: its id
            attname: value,
            attname: value,
            attname: value
            
        },
        {
            ....
        }
    ]
    
}
"""


"""
DATA schema format:

data_schema {
        Toptype: type
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
"""

# processes a passed in data dict containing the whole "graph" according to the schema in order to 
def processDataDict(datadict, data_schema):
    # initialising a masterlist, which will contain all of the graph nodes separated into their respective types. Format: dict of lists, 
    # masterlist = {}
    # toptype = data_schema['Toptype']

    # for nodetype in data_schema:
    #     masterlist[nodetype] = {}

    masterlist = buildMasterList(datadict, data_schema)
    build # why am i even trying to redesign these
    



    




def processIndividualNode(nodeid, node, nodetype, dataschema, masterlist, explorationqueue):
    # filteringfunctions: [String -> Bool] - list of string to bool functions supposed to identify special keys
    # actionFunctions: list of functions with the same length as filteringfunctions in order to identify what to do with each repsective key
    features = {}

    for child in node:

        
        if isinstance(node[child], dict):
            explorationqueue.put(node[child])
            continue

        if isinstance(node[child], list):
            # TODO implement: add *node[child] (unpacked list) to explorationqueue OR smth else instead
            continue

        if dataschema[nodetype]['idAtt'].get(child) is not None:
            # 7ot el id wel type fel masterlist faaaaast
        elif dataschema[nodetype][featureAtts] containskey child:
            features[child] = node[child]
        elif dataschema[nodetype][linkAtts] containskey child:
            features['neighbours'][node[child] (child Value (id))] = dataschema[child] (type of child)
        else:
            pass
            # for function in filteringfunctions:
            #     if (filteringfunctions)

    # hat ba2a el nodeid ya fale7 wenta da5el, its the label for this dict
    masterlist[nodetype][nodeid] = features

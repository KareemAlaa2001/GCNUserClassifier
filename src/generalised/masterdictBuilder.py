from queue import Queue



def verify_schema(schema):
    # things I need to verify in the schema: 
    # - neighbourtypes in the linkatt values actually exist up top
    # - TODO see if I am going to include a 'toptype' in the schema

    # building up the list of knowntypes and verifying the existences and data types sof assumed attributes
    knowntypes = []
    for nodetype in schema:
        knowntypes.append(nodetype)

        # checking that key attributes exist

        if schema[nodetype].get('idAtt') is None:
            estring = "This schema is missing an attribute named \'idAtt\' for the unique id for node type: " + str(nodetype)
            raise Exception(estring)

        if schema[nodetype].get('featureAtts') is None:
            estring = "This schema is missing an attribute named \'featureAtts\' containing a list of attribute names associated with the features for node type: " + str(nodetype)
            raise Exception(estring)

        if schema[nodetype].get('linkAtts') is None:
            estring = """This schema is missing an attribute named \'linkAtts\' containing a dict with (attributename: neighbourtype) entries, 
            where attributename is the name of the attribute that has the id of the linked neighbour and neighbourtype is the respective type of that neighbour. This is missing for nodetype: """ + str(nodetype)
            raise Exception(estring)

        # checking that the value passed into the featureAtts attribute is a list
        featureAtts = schema[nodetype].get('featureAtts')
        if not isinstance(featureAtts, list):
            estring = "The value associated with the \'featureAtts\' attribute is not a list for node type: " + str(nodetype) + " , it should have the list of the names of attributes associated with features. If none exist, pass an empty list."
            raise Exception(estring)

        # checking that the value passed into the linkAtts attribute is a dict
        linkAttDict = schema[nodetype].get('linkAtts')
        if not isinstance(linkAttDict, dict):
            estring = "The value associated with the \'linkAtts\' attribute is not a dict for node type: " + str(nodetype) + """ . It should have (attributename: neighbourtype) entries, 
            where attributename is the name of the attribute that has the id of the linked neighbour and neighbourtype is the respective type of that neighbour. If none exist, pass an empty dict."""
            raise Exception(estring)

    # verifying that the values in linkatts point to knowntypes
    for nodetype in schema:
        for linkAtt in schema[nodetype]['linkAtts']:
            if schema[nodetype]['linkAtts'][linkAtt] not in knowntypes:
                estring = "The passed in neighbour type in the link attribute " + str(linkAtt) + " for node type " + str(nodetype) + " does not match one of the node types outlined in the schema!"
                raise Exception(estring)

    return schema
    
    

"""
DATA schema format:

data_schema {
        
        type1: {
            # Toptype: True - if toptype
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




# # processes a passed in data dict containing the whole "graph" according to the schema in order to 
# def processDataDict(datadict, data_schema):
#     # initialising a masterlist, which will contain all of the graph nodes separated into their respective types. Format: dict of lists, 
#     # masterlist = {}
#     # toptype = data_schema['Toptype']

#     # for nodetype in data_schema:
#     #     masterlist[nodetype] = {}

#     masterdict = buildMasterDict(datadict, data_schema)
#     # build # why am i even trying to redesign these
    



    




# def processIndividualNode(nodeid, node, nodetype, dataschema, masterlist, explorationqueue):
#     # filteringfunctions: [String -> Bool] - list of string to bool functions supposed to identify special keys
#     # actionFunctions: list of functions with the same length as filteringfunctions in order to identify what to do with each repsective key
#     features = {}

#     for child in node:

        
#         if isinstance(node[child], dict):
#             explorationqueue.put(node[child])
#             continue

#         if isinstance(node[child], list):
#             # TODO implement: add *node[child] (unpacked list) to explorationqueue OR smth else instead
#             continue

#         if dataschema[nodetype]['idAtt'].get(child) is not None:
#             # 7ot el id wel type fel masterlist faaaaast
#         elif dataschema[nodetype][featureAtts] containskey child:
#             features[child] = node[child]
#         elif dataschema[nodetype][linkAtts] containskey child:
#             features['neighbours'][node[child] (child Value (id))] = dataschema[child] (type of child)
#         else:
#             pass
#             # for function in filteringfunctions:
#             #     if (filteringfunctions)

#     # hat ba2a el nodeid ya fale7 wenta da5el, its the label for this dict
#     masterlist[nodetype][nodeid] = features

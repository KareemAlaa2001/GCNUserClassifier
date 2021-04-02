from queue import Queue

# NOTE - changing masterdict to include an extra "internal-misc" type for any dict entries that are not going to be nodes in the graph

def buildMasterDict(data, schema, toptype=None):
    masterdict = {} 

    verify_schema(schema)
    # NOTE can use whether the passed in data is a dict or a list to determine whether 
    # want to be able to handle data either in a form where it is a dict of lists, each list corresponding to the entries in each type ( this is simple )
    # or to be in the more complex format of a dict tree, where atts point to either attributes of that type or child nodes
    
    
    # if we're using a toptype, first check it is a type in the schema
    # then we want to parrse through. Want to check that entries satisfy that toptype
    if toptype is not None:
        if not verify_toptype(toptype, schema):
            raise Exception("Toptype passed in is not in the list of types outlined in the schema!")

        # if the data passed in is in a list form: could be a list of nodes of the same type or mixed types
        if isinstance(data, list):

            # since a toptype was set, then all entries in top list must be of that type
            # make that check while building the queue of nodes to explore
            toExplore = Queue()

            for topentry in data:
                if entrySatisfiesNodeType(topentry, schema[toptype]):
                    toExplore.put((topentry,toptype))

                else: 
                    raise Exception("A toptype was passed in, but not all entries in the list satisfy that type!")

            # now done with verification, time to actually build the masterdict!

            # TODO implement this
            while not toExplore.empty():
                entry, entrytype = toExplore.get()

                entryDict = {}
                entrySchema = schema.get(entrytype)
                if entrySchema is None:
                    raise Exception("Passed in entry type does not exist in the schema!")
                # looping over all the attributes in the entry. Either this att links to an individual value, a list or a dict
                # The list could either be a list of values or list of dicts
                for att in entry:
                    value = entry.get(att)

                    if att in entrySchema.get('linkAtts'):
                        if isinstance(value, dict):
                            neighbourtype = entrySchema.get('linkAtts').get(att)
                            toExplore.put((value,entrySchema.get('linkAtts').get(att)))

                            neighbouridatt = schema.get(neighbourtype).get('idAtt')
                            entryDict[att] = value.get(neighbouridatt)
                        elif isinstance(value, list):
                            neighbourids = []
                            for elem in value:
                                
                                if isinstance(elem, dict):
                                    neighbourtype = entrySchema.get('linkAtts').get(att)
                                    toExplore.put((elem,neighbourtype))

                                    neighbouridatt = schema.get(neighbourtype).get('idAtt')
                                    neighbourids.append(elem.get(neighbouridatt))
                                else: 
                                    neighbourids.append(elem)

                            entryDict[att] = neighbourids
                        else:
                            # normal att for link - use as id of linked node
                            entryDict[att] = value

                    elif att in entrySchema.get('featureAtts'):
                        if isinstance
                        pass  # todo - figure out this scenario where a feature points to a dict
                    else:
                        pass # can allow for custom attributes here 

                

            



            

        
    # TODO need to decide what to process if toptypes is None
    # NOTE could accept the following:
    #   list of nodes of mixed types
    #   dict containing single node - SHOULD HAVE BEEN COVERED BY TOPTYPE
    #   Any other formats will have custom attributes - must first figure out the stuff with fixed att names
    #

    if verify_masterdict(data, schema):
        return data

    # NOTE a possible solution is to accept a few different formats for the input data

    pass
    # if thedata is in the former format
    # pass ( for now)

    # else:
    # need to verify that toptype is not none
    # then we open the item list and treat the entries in that list as entries of that type

def entrySatisfiesNodeType(entry, ntype):
    idAtt = ntype.get('idAtt')

    if idAtt not in entry:
        return False

    featureAtts = ntype.get('featureAtts')
    linkAtts = ntype.get('linkAtts')

    for att in entry:
        if att not in featureAtts and att not in linkAtts:
            return False
    
    return True

def verify_toptype(toptype, schema):
    if toptype not in schema.keys():
        return False
    else:
        return True


# Verifies the following:
# passed in data has a dict type with the same children keys (nodetypes) as the schema
# the values mapped by those keys are lists
# Each entry in that list has the unique idAtt as named
# If the idAtt is there, all entries in a certain nodetype have unique ids
def verify_masterdict(inp, schema):
    if isinstance(inp, dict) and inp.keys() == schema.keys():
        
        for ntype in inp:
            encounteredids = {}
            if isinstance(inp[ntype],list):
                entries = inp[ntype]

                for entry in entries:
                    # making sure that each entry contains the id attribute
                    if entry.get(schema.get(ntype).get('idAtt')) is not None:
                        id = entry.get(schema.get(ntype).get('idAtt'))
                        if encounteredids.get(id) is not None:
                            estring = "Data contains duplicate ids for id " + str(id) + " in node type " + ntype + " !"
                            raise Exception(estring)
                        else:
                            encounteredids[id] = 1
                    else:
                        return False
            else:
                return False

        return True
    else:
        return False

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

import fvBuilder
import graphBuilder
from stanza.server import CoreNLPClient
from extraction import *
from helpers import isComment, isPost, isUser


def buildWholePipeline(data_dir, fileNames):
    # maps the "nodetype" to the root
    nodeTypeRoots = {}

    #maps the filename to the nodetype
    fileNameNodeTypes = {}


    for name in fileNames:
        nodetype = name.lower()
        fileNameNodeTypes[name] = nodetype
        fname = data_dir + name + ".xml"
        nodeTypeRoots[nodetype] = ET.parse(fname).getroot()
    
    # contains a dict with each entry having a mapping nodetype: list of nodes in that type
    data_dict = {}

    # code to extract the list of nodes of each type
    for nodetype in nodeTypeRoots:
        data_dict[nodetype] = extractNodeType(root=nodeTypeRoots[nodetype], )

# This is VERY SO specific, but it does the job 
def extractNodeType(root, filterFunc, **specialTypeArgs):

    if filterFunc is None:
        return listChildrenAttrib(root)
    else:
        if specialTypeArgs.get("knowntype") is not None:
            knowntype = specialTypeArgs.get("knowntype")

            if knowntype == 'stackexchangepost':
                return extractPosts(filterFunc, root)

            elif knowntype == 'stackexchangecomment':
                if specialTypeArgs.get('postsDict') is not None:
                    postsDict = specialTypeArgs.get('postsDict')
                    return extractComments(filterFunc, root, postsDict)
                else:
                    raise Exception("""Special type \"stackexchangecomment\" entered, 
                    but there was no named argument \"postsDict\" containing a dictionary of entries (postid:attributeDict) """)

            elif knowntype == 'stackexchangeuser':
                if specialTypeArgs.get('useriddict') is not None:
                    useriddict = specialTypeArgs.get('useriddict')
                    return extractConnectedUsers(root, useriddict)
                else:
                    raise Exception("""Special type \"stackexchangeuser\" entered, 
                    but there was no named argument \"useriddict\" containing a dictionary of entries with keys (userid) """)




    pass

def buildFVsAndGraphs(posts, users, comments):
    with CoreNLPClient(
            annotators=['tokenize','ssplit','pos','lemma','ner'],
            timeout=30000,
            memory='16G') as client:
        
        gcngraph, data = graphBuilder.buildGCNGraph(posts, users, comments)

        fvmatrix = [buildNodeFV(node, client) for node in data]

        # alright so supposedly gcngraph and fvmatrix have the lists of indexed nodes and the neighbourhood relationships between them
        # TODO write a function for a training-test split, start fleshing out the API to make it more extensible
        # TODO implement functionality to accept labels in for the data as well

# wrapper function that generalises featurevector building
def buildNodeFV(node, client):

    if isPost(node):
        return fvBuilder.postToFV(node, client)
    elif isUser(node):
        return fvBuilder.userToFV(node, client)
    elif isComment(node):
        return fvBuilder.commentToFV(node, client)
    else:
        raise Exception("Passed in node was not one of the 3 currently recognized node types!")


def main():
    data_dir = "../../datasets/meta.stackoverflow.com/"
    fileNames = ["Posts", "Comments", "Users"]
    buildWholePipeline(data_dir, fileNames)

if __name__ == '__main__':
    main()
        
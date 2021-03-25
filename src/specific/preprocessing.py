import fvBuilder
import graphBuilder
from stanza.server import CoreNLPClient
from extraction import recentComments, recentPosts, recentUsers
from helpers import isComment, isPost, isUser

def buildFVsAndGraphs(posts, users, comments):
    with CoreNLPClient(
            annotators=['tokenize','ssplit','pos','lemma','ner'],
            timeout=30000,
            memory='16G') as client:
        
        gcngraph, data = graphBuilder.buildGCNGraph(posts, users, comments)

        fvmatrix = [buildNodeFV(node, client) for node in data]

        # alright so supposedly gcngraph and fvmatrix have the lists of indexed nodes and the neighbourhood relationships between them
        # TODO write a function for a training-test split, start fleshing out the API to make it more extensible

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

   
        
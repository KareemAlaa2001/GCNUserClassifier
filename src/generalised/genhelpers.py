import re

def extractPostId(headerstring):
    postmatch = re.search(r'post_\d+', headerstring)
    if postmatch is not None:
        pstr = postmatch.group()
        return int(pstr.split("_")[1])
    else:
        raise Exception("The passed string doesn't have an embedded threadid!")

def extractThreadId(headerstring):
    threadmatch = re.search(r'thread_\d+', headerstring)
    if threadmatch is not None:
        tstr = threadmatch.group()
        return int(tstr.split("_")[1])
    else:
        raise Exception("The passed string doesn't have an embedded postid!")

def initEmptyTypesDict(schema):
    typesdict = {}

    for nodetype in schema:
        typesdict[nodetype] = {}

    return typesdict
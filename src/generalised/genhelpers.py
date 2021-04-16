import re
from lib.stackoverflowproc.extraction import recentUsers, recentPosts, recentComments

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

def alldictkeysarepositiveints(data):
    return all(list(map(lambda att: isinstance(att, int) and att >= 0,data)))

def alllistmembersarepositiveints(data):
    return all(list(map(lambda att: isinstance(att, int) and att >= 0,data)))

def alldictvaluesatisfytype(data,type):
    return all(list(map(lambda att: isinstance(data[att],type) , data)))

def allkeyssatisfytype(data, type):
    return all(list(map(lambda att: isinstance(att, type),data)))

def allmemberssatisfyanytypes(data, types):
    return all(list(map(lambda member: any(list(map(lambda t: isinstance(member,t), types))),data)))


# def main():
    # print(len(recentUsers), len(recentPosts), len(recentComments)) 

# if __name__ == '__main__':
#     main()
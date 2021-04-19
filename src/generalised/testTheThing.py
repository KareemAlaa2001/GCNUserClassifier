from corpusreader import CorpusReader, FileExtractor
from lib.stackoverflowproc.extraction import recentUsers, recentPosts, recentComments
from lib.stackoverflowproc.fvBuilder import extractFeatureVectorsWithoutNER, extractFeaturevectors
from stanza.server import CoreNLPClient
from masterdictGraphBuilder import MasterdictGraphProcessor
from dataHandler import GCNRunner, convertIdFVGuideToFVIndexGuide
import lib.stackoverflowproc.labelBuilder as labelBuilder
import random 
import os.path
import json

"""
export CORENLP_HOME=/Users/kareem/UniStuff/3rd\ Year/3rdYearProject/Libraries/stanford-corenlp-4.2.0
"""

# TODO re-implement the dataset splitting functionality to belong to the generalized library rather than just the SO specific stuff
# TODO consider replacing the whole GCN code lib with the DGL implementation



def test_run():
    data_obj = {'user':recentUsers, 'comment':recentComments, 'post':recentPosts}

    schema = {
        'user': {
            'idAtt': 'Id',
            'featureAtts': [],
            'linkAtts': {

            }
        },
        'post': {
            'idAtt': 'Id',
            'featureAtts': [],
            'linkAtts': {
                'ParentId': 'post',
                'OwnerUserId': 'user'
            }
        }, 
        'comment': {
            'idAtt': 'Id',
            'featureAtts': [],
            'linkAtts': {
                'UserId': 'user',
                'PostId': 'post'
            }

        }

    }

    reader = CorpusReader(True)

    masterdict = reader.readCorpus(data_obj, schema) 

    mdgraphproc = MasterdictGraphProcessor()

    gcngraph, idGraph, indexGuide = mdgraphproc.buildGraphsFromMasterDict(masterdict, schema)

    print("Built the adjacency graph!!")

    # with CoreNLPClient(
    #         annotators=['tokenize','ssplit','pos','lemma','ner'],
    #         timeout=200000,
    #         memory='16G', be_quiet=True) as client:


    idFVMap = extractFeatureVectorsWithoutNER(recentPosts, recentUsers, recentComments)
    print("Extracted all of the FVs!")
    # indexFvMap = convertIdFVGuideToFVIndexGuide(idFVMap, indexGuide)

    
    # dummyLabels = labelBuilder.buildUnlabbelledLabelsDict(indexGuide, userLabels, 2)
    print("splitting the dataset...")
    train_fvs, train_labels, test_fvs, test_labels, test_indices, train_all_fvs, train_all_labels = split_dataset(recentUsers, indexGuide, idFVMap, 0.8)
    print("dataset split complete! Running GCN now:")
    # allLabels = labelBuilder.buildAllLabelsDict(indexGuide, userLabels, 2)

    # labels_train, labels_train_all, labels_test = labelBuilder.splitDatasetLabels(userLabels, dummyLabels, 0.7)
    gcnrunner = GCNRunner(train_fvs, test_fvs, train_labels, test_labels, train_all_fvs, train_all_labels, test_indices, gcngraph)
    gcnrunner.train_gcn()




        



def main():
    data_obj = {'user':recentUsers, 'comment':recentComments, 'post':recentPosts}

    schema = {
        'user': {
            'idAtt': 'Id',
            'featureAtts': [],
            'linkAtts': {

            }
        },
        'post': {
            'idAtt': 'Id',
            'featureAtts': [],
            'linkAtts': {
                'ParentId': 'post',
                'OwnerUserId': 'user'
            }
        }, 
        'comment': {
            'idAtt': 'Id',
            'featureAtts': [],
            'linkAtts': {
                'UserId': 'user',
                'PostId': 'post'
            }

        }


    }
    reader = CorpusReader(True)

    masterdict = reader.readCorpus(data_obj, schema) 

    mdgraphproc = MasterdictGraphProcessor()

    gcngraph, idGraph, indexGuide = mdgraphproc.buildGraphsFromMasterDict(masterdict, schema)

    print("Built the adjacency graph!!")

    with CoreNLPClient(
            annotators=['tokenize','ssplit','pos','lemma','ner'],
            timeout=200000,
            memory='16G', be_quiet=True) as client:
        

        if os.path.isfile("fvmap.json") and os.path.getsize("fvmap.json") > 0:
            print("fvmap file already exists, rejoice! the training time will be much less this time")
            idFVMap = json.load(open("fvmap.json","r"))
        else:
            idFVMap = extractFeaturevectors(recentPosts, recentUsers, recentComments, client)

        print("Extracted all of the FVs!")
        # indexFvMap = convertIdFVGuideToFVIndexGuide(idFVMap, indexGuide)

        
        # dummyLabels = labelBuilder.buildUnlabbelledLabelsDict(indexGuide, userLabels, 2)
        print("splitting the dataset...")
        train_fvs, train_labels, test_fvs, test_labels, test_indices, train_all_fvs, train_all_labels = split_dataset(recentUsers, indexGuide, idFVMap, 0.8)
        print("dataset split complete! Running GCN now:")
        # allLabels = labelBuilder.buildAllLabelsDict(indexGuide, userLabels, 2)

        # labels_train, labels_train_all, labels_test = labelBuilder.splitDatasetLabels(userLabels, dummyLabels, 0.7)
        gcnrunner = GCNRunner(train_fvs, test_fvs, train_labels, test_labels, train_all_fvs, train_all_labels, test_indices, gcngraph)
        gcnrunner.train_gcn()

        


# takes in: indexFvMap, indexGuide, 
def split_dataset(users, indexGuide, idFvGuide, splitsize):

    # breakdown: 
    # need to get sheriff indexes, then split those into a training and test set
    # do the same for the indexes of the other users
    # test set & its labels: get fvs of users above and their labels, put em in a matrix in the same order
    # training set & its labels: same as above but for train
    # all_train_set: get the above set and add in all of the nodes & shuffleeee, make sure shuffles are consistent between a set of fvs and its labels
    # test_indicies - take the "indexGuide" values for the users in the test set

    sheriffIds = labelBuilder.getSheriffBadgeUserIds(users)
    
    num_train_sheriffs = int(splitsize*len(sheriffIds))

    train_sheriff_ids = sheriffIds[:num_train_sheriffs]
    test_sheriff_ids = sheriffIds[num_train_sheriffs:]

    otherusers = buildNonSheriffIdList(users, sheriffIds)

    num_train_nonsheriffs = int(splitsize*len(otherusers))

    train_nonsheriff_ids = otherusers[:num_train_nonsheriffs]
    test_nonsheriff_ids = otherusers[num_train_nonsheriffs:]

    train_user_ids = train_sheriff_ids + train_nonsheriff_ids

    test_user_ids = test_sheriff_ids + test_nonsheriff_ids

    random.shuffle(train_user_ids)
    random.shuffle(test_user_ids)

    user_label_dict = labelBuilder.buildUserLabelsDict(users, indexGuide, sheriffIds)
    # Let's first do the train_set:
    train_fvs = []
    train_labels = []

    for userid in train_user_ids:
        userindex = indexGuide['user'][userid]
        userfv = idFvGuide['user'][userid]
        userlabel = user_label_dict[userindex]

        train_fvs.append(userfv)
        train_labels.append(userlabel)

    # now the test set:

    test_fvs = []
    test_labels = []
    test_indices = []

    for userid in test_user_ids:
        userindex = indexGuide['user'][userid]
        userfv = idFvGuide['user'][userid]
        userlabel = user_label_dict[userindex]

        test_fvs.append(userfv)
        test_labels.append(userlabel)
        test_indices.append(userindex)

    # now for the train_all:

    train_all_fvs = []
    train_all_labels = []


    # train_all_indexes = []

    for userid in train_user_ids:
        userindex = indexGuide['user'][userid]

        train_all_fvs.append(idFvGuide['user'][userid])
        train_all_labels.append(user_label_dict[userindex])
    
    for nodetype in indexGuide:
        if nodetype == 'user':
            continue
        else:
            typeindexGuide = indexGuide[nodetype]
            for nodeid in typeindexGuide:
                nodindex = indexGuide[nodetype][nodeid]

                train_all_fvs.append(idFvGuide[nodetype][nodeid])
                train_all_labels.append([0,0])

    # need to shuffle the fvs and labels simultaneously

    indices = [i for i in range(len(train_all_fvs))]
    random.shuffle(indices)

    train_all_fvs = [train_all_fvs[i] for i in indices]
    train_all_labels = [train_all_labels[i] for i in indices]

    return train_fvs, train_labels, test_fvs, test_labels, test_indices, train_all_fvs, train_all_labels
    
# def build_train_all_indexes(train_user_ids, indexGuide):
#     train_all_indexes = []

#     for userid in train_user_ids:
#         userindex = indexGuide['user'][userid]

#         train_all_indexes.append(userindex)
    
#     for nodetype in indexGuide:
#         if nodetype == 'user':
#             continue
#         else:
#             typeindexGuide = indexGuide[nodetype]
#             for nodeid in typeindexGuide:
#                 train_all_indexes



def buildNonSheriffIdList(users, sheriffIds):
    nonsheriffids = []
    for user in users:
        userid = user.get('Id')
        
        if userid not in sheriffIds:
            nonsheriffids.append(userid)

    return nonsheriffids
            

if __name__ == '__main__':
    main()
    # test_run()


"""
TODO:

Train GCN with SO stuff

Test out inference to make sure it works 

Create some different labels to classify the users/posts

USE SEGMENTATION TO CLASSIFY USERS WITH A SUBSET OF THE TEST SET
- this will allow me to show weaknesses on smaller datasets with short posts? with long posts? with X? with Y?

- can use posts by n00b users vs experts

- can use short vs long posts

- can be able to breakdown the performance of GCN on different contexts and understand in what ways its strong vsv weak and why
"""


"""
could have a core benchmark to extract users as we said for classification

can then do an extra benchmark of adding domain specific regex (regex on java/python function or module names) to the features


evaluate performance with F1 score

Run analysis with different types of user groupings - see if the graph is better or worse of diff types of users

Run analysis with different types of posts
"""

"""

Stuart idea for regex-based stuff like URLs and namespaces:

Go the regex as a preproc step before corenlp runm and replace all instances with a combination of chars of my own, 
then if it is recognized add it as muy own feature later - might be a way to use stanza and avoid corenlp slowness

"""


"""

Different Runs:

Class for moderators 

Class for expert/novice - multiclass by number of years

Class for upvote/downvote
"""

"""
Stuart usually does scripts, take in dataset/model name, test set to run everything for me
"""

"""
Write up the report with placeholders to describe the experiments


allow for tables with the different F1 scores - precision - recall - F1 - 
Start writing ASAP
Skeleton - bullet points fillout -  

"""


"""
My demo might have a presentation with the problem, GCN architecture, run it, initial results, 

IDEA: Show graphs and results connected with the data in a meaningful way while narrating and demostrating my understanding
"""
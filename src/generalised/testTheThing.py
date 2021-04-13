from corpusreader import CorpusReader, FileExtractor
from lib.stackoverflowproc.extraction import recentUsers, recentPosts, recentComments
from lib.stackoverflowproc.fvBuilder import extractFeaturevectors
from stanza.server import CoreNLPClient
from masterdictGraphBuilder import MasterdictGraphProcessor
from dataHandler import GCNRunner, convertIdFVGuideToFVIndexGuide
import lib.stackoverflowproc.labelBuilder as labelBuilder
import random 

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

    masterdict = reader.readCorpus(data_obj, schema) # TODO implement this whole setup out with the SO_ds and make it happennnn

    mdgraphproc = MasterdictGraphProcessor()

    gcngraph, idGraph, indexGuide = mdgraphproc.buildGraphsFromMasterDict(masterdict, schema)

    print("Built the adjacency graph!!")

    with CoreNLPClient(
            annotators=['tokenize','ssplit','pos','lemma','ner'],
            timeout=200000,
            memory='16G', be_quiet=True) as client:

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
    
def build_train_all_indexes(train_user_ids, indexGuide):
    train_all_indexes = []

    for userid in train_user_ids:
        userindex = indexGuide['user'][userid]

        train_all_indexes.append(userindex)
    
    for nodetype in indexGuide:
        if nodetype == 'user':
            continue
        else:
            typeindexGuide = indexGuide[nodetype]
            for nodeid in typeindexGuide:
                train_all_indexes
                
    

def buildNonSheriffIdList(users, sheriffIds):
    nonsheriffids = []
    for user in users:
        userid = user.get('Id')
        
        if userid not in sheriffIds:
            nonsheriffids.append(userid)

    return nonsheriffids
            

if __name__ == '__main__':
    # test_labelBuilder()
    main()
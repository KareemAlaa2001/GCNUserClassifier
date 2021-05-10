from corpusreader import SchemaCorpusProcessorFactory
from lib.stackoverflowproc.extraction import recentUsers, recentPosts, recentComments, recentBadges
from lib.stackoverflowproc.fvBuilder import extractFeaturevectors
from stanza.server import CoreNLPClient
from masterdictGraphBuilder import MasterdictGraphProcessor
from dataHandler import GCNRunner, convertIdFVGuideToFVIndexGuide
import lib.stackoverflowproc.labelBuilder as labelBuilder
import os.path
import json
import numpy as np
from genhelpers import convertDictSetToListSet


def run_adj_dict_building_pipeline():
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
                'OwnerUserId': 'user',
                'RelatedPostId': 'post'
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
    procFactory = SchemaCorpusProcessorFactory()

    corpProc = procFactory.getCorpusProcessor()

    masterdict = corpProc.readCorpus(data_obj, schema) 

    mdgraphproc = MasterdictGraphProcessor()

    gcngraph, idGraph, indexGuide = mdgraphproc.buildGraphsFromMasterDict(masterdict, schema)

    return gcngraph, idGraph, indexGuide


def run_dataset_building_pipeline(input_label_set=None):
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
                'OwnerUserId': 'user',
                'RelatedPostId': 'post'
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
    procFactory = SchemaCorpusProcessorFactory()

    corpProc = procFactory.getCorpusProcessor()

    masterdict = corpProc.readCorpus(data_obj, schema) 

    mdgraphproc = MasterdictGraphProcessor()

    gcngraph, idGraph, indexGuide = mdgraphproc.buildGraphsFromMasterDict(masterdict, schema)

    numLinks = 0
    for index in gcngraph:
        numLinks += len(gcngraph[index])

    numLinks /= 2

    print("Number of edges in the graph:",numLinks)
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
        indexFvMap = convertIdFVGuideToFVIndexGuide(idFVMap, indexGuide)

        if input_label_set is None:
            indexLabelMap, userLabels = labelBuilder.getAllLabelsUsingBadgeClass(recentUsers, recentBadges, indexGuide)
        else:
            if input_label_set == "BadgeClass":
                indexLabelMap, userLabels = labelBuilder.getAllLabelsUsingBadgeClass(recentUsers, recentBadges, indexGuide)
            elif input_label_set == "NicePostBin":
                indexLabelMap, userLabels = labelBuilder.getAllLabelsUsingNiceQuestionAnswerBinary(recentUsers, recentBadges, indexGuide)
            else:
                indexLabelMap, userLabels = labelBuilder.getAllLabelsUsingNiceQuestionAnswerMulticlass(recentUsers, recentBadges, indexGuide)
        # unconnectedindexes = []

        # for index in indexFvMap:
        #     if gcngraph.get(index) is None:
        #         unconnectedindexes.append(index)

        # print("Number of unconnected nodes:",len(unconnectedindexes))

        # constructing the labels
        labelledindices = []
        for userindex in userLabels:
            labelledindices.append(userindex)

        

        fvslist = convertDictSetToListSet(indexFvMap)
        labelslist = convertDictSetToListSet(indexLabelMap)
        num_classes = len(labelslist[0])

        # NOTE this contains MANY dummy zero labels, will be ignored by constructing the masks from the labelled indices list
        labels_ints = np.argmax(np.array(labelslist),1).tolist()
        print("Creating DGL Dataset")

        return fvslist, labelledindices, labels_ints, gcngraph, num_classes
        # return fvslist, labelledindices, labels_ints, gcngraph, num_classes

# if __name__ == '__main__':
#     main()



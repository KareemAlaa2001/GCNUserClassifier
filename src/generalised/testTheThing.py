"""
from corpusreader import CorpusReader, FileExtractor
from lib.stackoverflowproc.extraction import recentUsers, recentPosts, recentComments
from lib.stackoverflowproc.fvBuilder import extractFeaturevectors
from stanza.server import CoreNLPClient
from masterdictGraphBuilder import MasterdictGraphProcessor
from dataHandler import GCNRunner, convertIdFVGuideToFVIndexGuide
import lib.stackoverflowproc.labelBuilder as labelBuilder

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

    with CoreNLPClient(
            annotators=['tokenize','ssplit','pos','lemma','ner'],
            timeout=30000,
            memory='16G') as client:
        idFVMap = extractFeaturevectors(recentPosts, recentUsers, recentComments, client)

        indexFvMap = convertIdFVGuideToFVIndexGuide(idFVMap, indexGuide)

        # gcnrunner = GCNRunner() # TODO deal with stackoverflow labels
"""
import lib.stackoverflowproc.labelBuilder as labelBuilder


def test_labelBuilder():
    labelBuilder.getSheriffBadgeDisplayNames()



if __name__ == '__main__':
    test_labelBuilder()
    # main()
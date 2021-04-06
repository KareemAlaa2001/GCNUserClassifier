from genhelpers import *


# class for converting the set of passed in featurevectors into a csr_matrix object
# accepts either {nodeid: [fv]} or [[fv]] indexed
class FVHandler:

    def __init__(self):
        pass

    def handleFeatureVectors(self, featurevectors):
        if isinstance(featurevectors, dict):
            pass
        elif isinstance(featurevectors, list):

            if allkeyssatisfytype(featurevectors, list):
                pass # TODO complete verification then convert data to a csr_matrix # TODO allow for a quick splits implementation

        else:
            raise ValueError(featurevectors)

def verifyFvList(fvlist):
    if allkeyssatisfytype(fvlist, list):
        



def verifyFvDict(fvdict):





# TODO implement a class for handling ground truths


# TODO implement a wrapper for running GCN


# TODO test this whole damn thing 
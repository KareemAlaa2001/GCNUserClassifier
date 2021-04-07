from genhelpers import *
import scipy.sparse as sp

# class for converting the set of passed in featurevectors into a csr_matrix object
# accepts either {nodeid: [fv]} or [[fv]] indexed
class FVHandler:

    def __init__(self, ):
        pass

    def to_csr_mat(self, featurevectors):
        if isinstance(featurevectors, sp.csr_matrix):
            return featurevectors

        if isinstance(featurevectors, dict):
            if verifyFvDict(featurevectors):
                mat = convertfvdict2dList(featurevectors)
                csr_mat = sp.csr_matrix(mat)
                return csr_mat
            else:
                raise ValueError("Unknown issue in the featurevectors object format")
        elif isinstance(featurevectors, list):
            if verifyFvList(featurevectors):
                csr_mat = sp.csr_matrix(featurevectors)
                return csr_mat
            else:
                raise ValueError("Unknown issue in the featurevectors object format")

        else:
            raise ValueError(featurevectors)


class GCNRUnner:

    def __init__(self, labeled_train, test_instances, train_labels, test_labels, all_train, all_train_labels, test_indicies, adj_graph):
        pass


def convertfvdict2dList(fvdict):
    mat = [[]] * len(fvdict)

    for i in fvdict:
        mat[i] = fvdict[i]

    return mat


def verifyFvList(fvlist):
    if allkeyssatisfytype(fvlist, list):
        it = iter(fvlist)
        the_len = len(next(it))
        if not all(len(l) == the_len for l in it):
            raise ValueError('not all lists have the same length!')


        for l in fvlist:
            if allmemberssatisfyanytypes(l, [float, int]):
                pass # do nothing, this list checks out# checking that fvlist is a list of lists of ints/floats
            else:
                estr = "Not all entries in this list are ints/floats"
                raise ValueError(estr)
        
        return True
    else:
        raise ValueError("The fv passed in is a list but not a list of lists!")




def verifyFvDict(fvdict):
    if alldictkeysarepositiveints(fvdict):
        if alldictvaluesatisfytype(fvdict, list):
            it = iter(fvdict)
            the_len = len(fvdict[next(it)])
            if not all(len(fvdict[ind]) == the_len for ind in it):
                raise ValueError('not all lists have the same length!')

            for index in fvdict:
                if allmemberssatisfyanytypes(fvdict[index], [float, int]):
                    pass # do nothing, this list checks out 
                else:
                    estr = "ValueError: Not all entries in this list are ints/floats"
                    raise ValueError(estr)
            return True
        else:
            raise ValueError("Not all of the featurevectors mapped to be the index keys are lists!")

    else:
        raise ValueError("Not all keys in this dict are positive integers, so not all are node indexes!")


# TODO implement a class for handling ground truths


# TODO implement a wrapper for running GCN


# TODO test this whole damn thing 
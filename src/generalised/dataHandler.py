from genhelpers import *
import scipy.sparse as sp
import numpy as np

# class for converting the set of passed in featurevectors into a csr_matrix object
# accepts either {nodeid: [fv]} or [[fv]] indexed
class FVHandler:

    def __init__(self, train_labelled, test_instances, train_labels, test_labels, all_train, all_train_labels):

        train_labelled = self.handleFeaturevectors(train_labelled)
        train_all = self.handleFeaturevectors(all_train)
        test_instances = self.handleFeaturevectors(test_instances)

        labels_train = self.handleLabels(train_labels)
        labels_test = self.handleLabels(test_labels)
        labels_all_train = self.handleLabels(all_train_labels)
        

        if checkEqualLengths(train_labelled, labels_train):
            self.train_labelled = train_labelled
            self.train_labels = labels_train
        else:
            raise ValueError("Lengths of training labels and training set passed in were not equal!")

        if checkEqualLengths(train_all, labels_all_train):
            self.train_all = train_all
            self.labels_all_train = labels_all_train
        else:
            raise ValueError("Number of featurevectors for all training nodes and the number of labels passed in were not equal! Use lists of 0s for unlabbeled node labels")

        if checkEqualLengths(test_instances, labels_test):
            self.test_instances = test_instances
            self.test_labels = labels_test
        else:
            raise ValueError("Lengths of test labels and test set passed in were not equal!")


    def handleLabels(self, labels):
        if isinstance(labels, np.array):
            return labels

        if isinstance(labels, dict):
            if verifyFvDict(labels):
                mat = convertfvdict2dList(labels)
                if checkOHEOrZeroes(mat):
                    np_arr = np.array(mat)
                    return np_arr
            else:
                raise ValueError("Unknown issue in the labels object format")
        elif isinstance(labels, list):
            if verifyFvList(labels):
                if checkOHEOrZeroes(labels):
                    np_arr = np.array(labels)
                    return np_arr
            else:
                raise ValueError("Unknown issue in the labels object format")

        else:
            raise ValueError(labels)

    def handleFeaturevectors(self, featurevectors):
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


class GCNRunner:

    # NOTE any featurevectors are in a csr_matrix. NOTE any labels are in a numpy array. NOTE test_indices is a list. NOTE adj_graph is a dict
    def __init__(self, train_labelled, test_instances, train_labels, test_labels, all_train, all_train_labels, test_indices, adj_graph):
        self.fvHandler = FVHandler(train_labelled,test_instances,train_labels, test_labels, all_train, all_train_labels)
        if verify_test_indices(test_indices):
            self.test_indices = test_indices

        self.adj_graph = adj_graph

    def train_gcn(self):
        pass



def verify_test_indices(test_indices, all_train):
    if isinstance(test_indices, list):
        if alllistmembersarepositiveints(test_indices):
            if max(test_indices) < all_train.get_shape()[0]:
                return True
            else:
                raise ValueError("Test indices list has indices larger than the number of elements in the training set!")
        else:
            raise ValueError("Not all elements in the test indices list are nonnegative ints!")
    else:
        raise ValueError("Test indices is not a list!")


def checkEqualLengths(fvs, labels):
    fv_shape = fvs.get_shape()
    num_fvs = fv_shape[0]
    labelsShape = labels.shape
    num_labels = labelsShape[0]
    
    if num_fvs == num_labels:
        return True

    else:
        return False


def checkOHEOrZeroes(labels):
    if all(list(map(isOHEOrZeroes, labels))):
        return True

    else: 
        return False

def isOHEOrZeroes(l):
    if isAllZeroes(l) or isOHE(l):
        return True

    else:
        return False

def isAllZeroes(l):
    if len(list(filter(lambda x: x == 0, l))) == len(l):
        return True
    else:
        return False

def isOHE(l):
    if sum(l) == 1 and len(list(filter(lambda x: x != 0, l))) == 1:
        return True

    else: 
        return False

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


def handleLabels(labels):
        if isinstance(labels, np.ndarray):
            return labels

        if isinstance(labels, dict):
            if verifyFvDict(labels):
                mat = convertfvdict2dList(labels)
                if checkOHEOrZeroes(mat):
                    np_arr = np.array(mat)
                    return np_arr
            else:
                raise ValueError("Unknown issue in the labels object format")
        elif isinstance(labels, list):
            if verifyFvList(labels):
                if checkOHEOrZeroes(labels):
                    np_arr = np.array(labels)
                    return np_arr
            else:
                raise ValueError("Unknown issue in the labels object format")

        else:
            raise ValueError(labels)

def handleFeaturevectors(featurevectors):
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

def main():
    test_fvs = [[0,1,0,1,1],[1,0,1,0,1]]
    test_labels = [[1,0],[0,1]] 

    # handler = FVHandler()
    handled_fv = handleFeaturevectors(test_fvs)
    handled_labels = handleLabels(test_labels)

    print(handled_fv)
    print(handled_labels)

    checkEqualLengths(handled_fv, handled_labels)

if __name__ == '__main__':
    main()

# TODO implement a class for handling ground truths


# TODO implement a wrapper for running GCN


# TODO test this whole damn thing 
"""
    Loads input data from gcn/data directory

    ind.dataset_str.x => the feature vectors of the training instances as scipy.sparse.csr.csr_matrix object;
    ind.dataset_str.tx => the feature vectors of the test instances as scipy.sparse.csr.csr_matrix object;
    ind.dataset_str.allx => the feature vectors of both labeled and unlabeled training instances
        (a superset of ind.dataset_str.x) as scipy.sparse.csr.csr_matrix object;
    ind.dataset_str.y => the one-hot labels of the labeled training instances as numpy.ndarray object;
    ind.dataset_str.ty => the one-hot labels of the test instances as numpy.ndarray object;
    ind.dataset_str.ally => the labels for instances in ind.dataset_str.allx as numpy.ndarray object;
    ind.dataset_str.graph => a dict in the format {index: [index_of_neighbor_nodes]} as collections.defaultdict
        object;
    ind.dataset_str.test.index => the indices of test instances in graph, for the inductive setting as list object.

    All objects above must be saved using python pickle module.

    :param dataset_str: Dataset name
    :return: All data input files loaded (as well the training/test data).
""" 
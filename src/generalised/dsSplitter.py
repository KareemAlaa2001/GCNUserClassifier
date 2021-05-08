from abc import ABCMeta
import random
import numpy as np
"""

This modules is supposed to be the connecting module between the creation of FVs and labels with 
the data formats taken in by the fvHandler and GCNRunner classes

Might be worth mapping out the sitaution around this module:

INPUT SITUATION:

So both the masterdictGraphBuilder and the indexGraphBuilder output a graph of {node_index: [neighbour_indexes]}

masterdictGraphBuidler also spits out an idGraph and indexGuide

Can assume in both cases they gotta build some kind of fv and label holding matrices/ dicts

OUTPUT SITUATION:

wanna output:

train_fvs, train_labels, test_fvs, test_labels, test_indices, train_all_fvs, train_all_labels

Need to split fvs into labelled fvs and unlabelled fvs, then split the labelled fvs into train and test

also need to hold on to the original indices of the fvs for the test_indices obj
"""


"""
If I'm just taking all of the FVs and all of the labels, I gotta split these to the needed formats as detailed above
"""

class DSSplitter:
    def __init__(self, fvs, labels, train_size):
        self.fvs = fvs
        self.labels = labels 
        self.train_size = train_size

    def split_dataset(self):
        return split_dataset(self.fvs, self.labels, self.train_size)

# can either assume dicts or lists for the passed in fvs and labels

# either accepts {index: [fv]} or [[fv]], using index of [fv] for the index info
def split_dataset(fvs, labels, train_size):

    if train_size > 1 or train_size < 0:
        raise ValueError("train_size should be between 0 and 1!!")

    if len(fvs) != len(labels):
        raise ValueError("Lengths of fvs and labels not equal!!")
 
    train_fvs = []
    train_labels = []
    test_fvs = []
    test_labels = []
    train_all_fvs = []
    train_all_labels = []
    test_indices = []
    
    labelled_indices, unlabelled_indices = extractLabelledUnlabelledIndices(labels)

    ## need to now split the labelled dataset into training and testing sets using the indices
    ## CHECK IF I NEED TO REMOVE THE SHUFFLING HERE TO MAKE THIS WORK LMAO
    random.seed(123)
    random.shuffle(labelled_indices)

    train_indices = labelled_indices[:int(train_size*len(labelled_indices))]
    test_indices = labelled_indices[int(train_size*len(labelled_indices)):]

    ## now construct the sets 
    
    train_fvs, train_labels = constructSetFromIndices(fvs, labels, train_indices)
    test_fvs, test_labels = constructSetFromIndices(fvs, labels, test_indices)

    unlabelled_fvs, unlabelled_labels = constructSetFromIndices(fvs, labels, unlabelled_indices)

    train_all_fvs = train_fvs + unlabelled_fvs
    train_all_labels = train_labels + unlabelled_labels

    # shuffleeee

    # train_all_fvs, train_all_labels = shuffleListsTogether(train_all_fvs, train_all_labels)
    # train_fvs, train_labels = shuffleListsTogether(train_fvs, train_labels)
    # test_fvs, test_labels = shuffleListsTogether(test_fvs, test_labels)

    return train_fvs, train_labels, test_fvs, test_labels, train_all_fvs, train_all_labels, test_indices
  

# def shuffleListsTogether(A,B):
#     if len(A) != len(B):
#         raise ValueError("A and B are not of the same length!")

#     shuffleindices = [i for i in range(len(A))]
#     random.seed(123)
#     random.shuffle(shuffleindices)

#     A = [A[i] for i in shuffleindices]
#     B = [B[i] for i in shuffleindices]

#     return A, B

def constructSetFromIndices(fvs, labels, indices):
    set_fvs = []
    set_labels = []
    
    for index in indices:
        set_labels.append(labels[index])
        set_fvs.append(fvs[index])

    return set_fvs, set_labels

    

# want to extract labelled set while still holding on to the indices of the test instances we end up with
def extractLabelledUnlabelledIndices(labels):
    labelledindices = []
    unlablledindices = []

    if isinstance(labels, list) or isinstance(labels, np.ndarray):
        for i in range(len(labels)):
            if any(labels):
                labelledindices.append(i)
            else:
                unlablledindices.append(i)

    elif isinstance(labels, dict):
        for index in labels:
            if any(labels[index]):
                labelledindices.append(index)
            else:
                unlablledindices.append(index)
    else:
        raise ValueError("Labels data format not supported! Only supporting numpy arrays, lists and dicts!")
    
    return labelledindices, unlablledindices

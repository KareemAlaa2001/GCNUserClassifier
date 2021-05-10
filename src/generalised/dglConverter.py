import dgl
from dgl.data import DGLDataset
import torch
# import os
# import pandas as pd
import numpy as np
from torch._C import dtype
from pipelineRunner import run_dataset_building_pipeline
import random 


class StackExchangeDataset(DGLDataset):
    def __init__(self):
        super().__init__(name='stack_exchange')

    def process(self):
        fvs, labelledindices, labels_ints, adj_dict, num_classes = run_dataset_building_pipeline()
        self.labelledindices = labelledindices
        self.labels_ints = labels_ints
        node_features = torch.from_numpy(np.array(fvs))
        node_labels = torch.from_numpy(np.array(labels_ints))

        num_labelled = len(labelledindices)
        self.num_classes = num_classes
        src = []
        dst = []
        
        for index in adj_dict:
            neighbours = adj_dict[index]
            src += [index] * len(neighbours)
            dst += neighbours

        edges_src = torch.from_numpy(np.array(src))
        edges_dst = torch.from_numpy(np.array(dst))
    
        self.graph = dgl.graph((edges_src, edges_dst), num_nodes=node_features.shape[0])
        self.graph.ndata['feat'] = node_features
        self.graph.ndata['label'] = node_labels

        
        # want to split the labelled nodes to train, val and test 
        # full training set (all_train) mask will have indices in the above train_labelled indices + all nodes not in this set
        # implementing stratified splitting here to make my life easier

        # NOTE in case labels are very unbalanced and stratified splitting is needed, set this flag to true
        # TODO - LATER - MAKE A CLEANER INTERFACE FOR THIS
        random.seed(123)
        random.shuffle(labelledindices)
        stratified = True
        
        if stratified:
            train_indices, val_indices, test_indices = getstratifiedIndicesSplit(labels_ints, labelledindices, num_classes, 0.6,0.2)

        else:
            n_train = int(0.6*num_labelled)
            n_val = int(0.2* num_labelled)

            train_indices = labelledindices[:n_train]
            val_indices = labelledindices[n_train:n_train + n_val]
            test_indices = labelledindices[n_train + n_val:]

        

        print("Number of labelled indices passed into dgl thing:",len(labelledindices))
        print("Train:val:test in DGL used:",len(train_indices),len(val_indices),len(test_indices))
        # If your dataset is a node classification dataset, you will need to assign
        # masks indicating whether a node belongs to training, validation, and test set.
        n_nodes = node_features.shape[0]

        train_mask = torch.zeros(n_nodes, dtype=torch.bool)
        val_mask = torch.zeros(n_nodes, dtype=torch.bool)
        test_mask = torch.zeros(n_nodes, dtype=torch.bool)

        train_mask[train_indices] = True
        val_mask[val_indices] = True
        test_mask[test_indices] = True

        self.graph.ndata['train_mask'] = train_mask
        self.graph.ndata['val_mask'] = val_mask
        self.graph.ndata['test_mask'] = test_mask

    def update_masks_from_indices(self, new_train_indices=None, new_val_indices=None, new_test_indices=None):
        n_nodes = self.graph.ndata['train_mask'].shape[0]

        if new_train_indices is not None:
            train_mask = torch.zeros(n_nodes, dtype=torch.bool)
            train_mask[new_train_indices] = True
            self.graph.ndata['train_mask'] = train_mask

        if new_val_indices is not None:
            val_mask = torch.zeros(n_nodes, dtype=torch.bool)
            val_mask[new_val_indices] = True
            self.graph.ndata['val_mask'] = val_mask

        if new_test_indices is not None:
            test_mask = torch.zeros(n_nodes, dtype=torch.bool)
            test_mask[new_test_indices] = True
            self.graph.ndata['test_mask'] = test_mask

    def update_labels(self, labels_ints, num_classes):
        node_labels = torch.from_numpy(np.array(labels_ints))
        self.graph.ndata['label'] = node_labels
        self.num_classes = num_classes


    # NOTE this is legit since its a dataset with a single graph
    def __getitem__(self, i):
        return self.graph

    def __len__(self):
        return 1


def stratifiedKFold(labels_ints, labelledindices, num_classes, num_folds):
     # split indices to those of each class
    class_indices = [[] for i in range(num_classes)]

    for index in labelledindices:
        indexlabel = labels_ints[index]
        class_indices[indexlabel].append(index)

    # split each class then combine all together

    # train_indices = [] 
    # val_indices = []
    # test_indices = []

    # print("Lengths of class labels:", [len(class_indices[i]) for i in range(num_classes)])
    dataset_k_split = [[] for i in range(num_folds)]

    for classlabels in class_indices:
        splits = np.array_split(classlabels, num_folds) 

        for i in range(num_folds):
            dataset_k_split[i] += splits[i].tolist()
    
    return dataset_k_split


def getstratifiedIndicesSplit(labels_ints, labelledindices, num_classes, train_size, val_size):

    # split indices to those of each class
    class_indices = [[] for i in range(num_classes)]

    for index in labelledindices:
        indexlabel = labels_ints[index]
        class_indices[indexlabel].append(index)

    # split each class then combine all together

    train_indices = [] 
    val_indices = []
    test_indices = []

    print("Lengths of class labels:", [len(class_indices[i]) for i in range(num_classes)])

    for classlabels in class_indices:
        
        class_n_train = int(train_size*len(classlabels))
        class_n_val = int(val_size*len(classlabels))
        class_train_indices = classlabels[:class_n_train]
        class_val_indices = classlabels[class_n_train:class_n_train + class_n_val]
        class_test_indices = classlabels[class_n_train + class_n_val:]

        train_indices += class_train_indices
        val_indices += class_val_indices
        test_indices += class_test_indices
    
    return train_indices, val_indices, test_indices




# class KarateClubDataset(DGLDataset):
#     def __init__(self):
#         super().__init__(name='karate_club')

#     def process(self):
#         nodes_data = pd.read_csv('./members.csv')
#         edges_data = pd.read_csv('./interactions.csv')
#         node_features = torch.from_numpy(nodes_data['Age'].to_numpy())
#         node_labels = torch.from_numpy(nodes_data['Club'].astype('category').cat.codes.to_numpy())
#         edge_features = torch.from_numpy(edges_data['Weight'].to_numpy())
#         edges_src = torch.from_numpy(edges_data['Src'].to_numpy())
#         edges_dst = torch.from_numpy(edges_data['Dst'].to_numpy())

#         self.graph = dgl.graph((edges_src, edges_dst), num_nodes=nodes_data.shape[0])
#         self.graph.ndata['feat'] = node_features
#         self.graph.ndata['label'] = node_labels
#         self.graph.edata['weight'] = edge_features

#         # If your dataset is a node classification dataset, you will need to assign
#         # masks indicating whether a node belongs to training, validation, and test set.
#         n_nodes = nodes_data.shape[0]
#         n_train = int(n_nodes * 0.6)
#         n_val = int(n_nodes * 0.2)
#         train_mask = torch.zeros(n_nodes, dtype=torch.bool)
#         val_mask = torch.zeros(n_nodes, dtype=torch.bool)
#         test_mask = torch.zeros(n_nodes, dtype=torch.bool)
#         train_mask[:n_train] = True
#         val_mask[n_train:n_train + n_val] = True
#         test_mask[n_train + n_val:] = True
#         self.graph.ndata['train_mask'] = train_mask
#         self.graph.ndata['val_mask'] = val_mask
#         self.graph.ndata['test_mask'] = test_mask

#     def __getitem__(self, i):
#         return self.graph

#     def __len__(self):
#         return 1

# dataset = StackExchangeDataset()
# graph = dataset[0]

# print(graph)

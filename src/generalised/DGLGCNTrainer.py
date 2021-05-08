from corpusreader import SchemaCorpusProcessorFactory, FileExtractor
from lib.stackoverflowproc.extraction import recentUsers, recentPosts, recentComments, recentBadges
from lib.stackoverflowproc.fvBuilder import extractFeaturevectors
from stanza.server import CoreNLPClient
from masterdictGraphBuilder import MasterdictGraphProcessor
from dataHandler import GCNRunner, convertIdFVGuideToFVIndexGuide
import lib.stackoverflowproc.labelBuilder as labelBuilder
import random 
import os.path
import json
import dsSplitter
import numpy as np
from genhelpers import convertDictSetToListSet
from dglConverter import StackExchangeDataset
import dgl
import torch
import torch.nn as nn
import torch.nn.functional as F
import statistics
import dgl.data
from dgl.nn import GraphConv
from sklearn import metrics

# dataset = dgl.data.CoraGraphDataset() # will need 
# print('Number of categories:', dataset.num_classes)

# g = dataset[0]

# print('Node features')
# print(g.ndata)
# print('Edge features')
# print(g.edata)



class GCN(nn.Module):
    def __init__(self, in_feats, h_feats, num_classes, allow_zero_in_degree=False, dropout=0.0 ):
        super(GCN, self).__init__()
        self._allow_zero_in_degree = allow_zero_in_degree
        self.conv1 = GraphConv(in_feats, h_feats, allow_zero_in_degree=allow_zero_in_degree)
        self.conv2 = GraphConv(h_feats, num_classes, allow_zero_in_degree=allow_zero_in_degree)
        self.dropout = dropout

    def forward(self, g, in_feat):
        h = self.conv1(g, in_feat)
        h = F.relu(h)

        if self.dropout > 0:
            h = F.dropout(h, self.dropout)
        h = self.conv2(g, h)
        return h

# # Create the model with given dimensions
# model = GCN(g.ndata['feat'].shape[1], 16, dataset.num_classes)

def train(g, model, num_epochs=100, learning_rate=0.01, weight_decay=0, validation=True):
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate,weight_decay=weight_decay)
    best_val_acc = 0
    best_test_acc = 0

    features = g.ndata['feat']
    labels = g.ndata['label']
    train_mask = g.ndata['train_mask']
    val_mask = g.ndata['val_mask']
    test_mask = g.ndata['test_mask']

    model = model.float()

    for e in range(num_epochs):
        # Forward
        
        logits = model(g, features.float())

        # Compute prediction
        pred = logits.argmax(1)

        # Compute loss
        # Note that you should only compute the losses of the nodes in the training set.
        loss = F.cross_entropy(logits[train_mask], labels[train_mask])

        # Compute accuracy on training/validation/test
        train_acc = (pred[train_mask] == labels[train_mask]).float().mean()
        if validation:
            val_acc = (pred[val_mask] == labels[val_mask]).float().mean() 
        test_acc = (pred[test_mask] == labels[test_mask]).float().mean()

        # test_prec, test_rec, test_f1, test_support = metrics.precision_recall_fscore_support(labels, pred, average='macro', sample_weight=test_mask)
        


        # TODO JUST USE THE SKLEARN METRICS U IDIOT
        # Save the best validation accuracy and the corresponding test accuracy.
        if validation:
            if best_val_acc < val_acc:
                best_val_acc = val_acc
                best_test_acc = test_acc

        # Backward
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if e % 5 == 0:
            if validation:
                print('In epoch {}, loss: {:.3f}, val acc: {:.3f} (best {:.3f}), test acc: {:.3f} (best {:.3f})'.format(
                    e, loss, val_acc, best_val_acc, test_acc, best_test_acc))
            else:
                print('In epoch {}, loss: {:.3f}, test acc: {:.3f} (best {:.3f})'.format(
                    e, loss, test_acc, best_test_acc))
    
    report = metrics.classification_report(labels, pred, sample_weight=test_mask, digits=3, output_dict=True)
    return report

def train_get_weighted_f1(g, model, num_epochs=100, learning_rate=0.01, weight_decay=0):
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate,weight_decay=weight_decay)
    best_val_acc = 0
    best_test_acc = 0

    features = g.ndata['feat']
    labels = g.ndata['label']
    train_mask = g.ndata['train_mask']
    val_mask = g.ndata['val_mask']
    test_mask = g.ndata['test_mask']

    model = model.float()

    for e in range(num_epochs):
        # Forward
        
        logits = model(g, features.float())

        # Compute prediction
        pred = logits.argmax(1)

        # Compute loss
        # Note that you should only compute the losses of the nodes in the training set.
        loss = F.cross_entropy(logits[train_mask], labels[train_mask])

        # Compute accuracy on training/validation/test
        train_acc = (pred[train_mask] == labels[train_mask]).float().mean()
        val_acc = (pred[val_mask] == labels[val_mask]).float().mean()
        test_acc = (pred[test_mask] == labels[test_mask]).float().mean()

        # test_prec, test_rec, test_f1, test_support = metrics.precision_recall_fscore_support(labels, pred, average='macro', sample_weight=test_mask)
        


        # TODO JUST USE THE SKLEARN METRICS U IDIOT
        # Save the best validation accuracy and the corresponding test accuracy.
        if best_val_acc < val_acc:
            best_val_acc = val_acc
            best_test_acc = test_acc

        # Backward
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if e % 5 == 0:
            
            print('In epoch {}, loss: {:.3f}, val acc: {:.3f} (best {:.3f}), test acc: {:.3f} (best {:.3f})'.format(
                e, loss, val_acc, best_val_acc, test_acc, best_test_acc))
    
    report = metrics.classification_report(labels, pred, sample_weight=test_mask, digits=3, output_dict=True)
    weighted_f1_score = report['weighted avg']['f1-score']

    return weighted_f1_score

# def test_on_indices(g, model, test_indices):
#     model # TODO 

def test_model(g, model):
    features = g.ndata['feat']
    labels = g.ndata['label']
    test_mask = g.ndata['test_mask']

    logits = model(g, features.float())
        # Compute prediction
    pred = logits.argmax(1)

    report = metrics.classification_report(labels, pred, sample_weight=test_mask, digits=3, output_dict=True)
    return report

def new_test():
    dataset = StackExchangeDataset()
    g = dataset[0]
    print(g)
    model = GCN(g.ndata['feat'].shape[1], 16, dataset.num_classes, allow_zero_in_degree=True)
    train_get_weighted_f1(g, model)
    
def binary_f1_from_tensor(y_true, y_pred):
    assert y_true.ndim == 1
    assert y_pred.ndim == 1 or y_pred.ndim == 2
    
    if y_pred.ndim == 2:
        y_pred = y_pred.argmax(dim=1)
        
    
    tp = (y_true * y_pred).sum().to(torch.float32)
    tn = ((1 - y_true) * (1 - y_pred)).sum().to(torch.float32)
    fp = ((1 - y_true) * y_pred).sum().to(torch.float32)
    fn = (y_true * (1 - y_pred)).sum().to(torch.float32)
        
    precision = tp / (tp + fp )
    recall = tp / (tp + fn )
    
    f1 = 2* (precision*recall) / (precision + recall)
    return f1

def multiclass_f1(y_true, y_pred, num_classes):
    assert y_true.ndim == 1
    assert y_pred.ndim == 1 or y_pred.ndim == 2

    if y_pred.ndim == 2:
        y_pred = y_pred.argmax(dim=1)

    precisions = []
    recalls = []
    f1scores = []
    for i in range(num_classes):
        prec, recall, f1 = specific_class_f1_in_multiclass(y_true, y_pred, i)
        precisions.append(prec)
        recalls.append(recall)
        f1scores.append(f1)

    avg_prec = statistics.mean(precisions)
    avg_recall = statistics.mean(recalls)
    avg_f1 = statistics.mean(f1scores)

    return avg_prec, avg_recall, avg_f1



    

def specific_class_f1_in_multiclass(y_true, y_pred, classid):
    assert y_true.ndim == 1
    assert y_pred.ndim == 1

    tp = y_pred[y_pred == y_true and y_pred == classid].shape[0]
    tn = y_pred[y_pred == y_true and y_pred != classid].shape[0]
    fp = y_pred[y_pred != y_true and y_pred == classid].shape[0]
    fn = y_pred[y_pred != y_true and y_pred != classid].shape[0]
    
    precision = tp / (tp + fp )
    recall = tp / (tp + fn )
    
    f1 = 2* (precision*recall) / (precision + recall)
    return precision, recall, f1

# def main():
#     data_obj = {'user':recentUsers, 'comment':recentComments, 'post':recentPosts}

#     schema = {
#         'user': {
#             'idAtt': 'Id',
#             'featureAtts': [],
#             'linkAtts': {

#             }
#         },
#         'post': {
#             'idAtt': 'Id',
#             'featureAtts': [],
#             'linkAtts': {
#                 'ParentId': 'post',
#                 'OwnerUserId': 'user',
#                 'RelatedPostId': 'post'
#             }
#         }, 
#         'comment': {
#             'idAtt': 'Id',
#             'featureAtts': [],
#             'linkAtts': {
#                 'UserId': 'user',
#                 'PostId': 'post'
#             }

#         }


#     }
#     procFactory = SchemaCorpusProcessorFactory()

#     corpProc = procFactory.getCorpusProcessor()

#     masterdict = corpProc.readCorpus(data_obj, schema) 

#     mdgraphproc = MasterdictGraphProcessor()

#     gcngraph, idGraph, indexGuide = mdgraphproc.buildGraphsFromMasterDict(masterdict, schema)

#     numLinks = 0
#     for index in gcngraph:
#         numLinks += len(gcngraph[index])

#     numLinks /= 2

#     print("Number of edges in the graph:",numLinks)
#     print("Built the adjacency graph!!")

#     with CoreNLPClient(
#             annotators=['tokenize','ssplit','pos','lemma','ner'],
#             timeout=200000,
#             memory='16G', be_quiet=True) as client:
        

#         if os.path.isfile("fvmap.json") and os.path.getsize("fvmap.json") > 0:
#             print("fvmap file already exists, rejoice! the training time will be much less this time")
#             idFVMap = json.load(open("fvmap.json","r"))
#         else:
#             idFVMap = extractFeaturevectors(recentPosts, recentUsers, recentComments, client)

#         print("Extracted all of the FVs!")
#         indexFvMap = convertIdFVGuideToFVIndexGuide(idFVMap, indexGuide)
#         indexLabelMap = labelBuilder.getAllLabelsUsingBadgeClass(recentUsers, recentBadges, indexGuide)
#         fvslist = convertDictSetToListSet(indexFvMap)
#         lablelslist = convertDictSetToListSet(indexLabelMap)
        
#         print("Creating DGL Dataset")
#         dataset = StackExchangeDataset(fvslist,lablelslist,gcngraph,0.6,0.2,0.2)
#         graph = dataset[0]

#         print(graph)


if __name__ == '__main__':
    new_test()
    # main()
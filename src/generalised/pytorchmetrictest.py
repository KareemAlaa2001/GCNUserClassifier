import torch
import statistics
import numpy as np
from sklearn import metrics
# from metrics import f1_score, precision_recall_fscore_support

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

# def multiclass_f1(y_true, y_pred, num_classes):
#     assert y_true.ndim == 1
#     assert y_pred.ndim == 1 or y_pred.ndim == 2

#     if y_pred.ndim == 2:
#         y_pred = y_pred.argmax(dim=1)

#     precisions = []
#     recalls = []
#     f1scores = []
#     for i in range(num_classes):
#         prec, recall, f1 = specific_class_f1_in_multiclass(y_true, y_pred, i)
#         precisions.append(prec)
#         recalls.append(recall)
#         f1scores.append(f1)

#     avg_prec = statistics.mean(precisions)
#     avg_recall = statistics.mean(recalls)
#     avg_f1 = statistics.mean(f1scores)

#     return avg_prec, avg_recall, avg_f1



    

# def specific_class_f1_in_multiclass(y_true, y_pred, classid):
#     assert y_true.ndim == 1
#     assert y_pred.ndim == 1

#     equals = y_pred == y_true
#     trues = equals[equals == True]
#     falses = equals[equals == False]

#     tp

#     tn = y_pred[y_pred == y_true and y_pred != classid].shape[0]
#     fp = y_pred[y_pred != y_true and y_pred == classid].shape[0]
#     fn = y_pred[y_pred != y_true and y_pred != classid].shape[0]
    
#     precision = tp / (tp + fp )
#     recall = tp / (tp + fn )
    
#     f1 = 2* (precision*recall) / (precision + recall)
#     return precision, recall, f1


def main():
    dummypreds = torch.from_numpy(np.array([[0.02,0.28,0.2,0.5],[0.02,0.18,0.6,0.2],[0.9,0.1,0,0],[1,0,0,0],[0.2,0.8,0.0,0.0],[0.3,0.6,0.05,0.05]]))
    dummylabels = torch.from_numpy(np.array([[1,0,0,0],[0,0,1,0],[1,0,0,0],[1,0,0,0],[0,1,0,0],[0,0,0,1]]))
    dummypredsreduced = dummypreds.argmax(1)
    dummylabelsreduced = dummylabels.argmax(1)

    mask = torch.ones(6, dtype=torch.bool)
    # mask[4] = False
    prec, rec, f1, support = metrics.precision_recall_fscore_support(dummylabelsreduced, dummypredsreduced, average='macro', sample_weight=mask)
    print(metrics.classification_report(dummylabelsreduced, dummypredsreduced, sample_weight=mask, digits=3, output_dict=True))
    my_f1 = 2*(prec*rec)/(prec + rec)
    print("Avg precision:",prec)
    print("Avg recall:",rec)
    print("Avg f1:",f1)

if __name__ == '__main__':
    main()
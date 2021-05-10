import DGLGCNTrainer
from dglConverter import StackExchangeDataset, stratifiedKFold
import statistics as stats


def main():
    ##  Dataset building operartions done here
    dataset = StackExchangeDataset()
    labels_ints = dataset.labels_ints
    labelledindices = dataset.labelledindices
    g = dataset[0]  

    reports = []

    

    badgeclasshyperparams = {'target': 0.7482505099467229, 
    'params': {
        'dropout': 0.2095972572016474, 'hidden1': 47.631414020631496, 
        'learning_rate': 0.020524779748178592, 'num_epochs': 180.49878982255126, 'reg_factor': 0.00027387593197926164}}
    
    nicePostBinaryHyperparams = {'target': 0.8259088957051715, 
        'params': { 'dropout': 0.0461692973843989, 'hidden1': 21.685530991638885, 
        'learning_rate': 0.03462151663160047, 'num_epochs': 103.48279587690719, 'reg_factor': 0.005388167340033569}}

    #   Running the actual classification
    #   Going to run a 10-fold evaluation
    #   NOTE doing this in the separate func below
    # num_folds = 10
    # for i in range(10):
    #     params = badgeclasshyperparams.get('params')
    #     model = DGLGCNTrainer.GCN(g.ndata['feat'].shape[1], params.get('hidden1'), dataset.num_classes, allow_zero_in_degree=True, dropout=params.get('dropout'))
    #     report = DGLGCNTrainer.train(g, model, weight_decay=params.get('reg_factor'), learning_rate=params.get('learning_rate'), num_epochs=params.get('num_epochs'))

    #     reports.append(report)

def kfoldPipelineRun():
    dataset = StackExchangeDataset()
    labels_ints = dataset.labels_ints
    labelledindices = dataset.labelledindices
    num_classes = dataset.num_classes

    reports = []

    badgeclasshyperparams = {'target': 0.7492577835171325, 
    'params': {'dropout': 0.4022805061070413, 'hidden1': 33.6998497230906, 'learning_rate': 0.0559131138617306, 
    'num_epochs': 62.461910175237406, 'reg_factor': 0.001981014890848788}}

    
    nicePostBinaryHyperparams = {'target': 0.8302443037409214, 
    'params': {'dropout': 0.2515167086419769, 'hidden1': 47.631414020631496, 'learning_rate': 0.020524779748178592, 
    'num_epochs': 180.49878982255126, 'reg_factor': 0.00027387593197926164}}


    nicePostMulticlassHyperparams = {'target': 0.7147793751578765, 
    'params': {'dropout': 0.0, 'hidden1': 12.0, 'learning_rate': 0.03106249938783281, 
    'num_epochs': 117.92144217515235, 'reg_factor': 0.0}}


    tkipfOGHyperparams = {'dropout': 0.5, 'hidden1': 16, 
        'learning_rate': 0.01, 'num_epochs': 200, 'reg_factor': 0.0005}

    num_folds = 10


    # choice of params (depends on label type)
    # params = nicePostMulticlassHyperparams.get('params')
    params = tkipfOGHyperparams

    kfoldSplits = stratifiedKFold(labels_ints, labelledindices, num_classes, num_folds)

    dataset.update_masks_from_indices(new_val_indices=[])

    for i in range(num_folds):
        test_indices = kfoldSplits[i]
        train_indices = []
        for j in range(num_folds):
            if j != i:
                train_indices += kfoldSplits[j]

        dataset.update_masks_from_indices(new_train_indices=train_indices, new_test_indices=test_indices)
        graph = dataset[0]

        model = DGLGCNTrainer.GCN(graph.ndata['feat'].shape[1], int(params.get('hidden1')), dataset.num_classes, allow_zero_in_degree=True, dropout=params.get('dropout'))
        report = DGLGCNTrainer.train(graph, model, weight_decay=params.get('reg_factor'), learning_rate=params.get('learning_rate'), num_epochs=int(params.get('num_epochs')), validation=False)
        reports.append(report)

    meanstdevs, class_meanstdevs = getMetricAvgsStdDevsFromReports(reports, num_classes)
    output_text = "\n\n"
    output_text += "Results for label set BadgeClass:\n"
    output_text += "Means and standard deviations:\n"

    output_text += "Accuracy: " + str(meanstdevs[0]) + "\n"
    output_text += "Macro Precision: " + str(meanstdevs[1]) + "\n"
    output_text += "Macro Recall: " + str(meanstdevs[2]) + "\n"
    output_text += "Macro F1: " + str(meanstdevs[3]) + "\n"
    output_text += "Weighted Precision: " + str(meanstdevs[4]) + "\n"
    output_text += "Weighted Recall: " + str(meanstdevs[5]) + "\n"
    output_text += "Weighted F1: " + str(meanstdevs[6]) + "\n"

    output_text += "Class Results: (each sublist reps a class, elems are [precision,recall,f1])\n"
    output_text += str(class_meanstdevs) + "\n"

    print(output_text)

    file = open("output.txt","a")
    file.write(output_text)

    print("Run complete with BadgeClass labels!")



# this code is not brilliant but f it
def getMetricAvgsStdDevsFromReports(reports, num_classes):
    accs = []

    macro_precs = []
    macro_recs = []
    macro_f1s = []

    weighted_precs = []
    weighted_recalls = []
    weighted_f1s = []

    class_metric_agg = [[[],[],[]] for i in range(num_classes)]

    for report in reports:
        acc, macro_avgs, weighted_avgs, class_avgs = extractMetricsFromReport(report, num_classes)

        accs.append(acc)
        macro_precs.append(macro_avgs.get('precision'))
        macro_recs.append(macro_avgs.get('recall'))
        macro_f1s.append(macro_avgs.get('f1-score'))

        weighted_precs.append(weighted_avgs.get('precision'))
        weighted_recalls.append(weighted_avgs.get('recall'))
        weighted_f1s.append(weighted_avgs.get('f1-score'))

        for i in range(len(class_avgs)):
            class_report = class_avgs[i]
            class_metric_agg[i][0].append(class_report["precision"])
            class_metric_agg[i][1].append(class_report["recall"])
            class_metric_agg[i][2].append(class_report["f1-score"])

    
    metrics = [accs, macro_precs, macro_recs, macro_f1s, weighted_precs, weighted_recalls, weighted_f1s]

    meanstdevs = list(map(lambda lst: (stats.mean(lst),stats.stdev(lst)),metrics))

    class_meanstdevs = [[(stats.mean(lst), stats.stdev(lst)) for lst in classaggs] for classaggs in class_metric_agg]

    return meanstdevs, class_meanstdevs



def extractMetricsFromReport(report, num_classes):
    accuracy = report.get('accuracy')
    macro_avgs = report.get('macro avg')
    weighted_avgs = report.get('weighted avg')

    class_avgs = [{} for i in range(num_classes)]
    for i in range(num_classes):
        class_avgs[i] = report.get(str(i))

    return accuracy, macro_avgs, weighted_avgs, class_avgs


        
"""
{'0': {'precision': 1.0, 'recall': 0.6666666666666666, 'f1-score': 0.8, 'support': 3.0}, 
'1': {'precision': 0.5, 'recall': 1.0, 'f1-score': 0.6666666666666666, 'support': 1.0}, 
'2': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 1.0}, 
'3': {'precision': 0.0, 'recall': 0.0, 'f1-score': 0.0, 'support': 1.0}, 
'accuracy': 0.6666666666666666, 
'macro avg': {'precision': 0.625, 'recall': 0.6666666666666666, 'f1-score': 0.6166666666666667, 'support': 6.0}, 
'weighted avg': {'precision': 0.75, 'recall': 0.6666666666666666, 'f1-score': 0.6777777777777777, 'support': 6.0}}
"""
    

    
    

if __name__=='__main__':
    # main()
    kfoldPipelineRun()
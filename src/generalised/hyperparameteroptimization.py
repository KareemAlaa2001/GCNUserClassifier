from bayes_opt import BayesianOptimization
import DGLGCNTrainer
from dglConverter import StackExchangeDataset, getstratifiedIndicesSplit
import random


dataset = StackExchangeDataset()
g = dataset[0]

def main():
    output = ""
    optimisermax = optimize_this_shit()

    output += "Hyperparameter values achieved for NicePostMulti labels:\n"
    output += str(optimisermax) + "\n\n"

    file = open("hyperparam.txt","a")
    file.write(output)


def optimize_this_shit():
    pbounds = {'learning_rate': (0.0001,0.1), 'reg_factor': (0,0.01), 'dropout': (0,0.6), 'hidden1': (12,64), 'num_epochs': (40,200)}
    optimizer = BayesianOptimization(
        f=func_to_optimise,
        pbounds=pbounds,
        verbose=2, # verbose = 1 prints only when a maximum is observed, verbose = 0 is silent
        random_state=1,
    )

    optimizer.maximize(
        init_points=6,
        n_iter=15,
    )

    print(optimizer.max)
    return optimizer.max

# implemented shuffling between optimisation runs
def func_to_optimise(learning_rate, num_epochs, dropout, hidden1, reg_factor):
    
    hidden1 = int(hidden1)
    num_epochs = int(num_epochs)

    labelledindices = dataset.labelledindices
    labels_ints = dataset.labels_ints
    num_classes = dataset.num_classes
    random.shuffle(labelledindices)

    train_indices, val_indices, test_indices = getstratifiedIndicesSplit(labels_ints, labelledindices, num_classes, 0.8,0)

    dataset.update_masks_from_indices(new_train_indices=train_indices, new_val_indices=val_indices, new_test_indices=test_indices)
    g = dataset[0]

    model = DGLGCNTrainer.GCN(g.ndata['feat'].shape[1], hidden1, dataset.num_classes, allow_zero_in_degree=True, dropout=dropout)
    weighted_f1 = DGLGCNTrainer.train_get_weighted_f1(g, model, weight_decay=reg_factor, learning_rate=learning_rate, num_epochs=num_epochs)
    return weighted_f1


if __name__== '__main__':
    main()
from bayes_opt import BayesianOptimization
import DGLGCNTrainer
from dglConverter import StackExchangeDataset

dataset = StackExchangeDataset()
g = dataset[0]

def main():
    optimize_this_shit()


def optimize_this_shit():
    pbounds = {'learning_rate': (0.0001,0.1), 'reg_factor': (0,0.01), 'dropout': (0,0.5), 'hidden1': (12,64), 'num_epochs': (40,200)}
    optimizer = BayesianOptimization(
        f=func_to_optimise,
        pbounds=pbounds,
        verbose=2, # verbose = 1 prints only when a maximum is observed, verbose = 0 is silent
        random_state=1,
    )

    optimizer.maximize(
        init_points=4,
        n_iter=10,
    )

    print(optimizer.max)

def func_to_optimise(learning_rate, num_epochs, dropout, hidden1, reg_factor):
    
    hidden1 = int(hidden1)
    num_epochs = int(num_epochs)

    model = DGLGCNTrainer.GCN(g.ndata['feat'].shape[1], hidden1, dataset.num_classes, allow_zero_in_degree=True, dropout=dropout)
    weighted_f1 = DGLGCNTrainer.train_get_weighted_f1(g, model, weight_decay=reg_factor, learning_rate=learning_rate, num_epochs=num_epochs)
    return weighted_f1


if __name__== '__main__':
    main()
import numpy

def calc_true_false_pos_neg(labels, guesses):
    assert all(list(map(lambda x: len(x) == 2, labels))) and all(list(map(lambda x: len(x) == 2, guesses))), "This function only works with binary classification!!"
    assert len(labels) == len(guesses), "Number of labels and number of guesses is not equal!!!"
    
    truePos = 0
    trueNeg = 0
    falsePos = 0
    falseNeg = 0

    for i in range(len(labels)):
        label = labels[i]
        guess = guesses[i]

        # if label is +ve
        if label[0] == 1 and label[1] == 0:
            if all(guess == label):
                truePos += 1
            else:
                falseNeg += 1
        # if label is -ve
        elif label[0] == 0 and label[1] == 1:
            if all(guess == label):
                trueNeg += 1
            else:
                falsePos += 1

    return truePos, falsePos, trueNeg, falseNeg

def calc_acc(truePos, falsePos, trueNeg, falseNeg):
    return 100 * (truePos + trueNeg)/ (falseNeg + falsePos)

def calc_f1_score(truePos, falsePos, trueNeg, falseNeg):
    precision = calc_precision(trueNeg,falseNeg, truePos, falsePos)
    recall = calc_recall(trueNeg,falseNeg, truePos, falsePos)

    return 2*((precision*recall)/(precision+recall))


# 2*((precision*recall)/(precision+recall))
def calc_f1_score_from_guesses(labels, guesses):

    if not (all(list(map(lambda x: len(x) == 2, labels))) and all(list(map(lambda x: len(x) == 2, guesses)))):
        raise ValueError( "This function only works with binary classification!!")
    if len(labels) != len(guesses):
        raise ValueError( "Number of labels and number of guesses is not equal!!!")
    
    truePos = 0
    trueNeg = 0
    falsePos = 0
    falseNeg = 0

    for i in range(len(labels)):
        label = labels[i]
        guess = guesses[i]

        # if label is +ve
        if label[0] == 1 and label[1] == 0:
            if all(guess == label):
                truePos += 1
            else:
                falseNeg += 1
        # if label is -ve
        elif label[0] == 0 and label[1] == 1:
            if all(guess == label):
                trueNeg += 1
            else:
                falsePos += 1

    precision = calc_precision(trueNeg,falseNeg, truePos, falsePos)
    recall = calc_recall(trueNeg,falseNeg, truePos, falsePos)

    return 2*((precision*recall)/(precision+recall))

    
    
def calc_precision(truePos, falsePos):
    return truePos / (truePos + falsePos)



def calc_recall(falseNeg, truePos):
    return truePos / (truePos + falseNeg)

#%%
from extraction import extractAttribListIgnoreNones, recentPosts, recentComments, recentUsers, extractAttribList
from helpers import flatten, toIntList, sotimeToTimestamp
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.ticker import PercentFormatter


def test_bins(list, thresholds):
    counts = np.zeros(len(thresholds) + 1)
    
    for num in list:
        inRange = False

        for i in range(len(thresholds)):
            if num > thresholds[i]:
                continue
            else:
                counts[i] += 1
                inRange = True
                break
    
        if not inRange:
            counts[-1] += 1

    return counts


# print(viewsList[:200])
# # plt.xticks(np.arange(0, 1, step=0.1), np.arange(0,10000, 1000))
# nonZeroes = list(filter(lambda x: int(x) != 0, viewsList))

# print(nonZeroes[:200])
# plt.hist(nonZeroes, bins=n_bins)
# plt.show()
#%%

# postScoreList = extractAttribList(recentPosts, 'Score')

# print("Post score list size:", len(postScoreList))
# print("Post Scores: ")
# print(postScoreList[:100])

# commentScoreList = extractAttribList(recentComments, 'Score')

# print("Comment score list size:", len(commentScoreList))
# print("Comment Scores: ")
# print(commentScoreList[:100])

# userRepList = extractAttribList(recentUsers, 'Reputation' )

# print("User rep list size:", len(userRepList))
# print("User Reputations: ")
# print(userRepList[-100:])

# concatScoreList = flatten([postScoreList, commentScoreList, userRepList])
# intScores = list(map(lambda x: int(x), concatScoreList))
# print(intScores[:100])


# plt.hist(intScores, alpha=0.5, bins=np.arange(min(intScores), max(intScores) + 100, 100))
# # Generate a normal distribution, center at x=0 and y=5
# # x = np.random.randn(N_points)
# # y = .4 * x + np.random.randn(100000) + 5

# fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)

# # We can set the number of bins with the `bins` kwarg
# axs[0].hist(x, bins=n_bins)
# axs[1].hist(y, bins=n_bins)


# %%
viewsList = toIntList(extractAttribList(recentUsers, 'Views'))
# print(test_bins(viewsList, [0,10,100,1000]))


answerCounts = toIntList(extractAttribListIgnoreNones(recentPosts, 'AnswerCount'))
commentCounts = toIntList(extractAttribListIgnoreNones(recentPosts, 'CommentCount'))

# print(test_bins(answerCounts, [0,2,5,10,20]))
# print(test_bins(commentCounts, [0,2,5,10,20]))

upvotes = toIntList(extractAttribList(recentUsers, 'UpVotes'))
downvotes = toIntList(extractAttribList(recentUsers, 'DownVotes'))

plt.hist(upvotes, bins=[5,10,50,100,500,1000,5000])
plt.show()

print(test_bins(upvotes, [0,2,5,10,20,50,100,1000]))
print(test_bins(downvotes, [0,2,5,10,20,50,100,1000]))


# %%

postCreationDates = extractAttribList(recentPosts, 'CreationDate')
postLastActivities = extractAttribList(recentPosts, 'LastActivityDate')

print(len(postCreationDates), len(postLastActivities))

postdurations = [sotimeToTimestamp(latest)-sotimeToTimestamp(creation) for creation,latest in zip(postCreationDates, postLastActivities)]

timeMilestones = [60,3600,86400,604800,2629743,31556926] # 1 min, 1 hr, 1 day, 1 week, 1 month, 1 year

print("Post activity durations: ")
print(test_bins(postdurations, [60,3600,86400,604800,2629743,31556926])) 



userCreationDates = extractAttribList(recentUsers, 'CreationDate')
userLastAccessDates = extractAttribList(recentUsers, 'LastAccessDate')

print(len(userCreationDates), len(userLastAccessDates))

userdurations = [sotimeToTimestamp(latest)-sotimeToTimestamp(creation) for creation,latest in zip(userCreationDates, userLastAccessDates)]

print("User activity durations: ")
print(test_bins(userdurations, [60,3600,86400,604800,2629743,31556926, 31556926*5,31556926*10])) 

plt.hist(userdurations, bins=[60,3600,86400,604800,2629743,31556926, 31556926*5,31556926*10, 31556926*20])
plt.show()

concatdurations = postdurations + userdurations

plt.hist(concatdurations, bins=[60,3600,86400,604800,2629743,31556926, 31556926*5,31556926*10, 31556926*20])
plt.show()

print(len(postdurations))
print(len(userdurations))
# %%

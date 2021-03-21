#%%
from extraction import recentPosts, extractAttribList

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.ticker import PercentFormatter


# Fixing random state for reproducibility
np.random.seed(19680801)
# N_points = 100000
n_bins = 10

# viewsList = extractAttribList(recentUsers, 'Views')

# print(viewsList[:200])
# # plt.xticks(np.arange(0, 1, step=0.1), np.arange(0,10000, 1000))
# nonZeroes = list(filter(lambda x: int(x) != 0, viewsList))

# print(nonZeroes[:200])
# plt.hist(nonZeroes, bins=n_bins)
# plt.show()

postScoreList = extractAttribList(recentPosts, 'Score')

print(postScoreList[:1000])

# # Generate a normal distribution, center at x=0 and y=5
# # x = np.random.randn(N_points)
# # y = .4 * x + np.random.randn(100000) + 5

# fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)

# # We can set the number of bins with the `bins` kwarg
# axs[0].hist(x, bins=n_bins)
# axs[1].hist(y, bins=n_bins)


 # %%

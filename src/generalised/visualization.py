from lib.stackoverflowproc.extraction import recentUsers, recentComments, recentPosts, recentBadges, relevantUserIdDict
from pipelineRunner import run_adj_dict_building_pipeline
import lib.stackoverflowproc.labelBuilder as labelBuilder
from dglConverter import StackExchangeDataset
import DGLGCNTrainer
import sklearn.metrics as metrics
import matplotlib.pyplot as plt

dataset = StackExchangeDataset()

graph = dataset[0]

nicePostMulticlassHyperparams = {'target': 0.7147793751578765, 
    'params': {'dropout': 0.0, 'hidden1': 12.0, 'learning_rate': 0.03106249938783281, 
    'num_epochs': 117.92144217515235, 'reg_factor': 0.0}}

badgeclasshyperparams = {'target': 0.7492577835171325, 
    'params': {'dropout': 0.4022805061070413, 'hidden1': 33.6998497230906, 'learning_rate': 0.0559131138617306, 
    'num_epochs': 62.461910175237406, 'reg_factor': 0.001981014890848788}}

nicePostBinaryHyperparams = {'target': 0.8302443037409214, 
    'params': {'dropout': 0.2515167086419769, 'hidden1': 47.631414020631496, 'learning_rate': 0.020524779748178592, 
    'num_epochs': 180.49878982255126, 'reg_factor': 0.00027387593197926164}}

params = nicePostBinaryHyperparams.get('params')

model = DGLGCNTrainer.GCN(graph.ndata['feat'].shape[1], int(params.get('hidden1')), dataset.num_classes, allow_zero_in_degree=True, dropout=params.get('dropout'))
confusion = DGLGCNTrainer.train_get_confusion_matrix(graph, model, weight_decay=params.get('reg_factor'), learning_rate=params.get('learning_rate'), num_epochs=int(params.get('num_epochs')), validation=False)
#  labels=["NoNicePosts","NiceQuestionOnly","NiceAnswerOnly","Both"],

disp = metrics.ConfusionMatrixDisplay(confusion_matrix=confusion, display_labels=["NoNice","NicePost"])
# metrics.plot_confusion_matrix(DGLGCNTrainer.GCN, confusion_matrix=confusion, display_labels=["NoNicePosts","NiceQuestionOnly","NiceAnswerOnly","Both"])
disp.plot() 
plt.show()







# Checking the number of yearling badges within recentBadges

# # yearlingBadges = list(filter(lambda badge: badge.get('Name') == "Yearling", recentBadges))

# # numYearling = len(yearlingBadges)
# yearlingUsers = {}
# niceQUsers = {}
# niceAUsers = {}
# for badge in recentBadges:
#     if badge.get('Name') == "Yearling":
#         yearlingUsers[badge.get('UserId')] = 1

#     if badge.get('Name') == "Nice Question":
#         niceQUsers[badge.get('UserId')] = 1

#     if badge.get('Name') == "Nice Answer":
#         niceAUsers[badge.get('UserId')] = 1
        
# numYearling = len(yearlingUsers)
# print("Number of yearling userids:", numYearling)
        
# numniceQ = len(niceQUsers)
# print("Number of nice question userids:", numniceQ)

# print("Number of nice answer userids:", len(niceAUsers))

# either = niceAUsers.copy()
# either.update(niceQUsers)
# print("Number of nice answer or question userids:", len(either))

# print("Number of niceQ AND niceAns Users:",len( set(niceAUsers.keys() ) & set( niceQUsers.keys())))

# ##  Want to visualise average number of neighbours post question nodes have vs post answer nodes

# # 2 lists built: 1 - filter by PostTypeId = 1 (Question) and another with PostTypeId = 2 (Answer)

# questionPosts = []
# answerPosts = []
# otherPosts = []
# for post in recentPosts:
#     posttype = post.get('PostTypeId')

#     if posttype == '1':
#         questionPosts.append(post)

#     elif posttype == '2':
#         answerPosts.append(post)

#     else:
#         otherPosts.append(post)

# print("Numbers of question, answer and other posts: ",len(questionPosts),len(answerPosts),len(otherPosts))

# # Then need to get the average number of neighbours for each posttype - honestly would be fine to use the indexgraph directly 

# gcngraph, idGraph, indexGuide = run_adj_dict_building_pipeline()

# def get_average_num_neighbours_in_list(nodetype, nodelist):
#     avg_num_neighbours = 0

#     for member in nodelist:
#         nodeid = member.get('Id')
#         noideindex = indexGuide.get(nodetype).get(nodeid)
#         neighbourindexes = gcngraph.get(noideindex)
#         numneighbours = len(neighbourindexes)
#         avg_num_neighbours += numneighbours

#     avg_num_neighbours /= len(nodelist)

#     return avg_num_neighbours

# # avg_num_neighbours_question_posts = get_average_num_neighbours_in_list('post', questionPosts)
# # avg_num_neighbours_answer_posts = get_average_num_neighbours_in_list('post', answerPosts)
# # avg_num_neighbours_other_posts = get_average_num_neighbours_in_list('post', otherPosts)

# # print("Average number of neighbours for question, answer and other posts",avg_num_neighbours_question_posts,avg_num_neighbours_answer_posts,avg_num_neighbours_other_posts)

# allLabels, userLabels = labelBuilder.getAllLabelsUsingNiceQuestionAnswerMulticlass(recentUsers,recentBadges, indexGuide)
# allLabels, userLabels = labelBuilder.getAllLabelsUsingNiceQuestionAnswerBinary(recentUsers, recentBadges, indexGuide)

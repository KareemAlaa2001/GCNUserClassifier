from lib.stackoverflowproc.extraction import recentUsers, recentComments, recentPosts, recentBadges, relevantUserIdDict
from pipelineRunner import run_adj_dict_building_pipeline
import lib.stackoverflowproc.labelBuilder as labelBuilder
# Checking the number of yearling badges within recentBadges


# yearlingBadges = list(filter(lambda badge: badge.get('Name') == "Yearling", recentBadges))

# numYearling = len(yearlingBadges)
yearlingUsers = {}
niceQUsers = {}
niceAUsers = {}
for badge in recentBadges:
    if badge.get('Name') == "Yearling":
        yearlingUsers[badge.get('UserId')] = 1

    if badge.get('Name') == "Nice Question":
        niceQUsers[badge.get('UserId')] = 1

    if badge.get('Name') == "Nice Answer":
        niceAUsers[badge.get('UserId')] = 1
        
numYearling = len(yearlingUsers)
print("Number of yearling userids:", numYearling)
        
numniceQ = len(niceQUsers)
print("Number of nice question userids:", numniceQ)

print("Number of nice answer userids:", len(niceAUsers))

either = niceAUsers.copy()
either.update(niceQUsers)
print("Number of nice answer or question userids:", len(either))

print("Number of niceQ AND niceAns Users:",len( set(niceAUsers.keys() ) & set( niceQUsers.keys())))

##  Want to visualise average number of neighbours post question nodes have vs post answer nodes

# 2 lists built: 1 - filter by PostTypeId = 1 (Question) and another with PostTypeId = 2 (Answer)

questionPosts = []
answerPosts = []
otherPosts = []
for post in recentPosts:
    posttype = post.get('PostTypeId')

    if posttype == '1':
        questionPosts.append(post)

    elif posttype == '2':
        answerPosts.append(post)

    else:
        otherPosts.append(post)

print("Numbers of question, answer and other posts: ",len(questionPosts),len(answerPosts),len(otherPosts))

# Then need to get the average number of neighbours for each posttype - honestly would be fine to use the indexgraph directly 

gcngraph, idGraph, indexGuide = run_adj_dict_building_pipeline()

def get_average_num_neighbours_in_list(nodetype, nodelist):
    avg_num_neighbours = 0

    for member in nodelist:
        nodeid = member.get('Id')
        noideindex = indexGuide.get(nodetype).get(nodeid)
        neighbourindexes = gcngraph.get(noideindex)
        numneighbours = len(neighbourindexes)
        avg_num_neighbours += numneighbours

    avg_num_neighbours /= len(nodelist)

    return avg_num_neighbours

# avg_num_neighbours_question_posts = get_average_num_neighbours_in_list('post', questionPosts)
# avg_num_neighbours_answer_posts = get_average_num_neighbours_in_list('post', answerPosts)
# avg_num_neighbours_other_posts = get_average_num_neighbours_in_list('post', otherPosts)

# print("Average number of neighbours for question, answer and other posts",avg_num_neighbours_question_posts,avg_num_neighbours_answer_posts,avg_num_neighbours_other_posts)

allLabels, userLabels = labelBuilder.getAllLabelsUsingNiceQuestionAnswerMulticlass(recentUsers,recentBadges, indexGuide)
allLabels, userLabels = labelBuilder.getAllLabelsUsingNiceQuestionAnswerBinary(recentUsers, recentBadges, indexGuide)

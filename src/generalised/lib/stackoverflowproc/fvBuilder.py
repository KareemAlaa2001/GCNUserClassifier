# from lib.stackoverflowproc.extraction import recentPosts, recentComments
import stanza

from stanza.server import CoreNLPClient
import numpy as np
from lib.stackoverflowproc.helpers import *

"""
export CORENLP_HOME=/Users/kareem/UniStuff/3rd\ Year/3rdYearProject/Libraries/stanford-corenlp-4.2.0
"""

def main():
    text = "This is a testing sentence with Barack Obama and Marwan Pablo in Cairo, Egypt. I am also working at Tesco in Welwyn. Please also check out this url https://www.google.com."


    
    with CoreNLPClient(
            annotators=['tokenize','ssplit','pos','lemma','ner'],
            timeout=30000,
            memory='16G') as client:
        pass

        # ann = client.annotate(text)
        # sentences = ann.sentence
        # for sent in sentences:
        #     for token in sent.token:
        #         print(token.word, token.ner)
    
    #     for i in range(100,110):
    #         samplePost = recentPosts[i]
    #         sampleComment = recentComments[i]
            
    #         print("SAMPLE POST", i, ":")
    #         print(samplePost['Body'])
    #         print('\n')
    #         fv = postToFV(samplePost, client)
    #         print(fv)

    #         print("SAMPLE COMMENT", i, ":")
    #         print(sampleComment['Text'])
    #         print('\n')
    #         fv = commentToFV(sampleComment, client)
    #         print(fv)

            
    # pass

"""
 TODO figure out how I'm going to return the featurevectors of all the posts, users and comments
 Am I gonna return them separately? Will I put them all into one big matrix then split it later?
 How will I handle indexing in that case?

 Will I have an extra data structure that maps ids with indexes?
"""
def extractFeaturevectors(posts, users, comments, client):
    
    fvmap = {'post': {}, 'comment':{}, 'user':{}}

    for post in posts:
        postfv = postToFV(post, client)
        fvmap['post'][post.get('Id')] = postfv
    print("did all the post fvs")
    for user in users:
        userfv = userToFV(user, client)
        fvmap['user'][user.get('Id')] = userfv
    print("did all the user fvs")
    for comment in comments:
        commentfv = commentToFV(comment,client)
        fvmap['comment'][comment.get('Id')] = commentfv
    print("did all the comment fvs")
    return fvmap


    



"""
FEATUREVECTOR DOCUMENTATION:

 This will keep track of what each slot in the FV corresponds to.
 First a 1 for what it is:
    [ Post, User, Comment,
 
 Common ALL3:
    Score/Reputation[need to bin], ActiveDuration (rangebinned timestamps), NER, 

 Common POST & USER (fomat: User/Post):
    Views/ViewCount[6-dim array for 6 possible bins], LastAccessDate/LastActivityDate (TO TIMESTAMP) [need to bin]

 Unique to User:
    Upvotes, Downvotes
 
 Unique to Post:
    AnswerCount, CommentCount, IsAcceptedAnswer]

MUST DECIDE WHETHER TO CREATE A NEW TYPE FOR TAGS, OR IGNORE THEM ENTIRELY

"""

def postToFV(post, client):
    fv = [] # need to decide on the structure for a general node FV, then use that here
    postner = getPostNER(post, client)

    fv.append([
        1.0,0.0,0.0
        ])
    
    fv.append(rangeBinScore(float(post['Score'])))

    fv.append(rangeBinActiveDuration(sotimeToTimestamp(post['CreationDate']),sotimeToTimestamp(post['LastActivityDate'])))

    # fv.append(sotimeToTimestamp(post['CreationDate']))
        
    fv.append(postner)

    # If the post is a parent post in a thread
    if post['PostTypeId'] == '1':
        fv.append(rangeBinViews(float(post.get('ViewCount'))))

        # fv.append([sotimeToTimestamp(post['LastActivityDate'])])

        fv.append([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]) # User Upvotes
        fv.append([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]) # User DownVotes

        fv.append(rangeBinAnswerOrCommentCount(float(post.get('AnswerCount'))))
        fv.append(rangeBinAnswerOrCommentCount(float(post.get('CommentCount'))))
        
    else:
        
        fv.append(rangeBinViews(post.get('ViewCount')))

        # fv.append([sotimeToTimestamp(post['LastActivityDate'])])

        fv.append([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]) # User Upvotes
        fv.append([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]) # User DownVotes

        fv.append([0.0,0.0,0.0,0.0,0.0,0.0])
        fv.append(rangeBinAnswerOrCommentCount(float(post.get('CommentCount'))))

    fv.append([float(post.get('IsAcceptedAnswer'))])
    # print(fv)
    flat_vec = flatten(fv)
    return flat_vec

# Function to construct the featurevector representing the user dictionary passed
# Params: user - user dictionary, client - CoreNLP client for NER
def userToFV(user, client):
    fv = []
    userner = convertStringToNER(user.get('AboutMe'), client)

    fv.append([
        0.0,1.0,0.0
    ])

    fv.append(rangeBinScore(float(user.get('Reputation'))))

    # fv.append(sotimeToTimestamp(user['CreationDate']))

    fv.append(rangeBinActiveDuration(sotimeToTimestamp(user['CreationDate']),sotimeToTimestamp(user['LastAccessDate'])))


    fv.append(userner)

    viewsVector = rangeBinViews(float(user.get('Views')))

    fv.append(viewsVector)

    # fv.append(sotimeToTimestamp(user['LastAccessDate']))
    
    fv.append(rangeBinUpDownVotes(float(user.get('UpVotes'))))
    fv.append(rangeBinUpDownVotes(float(user.get('DownVotes'))))

    fv.append([0.0,0.0,0.0,0.0,0.0,0.0]) # AnswerCount
    fv.append([0.0,0.0,0.0,0.0,0.0,0.0]) # CommentCount
    
    fv.append([0.0]) # Post.IsAcceptedAnswer

    fv = flatten(fv)

    return fv

def commentToFV(comment, client):
    fv = []
    commentner = convertStringToNER(comment.get('Text'), client)

    fv.append([
        0.0,0.0,1.0
        ]) # Post, User or Comment

    fv.append(rangeBinScore(float(comment.get('Score')))) 

    fv.append(rangeBinActiveDuration(sotimeToTimestamp(comment['CreationDate']),sotimeToTimestamp(comment['LastActivityDate'])))
    
    fv.append(commentner)

    fv.append([0.0,0.0,0.0,0.0,0.0,0.0]) # Views

    fv.append([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]) # User Upvotes
    fv.append([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]) # User Downvotes

    fv.append([0.0,0.0,0.0,0.0,0.0,0.0]) # AnswerCount
    fv.append([0.0,0.0,0.0,0.0,0.0,0.0]) # CommentCount

    fv.append([0.0]) # Post.IsAcceptedAnswer

    fv = flatten(fv)

    return fv

def getPostNER(post, client):

    bodyNER = convertStringToNER(post.get('Body'), client)

    nerVector = np.array(bodyNER)

    if 'Title' in post:
        titleNER = convertStringToNER(post['Title'], client)
        nerVector = np.array(titleNER) + np.array(bodyNER)

    return nerVector




"""
WILL NOTE THE PROPERTIES OF ALL THE DIFFERENT NODE TYPES HERE:

POST: 
 Another Example Post:
    <row Id="377691" 
    PostTypeId="2" 
    ParentId="377643" 
    CreationDate="2018-12-11T01:54:46.607" 
    Score="10" 
    Body="&lt;p&gt;You're right, the answer should be edited out of the question.  Answers belong in answers, not in questions.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;As for what to do next, if the question is closed, you have several options:&lt;/p&gt;&#xA;&#xA;&lt;h3&gt;1. Vote to reopen.&lt;/h3&gt;&#xA;&#xA;&lt;p&gt;If you feel that the question deserves to be here and to be answered (i.e. it is on-topic, answerable and not a duplicate), then you should vote to reopen it.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;Unfortunately, as you've observed, reopen review is kinda broken, with even seemingly obvious cases (like, say, an on-topic question closed as a &lt;a href=&quot;https://data.stackexchange.com/stackoverflow/query/209965/duplicates-of-deleted-questions&quot; rel=&quot;nofollow noreferrer&quot;&gt;duplicate of a deleted question&lt;/a&gt;) having a pretty low success rate of getting reopened.  &lt;a href=&quot;https://meta.stackoverflow.com/questions/364251/are-these-questions-really-duplicates/364269#364269&quot;&gt;I've complained about this before&lt;/a&gt;, but as long as the queue keeps being flooded with auto-flagged questions that clearly should stay closed, I doubt it will improve.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;The work-around is to find some other place with less jaded people that you can ask to take a look at the question.  The &lt;a href=&quot;https://chat.stackoverflow.com/rooms/41570/so-close-vote-reviewers&quot;&gt;SOCVR&lt;/a&gt; chat room is one such place.  (Yes, compared to the reopen queue, it really is!)  Meta can be another, as you may have noticed; right now, &lt;a href=&quot;https://stackoverflow.com/q/53559850&quot;&gt;the question linked from the comments above&lt;/a&gt; is one vote away from being reopened.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;Of course, neither SOCVR nor meta are any kind of magic cheat codes to bypass review entirely &amp;mdash; they just get the question reviewed by a different set of people, hopefully with a more discerning eye.  In some cases it might turn out that those people still think the question doesn't deserve to be reopened, in which case &lt;a href=&quot;https://meta.stackoverflow.com/questions/356846/is-this-question-really-too-broad-and-if-so-how-did-i-manage-to-answer-it-anyw&quot;&gt;they'll probably tell you so, in detail.&lt;/a&gt;  But at least you'll get some useful feedback, rather than just a list of users who may or may not have glanced at the question before clicking &quot;Leave Closed&quot;.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;BTW, if you think that the question &lt;em&gt;could be&lt;/em&gt; good and on-topic, but is not necessarily so yet, then edit it into shape first &lt;em&gt;before&lt;/em&gt; proposing to reopen it!  I really can't stress that too much.  People will review the question based on what it is, not what it could be, and a poorly written half-off-topic question is unlikely to get reopened even if there's a good question buried inside it.&lt;/p&gt;&#xA;&#xA;&lt;h3&gt;2. Answer the duplicate instead.&lt;/h3&gt;&#xA;&#xA;&lt;p&gt;Of course, this only applies if the question is closed as a duplicate (unless you can get it reopened and re-closed, which takes a lot of effort for usually little gain).&lt;/p&gt;&#xA;&#xA;&lt;p&gt;The tricky part here is that the answer to &lt;em&gt;this specific closed question&lt;/em&gt; may not actually be a good answer to the duplicate, at least not without a considerable amount of editing.  Sometimes all it takes is changing a few variable names to match, but sometimes the closed question (and its answer) might be significantly narrower than the duplicate, or perhaps asking about the same problem using completely different terminology.  Maybe the duplicate is a general question about doing &lt;em&gt;X&lt;/em&gt; in &lt;em&gt;Y&lt;/em&gt;, while the closed question is about doing &lt;em&gt;Q&lt;/em&gt; (another name for &lt;em&gt;X&lt;/em&gt;) in &lt;em&gt;Y&lt;/em&gt; in the context of doing &lt;em&gt;Z&lt;/em&gt;.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;If you feel like spending the effort of editing the answer to make it fit, one potentially useful &quot;framing device&quot; can be to &lt;em&gt;briefly&lt;/em&gt; summarize the closed question at the top of the answer (and maybe link to it, for context), something like:&lt;/p&gt;&#xA;&#xA;&lt;blockquote&gt;&#xA;  &lt;p&gt;&quot;For the specific problem of doing &lt;em&gt;X&lt;/em&gt; (a.k.a. &lt;em&gt;Q&lt;/em&gt;) with &lt;em&gt;Y&lt;/em&gt; while also doing &lt;em&gt;Z&lt;/em&gt;, as in [this duplicate question](link), a good solution is to...&quot;&lt;/p&gt;&#xA;&lt;/blockquote&gt;&#xA;&#xA;&lt;p&gt;or:&lt;/p&gt;&#xA;&#xA;&lt;blockquote&gt;&#xA;  &lt;p&gt;&quot;The need to do &lt;em&gt;X&lt;/em&gt; (a.k.a. &lt;em&gt;Q&lt;/em&gt;) with &lt;em&gt;Y&lt;/em&gt; often arises in the context of &lt;em&gt;Z&lt;/em&gt;, as in [this duplicate question](link).  In such cases, one can...&quot;&lt;/p&gt;&#xA;&lt;/blockquote&gt;&#xA;&#xA;&lt;p&gt;or:&lt;/p&gt;&#xA;&#xA;&lt;blockquote&gt;&#xA;  &lt;p&gt;&quot;To illustrate how to do &lt;em&gt;X&lt;/em&gt; with &lt;em&gt;Y&lt;/em&gt;, let's say you're doing &lt;em&gt;Z&lt;/em&gt; and want to do &lt;em&gt;Q&lt;/em&gt;, as in [this duplicate question](link)...&quot;&lt;/p&gt;&#xA;&lt;/blockquote&gt;&#xA;&#xA;&lt;p&gt;Of course, even with such a framing device, you still need to ensure that the framed answer really is a useful answer to the question you're posting it under. &#xA; If you can't make it so, that could be evidence that &lt;em&gt;maybe the questions aren't truly duplicates after all&lt;/em&gt;, if there is a good answer to one of them that doesn't answer the other.  You may want to explicitly point that fact out when proposing to reopen.&lt;/p&gt;&#xA;&#xA;&lt;h3&gt;3. Find a better duplicate (and maybe answer it).&lt;/h3&gt;&#xA;&#xA;&lt;p&gt;Sometimes, you might discover that the question &lt;em&gt;is&lt;/em&gt; an exact duplicate, but not really of the question which it was closed as a duplicate of.  In such cases, it may be useful to note that &lt;a href=&quot;https://meta.stackexchange.com/questions/291824/gold-tag-badge-holders-and-moderators-can-now-edit-duplicate-links&quot;&gt;gold badge holders (and moderators) can edit duplicate links&lt;/a&gt; without having to reopen and re-close the question.  If you don't happen to have a gold badge in any of the question's tags yourself, you could:&lt;/p&gt;&#xA;&#xA;&lt;ul&gt;&#xA;&lt;li&gt;ask e.g. on SOCVR if there happen to be any gold badge holders around,&lt;/li&gt;&#xA;&lt;li&gt;flag the question for moderator attention and ask them to change the dupe target, or&lt;/li&gt;&#xA;&lt;li&gt;if the question was originally closed by a gold badge holder (alone), @ping them in the comments (&lt;a href=&quot;https://meta.stackexchange.com/questions/43019/how-do-comment-replies-work/43020#43020&quot;&gt;yes, this does work!&lt;/a&gt;) and ask them to edit the link.&lt;/li&gt;&#xA;&lt;/ul&gt;&#xA;&#xA;&lt;p&gt;Of course, if all else fails, you could also just post a comment linking to the better duplicate question yourself.  It may not get listed in the box at the top of the question, but at least the link will be there in the comments if anyone bothers to look for it.&lt;/p&gt;&#xA;&#xA;&lt;h3&gt;4. Just let it be.&lt;/h3&gt;&#xA;&#xA;&lt;p&gt;Sometimes, it might be that there is no good place for the answer.  Maybe the (new) duplicate already has an essentially equivalent answer, or maybe the answer is so tangled up with the OP's code and their specific needs that generalizing it to be useful to a wider audience would require a complete rewrite.  Or maybe the answer is just wrong, or the question it answers is off-topic.  In such cases, the best solution may be to just edit the answer out and &lt;em&gt;not&lt;/em&gt; repost it anywhere.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;You may also consider voting to delete the question itself, or at least downvoting it to &lt;a href=&quot;https://meta.stackexchange.com/questions/78048/enable-automatic-deletion-of-old-unanswered-zero-score-questions-after-a-year/92006#92006&quot;&gt;make it eligible for auto-deletion&lt;/a&gt;.  Note that SO currently has no delete vote review queue (all we have is the &lt;a href=&quot;https://stackoverflow.com/help/privileges/moderator-tools&quot;&gt;crappy old 10k tools page&lt;/a&gt;), so random single delete votes on old questions are &lt;em&gt;even less likely than reopen votes&lt;/em&gt; to actually achieve anything.  Again, SOCVR is your friend here.&lt;/p&gt;&#xA;"
    OwnerUserId="411022" 
    LastActivityDate="2018-12-11T01:54:46.607" 
    CommentCount="1" 
    ContentLicense="CC BY-SA 4.0" />

 Example post:
    row Id="250001" 
    PostTypeId="1" 
    AcceptedAnswerId="250002" 
    CreationDate="2014-04-17T00:49:28.617" 
    Score="21" ViewCount="893" 
    Body="&lt;p&gt;Will we get our reputation moved over or questions?&lt;/p&gt;&#xA;"
    OwnerUserId="23528" 
    LastEditorUserId="387076" 
    LastEditDate="2014-04-17T00:51:26.693" 
    LastActivityDate="2014-04-17T01:36:58.283" 
    Title="Will the questions be migrated over from meta.stackexchange.com?" 
    Tags="&lt;discussion&gt;&lt;meta&gt;&lt;mso-mse-split&gt;" 
    AnswerCount="4" 
    CommentCount="6" 
    ContentLicense="CC BY-SA 3.0"

 Example User:
    <row Id="2" 
    Reputation="5702" 
    CreationDate="2008-07-31T14:22:31.000" 
    DisplayName="Geoff Dalgas" 
    LastAccessDate="2020-08-27T14:55:29.363" 
    WebsiteUrl="http://stackoverflow.com" 
    Location="Corvallis, OR" 
    AboutMe="&lt;p&gt;Developer on the Stack Overflow team.  Find me on&lt;/p&gt;&#xA;&#xA;&lt;p&gt;&lt;a href=&quot;http://www.twitter.com/SuperDalgas&quot; rel=&quot;nofollow noreferrer&quot;&gt;Twitter&lt;/a&gt;&#xA;&lt;br&gt;&lt;br&gt;&#xA;&lt;a href=&quot;http://blog.stackoverflow.com/2009/05/welcome-stack-overflow-valued-associate-00003/&quot;&gt;Stack Overflow Valued Associate #00003&lt;/a&gt;&lt;/p&gt;&#xA;"
    Views="979" 
    UpVotes="76" 
    DownVotes="15" 
    ProfileImageUrl="https://i.stack.imgur.com/nDllk.png?s=256&amp;g=1" 
    AccountId="2" />

 Example Comment:
    Id="1" 
    PostId="250001" 
    Score="28" 
    Text="Looks like they arbitrarily choose 250000 as the post id cutoff. (1st comment on the new Meta.SO!!! AHAHAHAHA)" 
    CreationDate="2014-04-17T00:49:51.207" 
    UserId="922184" 
    ContentLicense="CC BY-SA 3.0" />

 Useful stuff for links:
    Post:
        Id
        AcceptedAnswerId
        OwnerUserId
        (LastEditorUserId)??
    User:
        Id
        AccountId?
    Comment:
        Id
        PostId
        UserId



 Useful stuff for an FV: 
    Post:
        Creationdate - convert to timestamp
        Score
        ViewCount
        BodyNER & TitleNER
        (LastEditDate)??
        (LastActivityDate)??
        Tags [Need to build a vector for that]
        AnswerCount
        CommentCount
        IsAcceptedAnswer
    User:
        Reputation
        CreationDate
        LastAccessDate?
        WebsiteUrl?
        AboutMeNER
        Views
        Upvotes
        Downvotes
    Comment:
        Score
        TextNER
        CreationDate

NOTICES:
Fields to share:
- Can share creationdates and lastactivity/lastaccess dates
- Can share field for score and reputation
- Can share Views & Viewcount fields
- Can share NER fields (obviously)

"""

"""
entityTypes = ["PERSON", "LOCATION", "ORGANIZATION", "MISC", "MONEY", "NUMBER", 
    "ORDINAL", "PERCENT", "DATE", "TIME", "DURATION", "SET", "EMAIL", "URL", "CITY", 
    "STATE_OR_PROVINCE", "COUNTRY", "NATIONALITY", "RELIGION", "TITLE", "IDEOLOGY", 
    "CRIMINAL_CHARGE", "CAUSE_OF_DEATH", "HANDLE"]

"""

if __name__ == '__main__':
    main()

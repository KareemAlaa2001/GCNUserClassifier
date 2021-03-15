import extraction
from extraction import recentPosts
import stanza
import re
from stanza.server import CoreNLPClient
import numpy as np
from datetime import datetime
# print(extraction.recentUsers[0])

"""
For English, by default, this annotator recognizes named (PERSON, LOCATION, ORGANIZATION, MISC), 
numerical (MONEY, NUMBER, ORDINAL, PERCENT), and temporal (DATE, TIME, DURATION, SET) entities (12 classes).
Adding the regexner annotator and using the supplied RegexNER pattern files adds support for the fine-grained and
additional entity classes EMAIL, URL, CITY, STATE_OR_PROVINCE, COUNTRY, NATIONALITY, RELIGION, (job) TITLE, 
IDEOLOGY, CRIMINAL_CHARGE, CAUSE_OF_DEATH, (Twitter, etc.) HANDLE (12 classes) for a total of 24 classes. 

"""

entityTypes = ["PERSON", "LOCATION", "ORGANIZATION", "MISC", "MONEY", "NUMBER", 
    "ORDINAL", "PERCENT", "DATE", "TIME", "DURATION", "SET", "EMAIL", "URL", "CITY", 
    "STATE_OR_PROVINCE", "COUNTRY", "NATIONALITY", "RELIGION", "TITLE", "IDEOLOGY", 
    "CRIMINAL_CHARGE", "CAUSE_OF_DEATH", "HANDLE"]

class NerProcessor:

    def __init__(self, *args):
        if len(args) < 1:
            print('did that') 
        else:
            print('nah')

    def stanza_basic_init(self):
        stanza.download("en")
        return stanza.Pipeline("en")

    # init a custom pipeline with a variable number of strings passed as the components of the pipeline 
    def init_pipeline(self, *args):
        pass

    def getEntryNE(self,entry):
        body = entry.get("Body")
        

def main():
    text = "This is a testing sentence with Barack Obama and Marwan Pablo in Cairo, Egypt. I am also working at Tesco in Welwyn. Please also check out this url https://www.google.com."

    with CoreNLPClient(
            annotators=['tokenize','ssplit','pos','lemma','ner'],
            timeout=30000,
            memory='16G') as client:

        # ann = client.annotate(text)
        # sentences = ann.sentence
        # for sent in sentences:
        #     for token in sent.token:
        #         print(token.word, token.ner)
    
        for i in range(100,110):
            samplePost = recentPosts[i]
            print(samplePost['Body'])
            print('\n')
            fv = postToFV(samplePost, client)
            print(fv)
    pass

def testSoTimeToTimestamp():
    dttest = datetime(year=2005,month=10, day=3, hour=15, minute=59, second=59, microsecond=987000)
    tstamptest = datetime.timestamp(dttest)
    print(tstamptest)
    sotimetest = "2005-10-03T15:59:59.987"
    sotimestamp = sotimeToTimestamp(sotimetest)
    print(sotimestamp)
    if tstamptest == sotimestamp:
        print('it works')
    else:
        print('something went wrong')

def sotimeToTimestamp(datetimestr):
   parts = datetimestr.split("T")
   date = parts[0]
   time = parts[1]

   dateparts = date.split("-")
   year = int(dateparts[0])
   month = int(dateparts[1])
   day = int(dateparts[2])

   timeparts = time.split(":")
   hour = int(timeparts[0])
   minute = int(timeparts[1])
   secNms = timeparts[2]

   sec = int(secNms.split(".")[0])
   ms = int(secNms.split(".")[1])

   dt = datetime(year,month,day,hour,minute,sec,ms*1000)
   return datetime.timestamp(dt)


def getPostNER(post, client):

    bodyNER = convertStringToNER(post['Body'], client)

    nerVector = np.array(bodyNER)

    if 'Title' in post:
        titleNER = convertStringToNER(post['Title'], client)
        nerVector = np.array(titleNER) + np.array(bodyNER)

    return nerVector

# basic naive regex xml tag remover
def cleanXML(string):
    return re.sub('<.*?>', '', string)

"""
WILL NOTE THE PROPERTIES OF ALL THE DIFFERENT NODE TYPES HERE:

POST: 

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
# WILL GO WITH THE IDEA OF HAVING NER SLOTS IN COMMON THEN HAVING EXTRA SLOTS FOR DIFFERENT METADATA. 

"""
FEATUREVECTOR DOCUMENTATION:

 This will keep track of what each slot in the FV corresponds to.

 Common ALL3:
    [Score/Reputation, CreationDate (converted to timestamp), NER, 

 Common POST & USER (fomat: User/Post):
    Views/ViewCount, LastAccessDate/LastActivityDate (TO TIMESTAMP)

 Unique to User:
    Upvotes, Downvotes
 
 Unique to Post:
    AnswerCount, CommentCount, TAGS? ]

MUST DECIDE WHETHER TO CREATE A NEW TYPE FOR TAGS, OR IGNORE THEM ENTIRELY

"""

def postToFV(post, client):
    fv = [] # need to decide on the structure for a general node FV, then use that here
    postner = getPostNER(post, client)
    fv.append([post['Score'],sotimeToTimestamp(post['CreationDate'])])
    fv.append(postner)
    fv.append([post['ViewCount'],sotimeToTimestamp(post['LastActivityDate']),0.0,0.0,post['AnswerCount'],post['CommentCount']])

    return fv
    

"""
entityTypes = ["PERSON", "LOCATION", "ORGANIZATION", "MISC", "MONEY", "NUMBER", 
    "ORDINAL", "PERCENT", "DATE", "TIME", "DURATION", "SET", "EMAIL", "URL", "CITY", 
    "STATE_OR_PROVINCE", "COUNTRY", "NATIONALITY", "RELIGION", "TITLE", "IDEOLOGY", 
    "CRIMINAL_CHARGE", "CAUSE_OF_DEATH", "HANDLE"]

"""

# THIS FUNCTION CAN BE EXPANDED TO INCLUDE ANY FUTURE ADDITIONAL PREPROCESSING NEEDED FOR THE STRING
def convertStringToNER(string, client):
    string = cleanXML(string)
    # need to add in functionality to take that and convert to a NER frequency vector
    ann = client.annotate(string)
    nerVector = buildNERVector(ann)
    return nerVector

def buildNERVector(ann):
    nerVector = np.zeros(24)
    sentences = ann.sentence

    for sent in sentences:
        tokens = sent.token
        for tok in tokens:
            if tok.ner != 'O':
                index = entityTypes.index(tok.ner)
                nerVector[index] += 1

    return nerVector


    

if __name__ == '__main__':
    main()

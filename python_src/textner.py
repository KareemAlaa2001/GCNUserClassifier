import extraction
# from extraction import recentPosts
import stanza
import re
from stanza.server import CoreNLPClient
import numpy as np
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
    # testNerObj = basicNer(testStr)
    # print(*[f'entity: {ent.text}\ttype: {ent.type}' for sent in testNerObj.sentences for ent in sent.ents], sep='\n')

    with CoreNLPClient(
            annotators=['tokenize','ssplit','pos','lemma','ner'],
            timeout=30000,
            memory='16G') as client:

        ann = client.annotate(text)
        sentences = ann.sentence
        for sent in sentences:
            for token in sent.token:
                print(token.word, token.ner)


    # print(testNerObj)
    # print(doc)\
    # for i in range(100,110):
    #     samplePost = recentPosts[i]
    #     print(samplePost['Body'])
    #     print('\n')
    #     print(cleanXML(samplePost['Body']))
    #     print('\n')


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

 Useful stuff for links:
    Id
    AcceptedAnswerId
    OwnerUserId
    (LastEdifotrUserId)??

 Useful stuff for an FV: 
    Creationdate - convert to timestamp
    Score
    ViewCount
    BodyNER
    (LastEditDate)??
    (LastActivityDate)??
    TitleNER
    Tags [Need to build a vector for that]
    AnswerCount
    CommentCount

"""
# WILL GO WITH THE IDEA OF HAVING NER SLOTS IN COMMON THEN HAVING EXTRA SLOTS FOR DIFFERENT METADATA. 

"""
FEATUREVECTOR DOCUMENTATION:

This will keep track of what each slot in the FV corresponds to.


"""

def postToFV(post):
    fv = [] # need to decide on the structure for a general node FV, then use that here

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

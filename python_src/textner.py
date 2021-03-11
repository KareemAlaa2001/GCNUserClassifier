# import extraction
# from extraction import recentPosts
import stanza
import re
from stanza.server import CoreNLPClient
# print(extraction.recentUsers[0])

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
        memory='16G', classpath="../Libraries/stanford-corenlp-4.2.0/") as client:

        ann = client.annotate(text)
        sentence = ann.sentence[0]
        entities = sentence.nerTags
        print(entities)


    # print(testNerObj)
    # print(doc)\
    # for i in range(100,110):
    #     samplePost = recentPosts[i]
    #     print(samplePost['Body'])
    #     print('\n')
    #     print(cleanXML(samplePost['Body']))
    #     print('\n')

def basicNer(str):
    nlp = stanza.Pipeline(lang='en', processors='tokenize,ner')
    return nlp(str)

def cleanXML(string):
    return re.sub('<.*?>', '', string)

def convertStringToNER(string):
    string = cleanXML(string)
    # need to add in funcionality to take that and convert to a NER frequency vector
    # first need to be able to customise entity types in the stanza pipeline
    return string

if __name__ == '__main__':
    main()

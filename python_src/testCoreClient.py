from stanza.server import CoreNLPClient

text = "Constructing a sentence where Kareem Hussein, who works at Tesco in Welwyn, studies at the University of Southampton, likes to visit youtube.com and was born on 03/01/2001 8 hours after midday is not very hard. I have a twitter handle of @KareemAlaa2001, and my email is asdf54@gmail.com, which didn't get picked up?"
with CoreNLPClient(
        annotators=['tokenize','ssplit','pos','lemma','ner', 'parse', 'depparse','coref'],
        timeout=30000,
        memory='16G') as client:
    ann = client.annotate(text)
    sentences = ann.sentence
    for sent in sentences:
        for token in sent.token:
            print(token.word, token.ner)
    
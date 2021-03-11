from stanza.server import CoreNLPClient

text = "Chris Manning is a nice person. Chris wrote a simple sentence. He also gives oranges to people."
with CoreNLPClient(
        annotators=['tokenize','ssplit','pos','lemma','ner', 'parse', 'depparse','coref'],
        timeout=30000,
        memory='16G') as client:
    ann = client.annotate(text)
    sentences = ann.sentence
    for sent in sentences:
        print(sent.nerTags())
    
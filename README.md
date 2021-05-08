# Third Year Project README

This project is comprised of multiple parts: a specialised module for extracting and processing data from stackoverflow, then a generalised library for converting data from any dataset format to one usable by GCN, with an extra wrapper class for running GCN. 

## Stackoverflow-specific Module

This module handles extraction of posts, users and comments as well as their filtering to include posts in 2019 or later, the relevant comments and the users involved in either (or both). Hand-crafted featurevectors were built to extract information from each of these node types, using StanfordCoreNLP for Named Entity Recognition on the contents of the posts, comments and user descriptions to form a key part of those descriptions. 

## GCNPrepper Library:

### Purpose:

This library exists to abstract away some of the preprocessing work necessary to convert a dataset to a format usable by GCN, particularly dealing with the formation of adjacency matrices. The design is highly modular to allow for different data formats to be passed in, as well as different amounts of work to be done by those using the library.

## Pipeline Classes:

### FileExtractor:

This is a simple module for extracting data directly from a JSON or XML file into the reprentative python dictionary form. Note that the XML extractor only deals well with files that have a list of chidless entries, where attributes are taken as the K:V pairs. The JSON extractor is more robust. 

Usage of this module is entirely optional.

## CorpusReader:

This module can work in one of two ways:

### Schema-based:
This abstracts away the most work from the library user since it deals with processing the node lists/trees passed in and converts them directly to the GCN adjacency matrix. However, the data needs to conform to some format restrictions for this approach to work, which becomes clearer when the schema is explained, but at a glance, the attribute names need to be consistent between entries, and each node type needs to have an identifying attribute with unique IDs. IDs do not have to be unique between all nodes, however, just unique among nodes of that type.




##### Schema Format:

The schema takes up the following format:
schema = {
    NodeType1: {
        'idAtt': IDAttribKey,
        'featureAtts': [Feature1Key, Feature2Key...], 
        'linkAtts': {
            LinkAttributeKey1: Type of Neighbour linked,
            LinkAttributeKey2: Type of Neighbour linked,
            ...
        }
    },
    NodeType2: {
        'idAtt': IDAttribKey,
        'featureAtts': [Feature1Key, Feature2Key...], 
        'linkAtts': {
            LinkAttributeKey1: Type of Neighbour linked,
            LinkAttributeKey2: Type of Neighbour linked,
            ...
        }
    }
    ...
}

###### Broken down:

Top level: TypeNames: These define the names of the different node types present in the data. This allows for the presence of multiple node types in the dataset passed in. 

'idAtt': this should have the name of the identifying attribute containing the id for nodes of this type. THis MUST be present in the schema

'featureAtts': this is a list of the names of attributes which correspond to either numerical or text features.
**NOTE:** This is mostly here to help filter down the present attributes to those you see as 'useful' for your analysis, since this library mostly handles adjacency matrix building

'linkAtts': this is a list of key:value linkAttributeName:Neighbourtype, which is used by the internal parser to identify which nodes of which types are linked to the node in question. The inclusion of the Neighbourtype is necessary to allow for datasets with type-specific indexes, allowing for the handling of nodes of different types with the same numerical id. 

#### Schema-Based Corpus Reading Output:

The outputs of the schema-based CorpusReader include the GCN-ready adjacency matrix extracted based on the links found according to the information passed in schema. There is also an "indexGuide" output, which shows which node id of which type maps to each index (structure {nodetype: {nodid: gcn_graph_index}}), which is useful in order to know the order your node featurevectors will be placed in the data matrix. 

There is also the intermediate "Masterdict" form, which is a dict containing type:list of nodes of that type. Each node entry contains the key:value pairs for the attributes included in the schema.

# TODO Complete this

# Possible Expansionsss:
### Expand to more officially accommodate sql/sqlite dumps directly from a DB
### includes supporting whatever objects come out of an sqlite DB
### can also do the same for data coming out of a pandas dataframe
### can expand data format output forms to also support the DGL (Deep Graph Library) running GCN and whatnot
### can expand to allow for dataset updates to an existing DS
### can add stackoverflowNER to OGB, and I guess make them aware of the existence of the library ppl can use to create their own graph datasets from other formats????
### at the very least expand the formats output by this lib to be usable by pytorch
### Can Experiment with word and sentence level embeddings by using more sophisticated methods like BERT models and whatnot
### Experiment with allowing multiple edge types and directed edges. THis could be a very useful addition to the library
### Could also possibly integrate with networkx
#### can expand to accommodate datasets with mukltiple link types as well as directed graphs (this muifght already be a point lmao)
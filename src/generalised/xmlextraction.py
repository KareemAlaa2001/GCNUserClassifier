import xml.etree.ElementTree as ET


"""
Helper Module for extracting data from a selection of file types into the dictionary format used internally
"""

"""
IDEA: 
    I noticed that to make it meta here for the graph construction side I'm basically doing the same thing I did with the
    stackoverflow data. The same basic idea: we have different types of nodes, each with a different way to connect to other nodes.
    
    One way to look at the SO data I had was that it was a master dict, with each key being a nopdetype containing a list of 
    the dicts, each representing an individual instance

    Each dict contained information about 2 separate things that I had to customise based on the attributes, the actual features themselves, 
    and the separate link info. In my case, they were all jhumbled up in one big list of atts together, but what I could do is make it so that
    I can also pass in a data structure containing:

    {
        nodetype1: {
            identifyingattName: 'attname' (in SO this was 'Id')
            featureAttribs: {
                attribfeatureA: typeA, 
                attribFeatureB: typeB,
                attribFeatureC: typeC....
            }

            NOTE SHOULD FIRST FOCUS ON THESE BEFORE CONSIDERING FEATURE FLEXIBILITY, 
                SINCE COULD JUST RETURN INDEX: ENRTY MAPS AND ALLOW USER TO PASS THE FEATUREVECTORS THEMSELVES
            linkAttribs: {
                attribLinkA: nodeTypeLinkedA,
                attribLinkB: nodeTypeLinkedB,
                attribLinkC: nodeTypeLinkedC...
            }
        }
    }

"""

# TODO support Stuart's JSON output
"""
What I could do is convert stuart's graph representation to the lists of dicts structures I had, 
where each list would correspond to a certain nodetype


How is stuart's graph constructed? 

NodeTypes:

Thread:

    Each post has a thread id and post id assoc

{
  <website>_thread_<thread_id>_post_<post_id>: {
    "author": <author_name>,
    "page_url": <post_uri>,
    <sentence_index>: [
      {
        "entity": [
          <NER-label>:<phrase>,
          <NER-label>:<phrase>,
          ...
        ]
      }
    ],
    <sentence_index>: [
      {
        "entity": [
          <NER-label>:<phrase>,
          <NER-label>:<phrase>,
          ...
        ]
      }
    ],
    ...
  },
  <website>_thread_<thread_id>_post_<post_id>: {
    "author": <author_name>,
    "page_url": <post_uri>,
    <sentence_index>: [ ... ],
    ...
  }
}
"""

# extracting data from XML files into the 
def extractXMLFileToDict(filename):
    root = ET.parse(filename).getroot()
    
    # simple case for XML file structure (that it matches the SO Dump files)
    return listChildrenAttrib(root)
    
def listChildrenAttrib(node):
    childAttrib = []
    for child in node:
        childAttrib.append(child.attrib)

    return childAttrib

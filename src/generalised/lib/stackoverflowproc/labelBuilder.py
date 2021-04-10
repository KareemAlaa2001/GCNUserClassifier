# from lib.stackoverflowproc.extraction import recentComments, recentPosts, recentUsers
import xml.etree.ElementTree as ET
import html5lib
# from html5_parser import parse
# This module will have functions for the implementations of different types of labels. Some will be dependent on the data I've extracted, 
# while others will be based on other stuff extracted from the website



# function to get the label of a user according to diamond mod status ( sheriff badgeholders )



def getSheriffBadgeDisplayNames():
    sheriff_holders_filename = "lib/stackoverflowproc/Sheriff_Badgeholders_Meta.html"
    root = ET.parse(sheriff_holders_filename,ET.XMLParser(encoding='utf-8')).getroot()
    displayNameElems = root.findall(".//[@class='user-details']/a")

    print(displayNameElems)



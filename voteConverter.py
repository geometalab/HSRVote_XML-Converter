import xml.etree.ElementTree as ET
import sys

# How the text of certain nodes should be formatted
nwiki_snippets = {
    'QuestionText': '={node_text}=',
    'Answer1': '==1: {node_text}==',
    'Answer2': '==2: {node_text}==',
    'Answer3': '==3: {node_text}==',
    'Answer4': '==4: {node_text}==',
    'PictureQuestionText': '[[image:{node_text}|{node_text}]]',
    'PictureAnswer1': '==1:==\n[[image:{node_text}|{node_text}]]',
    'PictureAnswer2': '==2:==\n[[image:{node_text}|{node_text}]]',
    'PictureAnswer3': '==3:==\n[[image:{node_text}|{node_text}]]',
    'PictureAnswer4': '==4:==\n[[image:{node_text}|{node_text}]]',
    'Solution': "'''Solution: {node_text}'''"
    }

# Gets the text from the accepted nodes
def node_to_nwiki(node):
    if node.text is not None:
        nwiki_snippet = nwiki_snippets.get(node.tag)
        if nwiki_snippet is not None:
            if is_version_old:
                node_text = node.text.encode('utf-8')
            else:
                node_text = node.text
            return nwiki_snippet.format(node_text=node_text)

# Check if version is below 3
is_version_old = sys.version_info[0] < 3

# Parses a xml-file with the given name
if is_version_old:
    xml_name = raw_input('The name of your xml-file: ')
else:
    xml_name = input('The name of your xml-file: ')
xmlTree = ET.parse(xml_name)
file_name = xml_name.split('.')[0] + '.txt'
root = xmlTree.getroot()

# Creates a file containing nwiki-formatted data
with open(file_name, 'w') as w:
    assert root.tag == 'ArrayOfQuestion'
    for question in root:
        assert question.tag == 'Question'
        for node in question:
            nwiki_snippet = node_to_nwiki(node)
            if nwiki_snippet is not None:
                w.write(nwiki_snippet + '\n')
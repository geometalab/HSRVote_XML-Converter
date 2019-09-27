import xml.etree.ElementTree as ET
import sys

nwiki_snippets = {
    'QuestionText': '={node_text}=',
    'Answer1': '==A: {node_text}==',
    'Answer2': '==B: {node_text}==',
    'Answer3': '==C: {node_text}==',
    'Answer4': '==D: {node_text}==',
    'PictureQuestionText': '[[image:{node_text}|{node_text}]]',
    'PictureAnswer1': '==A:==\n[[image:{node_text}|{node_text}]]',
    'PictureAnswer2': '==B:==\n[[image:{node_text}|{node_text}]]',
    'PictureAnswer3': '==C:==\n[[image:{node_text}|{node_text}]]',
    'PictureAnswer4': '==D:==\n[[image:{node_text}|{node_text}]]',
    'Solution': "'''Solution: {node_text}'''"
    }

def node_to_nwiki(node):
    if node.text is not None:
        nwiki_snippet = nwiki_snippets.get(node.tag)
        if nwiki_snippet is not None:
            return nwiki_snippet.format(node_text=node.text)

        

#xmlTree = ET.parse(sys.argv[1])
xmlTree = ET.parse('BspFragen.xml') #for testing
root = xmlTree.getroot()

with open('wikitext.txt', 'w') as w:
    assert root.tag == 'ArrayOfQuestion'
    for question in root:
        assert question.tag == 'Question'
        for node in question:
            nwiki_snippet = node_to_nwiki(node)

            if nwiki_snippet is not None:
                w.write(nwiki_snippet + '\n')
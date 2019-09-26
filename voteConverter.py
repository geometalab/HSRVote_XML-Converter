import xml.etree.ElementTree as ET
import sys

def node_to_nwiki(node):
    if node.text is not None:
        nwiki_snippets = {
            'QuestionText': f'={node.text}=',
            'Answer1': f'==A: {node.text}==',
            'Answer2': f'==B: {node.text}==',
            'Answer3': f'==C: {node.text}==',
            'Answer4': f'==D: {node.text}==',
            'PictureQuestionText': f'[[image:{node.text}|{node.text}]]',
            'PictureAnswer1': f'==A:==\n[[image:{node.text}|{node.text}]]',
            'PictureAnswer2': f'==B:==\n[[image:{node.text}|{node.text}]]',
            'PictureAnswer3': f'==C:==\n[[image:{node.text}|{node.text}]]',
            'PictureAnswer4': f'==D:==\n[[image:{node.text}|{node.text}]]',
            'Solution': f"'''Solution: {node.text}'''"
            }
        return nwiki_snippets.get(node.tag)

        

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
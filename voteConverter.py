import xml.etree.ElementTree as ET
import sys

#xmlTree = ET.parse(sys.argv[1])
xmlTree = ET.parse('BspFragen.xml') #for testing
root = xmlTree.getroot()

assert root.tag == 'ArrayOfQuestion'
for question in root:
    assert question.tag == 'Question'
    for node in question:
        if node.text is not None:
            if node.tag == 'QuestionText':
                print(f'={node.text}=')
            elif node.tag == 'Answer1':
                print(f'==A: {node.text}==')
            elif node.tag == 'Answer2':
                print(f'==B: {node.text}==')
            elif node.tag == 'Answer3':
                print(f'==C: {node.text}==')
            elif node.tag == 'Answer4':
                print(f'==D: {node.text}==')
            elif node.tag == 'PictureQuestionText':
                print(f'[[image:{node.text}|{node.text}]]')
            elif node.tag == 'PictureAnswer1':
                print('==A:==')
                print(f'[[image:{node.text}|{node.text}]]')
            elif node.tag == 'PictureAnswer2':
                print('==B:==')
                print(f'[[image:{node.text}|{node.text}]]')
            elif node.tag == 'PictureAnswer3':
                print('==C:==')
                print(f'[[image:{node.text}|{node.text}]]')
            elif  node.tag == 'PictureAnswer4':
                print('==D:==')
                print(f'[[image:{node.text}|{node.text}]]')
            elif node.tag == 'Solution':
                print(f"'''Solution: {node.text}'''")
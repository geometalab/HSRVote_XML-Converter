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
                print('=' + node.text + '=')
            elif node.tag == 'Answer1':
                print('==A: ' + node.text + '==')
            elif node.tag == 'Answer2':
                print('==B: ' + node.text + '==')
            elif node.tag == 'Answer3':
                print('==C: ' + node.text + '==')
            elif node.tag == 'Answer4':
                print('==D: ' + node.text + '==')
            elif node.tag == 'PictureQuestionText':
                print('[[image:' + node.text + '|' + node.text + ']]')
            elif node.tag == 'PictureAnswer1':
                print('==A:==')
                print('[[image:' + node.text + '|' + node.text + ']]')
            elif node.tag == 'PictureAnswer2':
                print('==B:==')
                print('[[image:' + node.text + '|' + node.text + ']]')
            elif node.tag == 'PictureAnswer3':
                print('==C:==')
                print('[[image:' + node.text + '|' + node.text + ']]')
            elif  node.tag == 'PictureAnswer4':
                print('==D:==')
                print('[[image:' + node.text + '|' + node.text + ']]')
            elif node.tag == 'Solution':
                print("'''Solution: " + node.text + "'''")
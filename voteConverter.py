from xml.dom.minidom import parse, Node
import sys

#xmlTree = parse(sys.argv[1])
xmlTree = parse('BspFragen.xml') #for testing


for question in xmlTree.getElementsByTagName('Question'):
    for node in question.childNodes:
        for node2 in node.childNodes:
            temp = str(node)
            if ' QuestionText' in temp:
                print('=' + node2.data + '=')
            elif ' Answer1' in temp:
                print('==A: ' + node2.data + '==')
            elif ' Answer2' in temp:
                print('==B: ' + node2.data + '==')
            elif ' Answer3' in temp:
                print('==C: ' + node2.data + '==')
            elif ' Answer4' in temp:
                print('==D: ' + node2.data + '==')
            elif ' PictureQuestionText' in temp:
                print('[[image:' + node2.data + '|' + node2.data + ']]')
            elif ' PictureAnswer1' in temp:
                print('==A:==')
                print('[[image:' + node2.data + '|' + node2.data + ']]')
            elif ' PictureAnswer2' in temp:
                print('==B:==')
                print('[[image:' + node2.data + '|' + node2.data + ']]')
            elif ' PictureAnswer3' in temp:
                print('==C:==')
                print('[[image:' + node2.data + '|' + node2.data + ']]')
            elif ' PictureAnswer4' in temp:
                print('==D:==')
                print('[[image:' + node2.data + '|' + node2.data + ']]')
            elif ' Solution' in temp:
                print("'''Solution: " + node2.data + "'''")

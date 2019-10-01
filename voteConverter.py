import xml.etree.ElementTree as ET
import sys, getopt

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

def show_options():
    print('o')

def show_help():
    print('h')

def convert(xml_name, file_name, allow_overwrite):
    # Parses a xml-file with the given name
    xmlTree = ET.parse(xml_name)
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

argv = sys.argv[1:]
opts = []
args = []

try:
    opts, args = getopt.getopt(argv,'?',['help'])
except getopt.GetoptError:
    print('Use arguments correctly.\nWrite -? or --help for clarification.')
    sys.exit(2)

if not opts:
    if not args:
        show_options()
    elif len(args) > 3:
        print('Too many arguments.\nWrite -? or --help for clarification.')
    else:
        allow_overwrite = args[-1] in ('-o', '--overwrite')
        if args[0][-4:] == '.xml':
            xml_name = args[0]
            file_name = args[0].split('.')[0] + '.nwiki'
        else:
            print('First argument should be a .xml-file\nWrite -? or --help for clarification.')
            sys.exit()
        if len(args) > 1:
            if args[1][-6:] == '.nwiki':
                file_name = args[1]
            elif not allow_overwrite:
                print('Second argument should be a .nwiki-filename or -o.\nWrite -? or --help for clarification.')
                sys.exit()
        convert(xml_name, file_name, allow_overwrite)
elif opts[0][0] in ('-?', '--help'):
    show_help()
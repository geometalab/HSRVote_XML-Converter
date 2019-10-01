import xml.etree.ElementTree as ET
import sys, getopt
import os.path

# Check if version is above 3
if sys.version_info[0] >= 3:
    print('Python-version 3 or higher detected. Try the script "voteConverter.py"')
    sys.exit()

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

# Displays options
def show_options():
    print('''Converts xml-files to nwiki-files

python voteConverter2.py input [output] [-o | --overwrite] for converting
python voteConverter2.py [-? | --help] for help

  input\t\t\tSpecifies the xml-file to convert.
  output\t\tSpecifies the name of the nwiki-output-file.
  -o, --overwrite\tAllows a nwiki-file to get overwritten.''')

# Displays some examples
def show_help():
    print('''How to use voteConverter2.py:

  python voteConverter2.py example.xml
  \t-> Read the file "example.xml" and create "example.nwiki"

  python voteConverter2.py example.xml different.nwiki
  \t-> Read the file "example.xml" and create "different.nwiki"

  python voteConverter2.py example.xml -o
  \t-> Read the file "example.xml" and overwrite already existing "example.nwiki"
  
  python voteConverter2.py example.xml different.nwiki -o
  \t-> Read the file "example.xml" and overwrite already existing "differrent.nwiki"''')

def convert(xml_name, file_name):
    # Parses a xml-file with the given name
    try:
        xmlTree = ET.parse(xml_name)
    except IOError:
        print('The file {xml_name} does not exist'.format(xml_name=xml_name))
        sys.exit()
    except ET.ParseError:
        print('The file {xml_name} somehow cannot be parsed'.format(xml_name=xml_name))
        sys.exit()
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
            node_text = node.text.encode('utf-8')
            return nwiki_snippet.format(node_text=node_text)

# Read the given arguments from the console
argv = sys.argv[1:]
opts = []
args = []

# Specifies which opts are allowed
try:
    opts, args = getopt.getopt(argv,'?',['help'])
except getopt.GetoptError:
    print('Use arguments correctly.\nWrite -? or --help for clarification.')
    sys.exit(2)

# Handles the given options and arguments
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
            elif not (args[1] in ('-o', '--overwrite')):
                print('Second argument should be a .nwiki-filename, -o or --overwrite.\nWrite -? or --help for clarification.')
                sys.exit()
        if os.path.isfile(file_name) and not allow_overwrite:
            print('{file_name} already exists. Use -o or --overwrite to allow overwriting.\nWrite -? or --help for clarification.'.format(file_name=file_name))
        else:
            convert(xml_name, file_name)
elif opts[0][0] in ('-?', '--help'):
    show_help()
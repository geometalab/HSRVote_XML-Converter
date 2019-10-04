import xml.etree.ElementTree as ET
import sys, getopt
import os.path

# Check if version is below 3
if sys.version_info[0] < 3:
    print('Python-version below 3 detected. Try the script "voteConverter2.py"')
    sys.exit()

xml = '.xml'
nwiki = '.nwiki'
help = '\nWrite -? or --help for clarification.'

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

# Displays options and some examples
def show_help():
    print('''Converts xml-files to nwiki-files

python voteConverter.py input [output] [-o | --overwrite] for converting
python voteConverter.py [-? | --help] for help

  input\t\t\tSpecifies the xml-file to convert.
  output\t\tSpecifies the name of the nwiki-output-file.
  -o, --overwrite\tAllows a nwiki-file to get overwritten.

How to use voteConverter.py:

  python voteConverter.py example.xml
  \t-> Read the file "example.xml" and create "example.nwiki"

  python voteConverter.py example.xml different.nwiki
  \t-> Read the file "example.xml" and create "different.nwiki"

  python voteConverter.py example.xml -o
  \t-> Read the file "example.xml" and overwrite already existing "example.nwiki"
  
  python voteConverter.py example.xml different.nwiki -o
  \t-> Read the file "example.xml" and overwrite already existing "different.nwiki"''')

def convert(xml_name, file_name):
    # Parses a xml-file with the given name
    try:
        xmlTree = ET.parse(xml_name)
    except FileNotFoundError:
        print(f'The file {xml_name} does not exist')
        sys.exit()
    except ET.ParseError:
        print(f'The file {xml_name} somehow cannot be parsed')
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
            return nwiki_snippet.format(node_text=node.text)

# Read the given arguments from the console
argv = sys.argv[1:]
opts = []
args = []

# Specifies which opts are allowed
try:
    opts, args = getopt.getopt(argv,'?',['help'])
except getopt.GetoptError:
    print(f'Use arguments correctly.{help}')
    sys.exit(2)

# Handles the given options and arguments
if not opts:
    if not args:
        show_help()
    elif len(args) > 3:
        print(f'Too many arguments.{help}')
    else:
        allow_overwrite = args[-1] in ('-o', '--overwrite')
        if args[0][-4:] == xml:
            xml_name = args[0]
            file_name = args[0].split('.')[0] + nwiki
        else:
            print(f'First argument should be a .xml-file{help}')
            sys.exit()
        if len(args) > 1:
            if args[1][-6:] == nwiki:
                file_name = args[1]
            elif not (args[1] in ('-o', '--overwrite')):
                print(f'Second argument should be a .nwiki-filename, -o or --overwrite.{help}')
                sys.exit()
        if os.path.isfile(file_name) and not allow_overwrite:
            print(f'{file_name} already exists. Use -o or --overwrite to allow overwriting.{help}')
        else:
            try:
                convert(xml_name, file_name)
                print(f'Conversion complete. New file {file_name} created')
            except:
                print('Conversion failed.')
elif opts[0][0] in ('-?', '--help'):
    show_help()
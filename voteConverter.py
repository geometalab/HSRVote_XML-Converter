import xml.etree.ElementTree as ET
import argparse
from pathlib import Path
import sys

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

examples = '''How to use voteConverter.py:

  python voteConverter.py example.xml
  \t-> Read the file "example.xml" and create "example.nwiki"

  python voteConverter.py example.xml different.nwiki
  \t-> Read the file "example.xml" and create "different.nwiki"

  python voteConverter.py example.xml -o
  \t-> Read the file "example.xml" and overwrite already existing "example.nwiki"
  
  python voteConverter.py example.xml different.nwiki -o
  \t-> Read the file "example.xml" and overwrite already existing "different.nwiki"'''

def main():
    args = parse_arguments()
    input_file = Path(args.input)
    output_file = input_file.parent / f'{input_file.stem}.nwiki' if args.output is None else Path(args.output)
    if output_file.exists() and not args.overwrite:
        print(f'{output_file} already exists. Use -o or --overwrite to allow overwriting.')
        sys.exit(1)
    try:
        convert(input_file, output_file)
        print(f'Conversion complete. New file {output_file} created')
    except:
        print('Conversion failed.')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Converts xml-files to nwiki-files', epilog=examples, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('input', type=str, help='the xml-file to convert')
    parser.add_argument('output', type=str, nargs='?', help='the name of the nwiki-output-file')
    parser.add_argument('-o', '--overwrite', action='store_true', help='if given, overwrite an existing nwiki-file if present')
    return parser.parse_args()

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

if __name__ == '__main__':
    main()
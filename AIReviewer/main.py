from pylint import lint
from pylint.reporters.text import TextReporter
from io import StringIO
from pathlib import Path
import ast


def get_node_with_error(tree, line_number):
    for node in tree:
        if node.lineno - 1 <= line_number - 1 <= node.end_lineno - 1:
            if isinstance(node, ast.ClassDef):
                if child_node := get_node_with_error(node.body, line_number):
                    return child_node
            return node


def get_errors_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()
        file_content_lines = file_content.splitlines()

    tree = [node for node in ast.walk(ast.parse(file_content)) if hasattr(node, 'lineno')]

    pylint_output = StringIO()

    # Create a Pylint TextReporter to write output to the buffer
    reporter = TextReporter(pylint_output)

    # Run Pylint with the specified arguments
    lint.Run([str(file_path)], reporter=reporter, exit=False)

    # Get the output as a string
    for error in pylint_output.getvalue().splitlines()[1:-4]:
        file_name, error_msg = error.split(' ', maxsplit=1)
        file_name, line_number, char_number = file_name.strip(':').rsplit(':', maxsplit=2)
        line_number, char_number = int(line_number), int(char_number)
        if file_content_lines[line_number-1].strip().startswith('#'):
            continue
        if node := get_node_with_error(tree, line_number):
            print(line_number-node.lineno+1, char_number, error_msg)
            print('\n'.join(file_content_lines[node.lineno-1:node.end_lineno]))
            print('\n\n##########################################################\n\n')


if __name__ == '__main__':
    get_errors_from_file(Path(r"C:\Progs\ODBBrowser\v.5.18.6\bin\presentation\comp_widgets.py"))

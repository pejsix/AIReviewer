from pylint import lint
from pylint.reporters.text import TextReporter
from io import StringIO
from pathlib import Path
import ast

from AIReviewer.openai_interface import ErrorsDetector


class FileParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_node_with_error(self, tree, line_number):
        for node in tree:
            if node.lineno - 1 <= line_number - 1 <= node.end_lineno - 1:
                if isinstance(node, ast.ClassDef):
                    if child_node := self.get_node_with_error(node.body, line_number):
                        return child_node
                return node

    def get_errors_from_file(self, selected_algorithm):
        if selected_algorithm == 'PyLint':
            return self.get_errors_from_file_pylint()
        elif selected_algorithm == 'OpenAI':
            return self.get_errors_from_file_openai()

    def get_errors_from_file_pylint(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
            file_content_lines = file_content.splitlines()

        tree = [node for node in ast.walk(ast.parse(file_content)) if hasattr(node, 'lineno')]

        pylint_output = StringIO()

        # Create a Pylint TextReporter to write output to the buffer
        reporter = TextReporter(pylint_output)

        # Run Pylint with the specified arguments
        lint.Run([str(self.file_path)], reporter=reporter, exit=False)

        line_numbers = {}
        for error in pylint_output.getvalue().splitlines()[1:-4]:
            file_name, error_msg = error.split(' ', maxsplit=1)
            file_name, line_number, char_number = file_name.strip(':').rsplit(':', maxsplit=2)
            line_number, char_number = int(line_number), int(char_number)
            if file_content_lines[line_number - 1].strip().startswith('#'):
                continue
            if node := self.get_node_with_error(tree, line_number):
                code_block = '\n'.join(file_content_lines[node.lineno - 1:node.end_lineno])
                line_numbers[line_number] = (
                code_block, line_number, char_number, error_msg, node.lineno - 1, node.end_lineno - 1)

        return line_numbers

    def get_errors_from_file_openai(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
            file_content_lines = file_content.splitlines()

        tree = [node for node in ast.walk(ast.parse(file_content)) if hasattr(node, 'lineno')]

        line_numbers = {}
        detected_errors = ErrorsDetector().get_error_detection(file_content).splitlines()
        for error in detected_errors:
            line_number, error_msg = error.split(' ', maxsplit=1)
            line_number, char_number = int(line_number), 0
            if file_content_lines[line_number - 1].strip().startswith('#'):
                continue
            if node := self.get_node_with_error(tree, line_number):
                code_block = '\n'.join(file_content_lines[node.lineno - 1:node.end_lineno])
                line_numbers[line_number] = (code_block, line_number, char_number, error_msg)

        return line_numbers


if __name__ == '__main__':
    file_parser = FileParser(r"C:\Progs\ODBBrowser\v.5.18.6\bin\presentation\comp_widgets.py")
    file_parser.get_errors_from_file_openai()
    # get_errors_from_file(Path(r"C:\Progs\ODBBrowser\v.5.18.6\bin\presentation\comp_widgets.py"))

import streamlit as st
from streamlit_ace import st_ace
from AIReviewer.file_parser import FileParser
from AIReviewer.openai_interface import ErrorsSolver
import os

# Get the source directory from environment variables
SOURCE_DIR = os.getenv("SOURCE_DIR_CONFIG_FILE_PATH")


# Function to list all Python files in the specified directory
def list_files():
    """
    Lists all Python files in the source directory.

    Returns:
    list: A list of filenames (str) of all Python files in the source directory.
    """
    return [f for f in os.listdir(SOURCE_DIR) if f.endswith('.py')]


# Function to read the content of a file
def read_file(file_path):
    """
    Reads the content of a file from the source directory.

    Parameters:
    file_path (str): The relative path to the file to read.

    Returns:
    str: The content of the file.
    """
    with open(os.path.join(SOURCE_DIR, file_path), 'r', encoding='utf-8') as file:
        return file.read()


# Function to replace a block of code in a file with a new block of code
def apply_change_to_file(selected_file, line_index_start, line_index_end, new_block):
    """
    Replaces a block of code in a file with a new block of code.

    Parameters:
    selected_file (str): The path to the file to modify.
    line_index_start (int): The starting line index of the block to replace.
    line_index_end (int): The ending line index of the block to replace.
    new_block (str): The new block of code to insert.

    Returns:
    None
    """
    with open(selected_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        lines = [line.rstrip('\n') for line in lines]

        # Split the new block into lines
        new_lines = new_block.split('\n')

        # Replace the old block with the new block
        updated_lines = lines[:line_index_start] + new_lines + lines[line_index_end + 1:]

        # Write the updated content back to the file
        with open(selected_file, 'w', encoding='utf-8') as file:
            file.writelines('\n'.join(updated_lines) + '\n')


# JavaScript code to add the underline marker
underline_js = """
<script>
    // Function to add underline marker to a line
    function addUnderline(editor, line) {

        // Define a custom class for the underline
        var css = `.ace_line.underline { border-bottom: 2px solid red !important; }`,
            head = document.head || document.getElementsByTagName('head')[0],
            style = document.createElement('style');

        style.type = 'text/css';
        if (style.styleSheet) {
            style.styleSheet.cssText = css;
        } else {
            style.appendChild(document.createTextNode(css));
        }
        head.appendChild(style);

        // Add the marker to the line
        editor.session.addMarker(new (window.ace).Range(line, 0, line, 1), 'underline', 'fullLine');
    }

    // Wait for the editor to be available
    setTimeout(() => {
        console.warn("test")
        var editor = window.ace.edit("ace-editor-{selected_file}");
        if (editor) {
            addUnderline(editor, {line_number});
        }
    }, 1000);
</script>
"""


# Main function to set up the Streamlit app layout and functionality
def main():
    """
    Main function to set up the Streamlit app layout and functionality.

    The app allows users to view Python files, select errors in the code,
    view corrections, and apply the corrections to the files.
    """
    st.set_page_config(layout="wide")  # Set the layout to wide

    st.sidebar.title("Python Code Viewer")

    # Sidebar for file selection
    files = list_files()
    selected_file = st.sidebar.selectbox("Choose a file", files, key="file_selector")

    # Sidebar for algorithm selection
    algorithms = ['PyLint', 'OpenAI']
    selected_algorithm = st.sidebar.selectbox("Choose a method to get errors", algorithms)

    # Read and display the content of the selected file
    file_content = read_file(selected_file)
    file_parser = FileParser(os.path.join(SOURCE_DIR, selected_file))

    # Check if algorithm or file has changed and update session state accordingly
    if "selected_algorithm" not in st.session_state or selected_algorithm != st.session_state.selected_algorithm or \
            "selected_file" not in st.session_state or selected_file != st.session_state.selected_file:
        st.session_state.selected_algorithm = selected_algorithm
        st.session_state.selected_file = selected_file
        st.session_state.line_numbers = file_parser.get_errors_from_file(selected_algorithm)

    # Select and display a specific error
    selected_error = st.sidebar.selectbox("Choose an error", st.session_state.line_numbers.keys())

    code_block, line_number, char_number, error_msg, block_line_start, block_line_end = st.session_state.line_numbers[
        selected_error]

    # Check if error has changed and update session state accordingly
    if "selected_algorithm" not in st.session_state or selected_algorithm != st.session_state.selected_algorithm or \
            "selected_file" not in st.session_state or selected_file != st.session_state.selected_file or \
            "selected_error" not in st.session_state or selected_error != st.session_state.selected_error:
        st.session_state.selected_error = selected_error
        solver = ErrorsSolver()
        st.session_state.correction = solver.get_error_correction(code_block, line_number, char_number, error_msg)

    # Sidebar to display the selected error message
    st.sidebar.subheader("Found error")
    st.sidebar.text(error_msg)

    # Sidebar to display the correction code
    st.sidebar.subheader("Fixes Code")
    st.sidebar.code(st.session_state.correction, language='python')

    # Button to apply the correction to the file
    apply_change = st.sidebar.button("Apply change", key="apply_change")
    if apply_change:
        selected_file_path = os.path.join(SOURCE_DIR, selected_file)
        apply_change_to_file(selected_file_path, block_line_start, block_line_end, st.session_state.correction)
        st.rerun()

    # Ace editor for displaying the file content with syntax highlighting
    st.subheader("Source Code")
    st_ace(
        value=file_content,
        language='python',
        theme='monokai',
        readonly=False,
        height=1000,
        key=f'ace-editor-{selected_file}',  # Ensure unique key per file
    )


if __name__ == "__main__":
    main()

import streamlit as st
from streamlit_ace import st_ace
from AIReviewer.file_parser import FileParser
from AIReviewer.openai_interface import ErrorsSolver
import os


SOURCE_DIR = os.getenv("SOURCE_DIR_CONFIG_FILE_PATH")


# Function to list all Python files in the current directory
def list_files():
    return [f for f in os.listdir(SOURCE_DIR) if f.endswith('.py')]


# Function to read a file
def read_file(file_path):
    with open(os.path.join(SOURCE_DIR, file_path), 'r', encoding='utf-8') as file:
        return file.read()

# Take a file and replace the block with an error with a new block with error removed.
def apply_change_to_file(selected_file, line_index_start, line_index_end, new_block):
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


# Streamlit app layout
def main():
    st.set_page_config(layout="wide")  # Set the layout to wide

    st.sidebar.title("Python Code Viewer")

    # Sidebar for file selection
    files = list_files()
    selected_file = st.sidebar.selectbox("Choose a file", files, key="file_selector")

    algorithms = ['PyLint', 'OpenAI']
    selected_algorithm = st.sidebar.selectbox("Choose a method to get errors", algorithms)

    # Read and display the content of the selected file
    file_content = read_file(selected_file)
    file_parser = FileParser(os.path.join(SOURCE_DIR, selected_file))
    if "selected_algorithm" not in st.session_state or selected_algorithm != st.session_state.selected_algorithm or \
            "selected_file" not in st.session_state or selected_file != st.session_state.selected_file:
        st.session_state.selected_algorithm = selected_algorithm
        st.session_state.selected_file = selected_file
        st.session_state.line_numbers = file_parser.get_errors_from_file(selected_algorithm)

    selected_error = st.sidebar.selectbox("Choose a error", st.session_state.line_numbers.keys())

    code_block, line_number, char_number, error_msg, block_line_start, block_line_end = st.session_state.line_numbers[selected_error]

    if "selected_algorithm" not in st.session_state or selected_algorithm != st.session_state.selected_algorithm or \
            "selected_file" not in st.session_state or selected_file != st.session_state.selected_file or \
            "selected_error" not in st.session_state or selected_error != st.session_state.selected_error:
        st.session_state.selected_error = selected_error
        solver = ErrorsSolver()
        st.session_state.correction = solver.get_error_correction(code_block, line_number, char_number, error_msg)

    st.sidebar.subheader("Found error")
    st.sidebar.text(error_msg)
    st.sidebar.subheader("Fixes Code")
    st.sidebar.code(st.session_state.correction, language='python')
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
        # annotations=[{"row": line_number-1, "column": char_number, "type": "underline", "text": error_msg} for
        #            _, line_number, char_number, error_msg in st.session_state.line_numbers.values()]
    )


if __name__ == "__main__":
    main()

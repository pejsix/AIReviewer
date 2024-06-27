import streamlit as st
from streamlit_ace import st_ace
import os


# Function to list all Python files in the current directory
def list_files():
    return [f for f in os.listdir() if f.endswith('.py')]


# Function to read a file
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


# Streamlit app layout
def main():
    st.title("Python Code Viewer")

    # Sidebar for file selection
    st.sidebar.header("Select a Python file")
    files = list_files()

    if files:
        selected_file = st.sidebar.selectbox("Choose a file", files)
        if selected_file:
            st.sidebar.write(f"Selected file: {selected_file}")

            # Read and display the content of the selected file
            file_content = read_file(selected_file)

            # Ace editor for displaying the file content with syntax highlighting
            st.subheader("Source Code")
            st_ace(
                value=file_content,
                language='python',
                theme='monokai',
                readonly=False,
                height=500,
                key='ace-editor'
            )
    else:
        st.sidebar.write("No Python files found in the current directory.")


if __name__ == "__main__":
    main()

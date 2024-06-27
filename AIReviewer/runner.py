import os
import subprocess
import sys

OPENAI_API_KEY_PATH = "../openai_key.txt"
SOURCE_DIR_CONFIG_FILE_PATH = "../path_to_data.txt"

def get_openai_api_key():
    with open(OPENAI_API_KEY_PATH, "r", encoding="utf-8") as f:
        openai_api_key = f.readline().strip()
    os.environ["OPENAI_API_KEY"] = openai_api_key

def get_source_dir():
    with open(SOURCE_DIR_CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
        source_dir = f.readline().strip()
    os.environ["SOURCE_DIR_CONFIG_FILE_PATH"] = source_dir

def run_streamlit_app():

    # Set environment variables.
    get_openai_api_key()
    get_source_dir()

    # Define the path to your Streamlit app
    streamlit_app_path = os.path.abspath('AIReviewer\\streamlit_app.py')  # Replace with your Streamlit app path
 
    python_dir = os.path.dirname(sys.executable)
    streamlit_path = python_dir + '\\streamlit.exe'
    print(streamlit_path)
    # Run the Streamlit app
    subprocess.run([streamlit_path, 'run', streamlit_app_path])

if __name__ == "__main__":
    run_streamlit_app()
import os
import subprocess
import sys

OPENAI_API_KEY_PATH = "../openai_key.txt"

def get_openai_api_key():
        with open(OPENAI_API_KEY_PATH, "r") as f:
            openai_api_key = f.readline().strip()
        return openai_api_key

def run_streamlit_app():
    # Set the environment variable
    
    os.environ["OPENAI_API_KEY"] = get_openai_api_key()

    # Define the path to your Streamlit app
    streamlit_app_path = os.path.abspath('AIReviewer\\streamlit_app.py')  # Replace with your Streamlit app path
 
    python_dir = os.path.dirname(sys.executable)
    streamlit_path = python_dir + '\\streamlit.exe'
    print(streamlit_path)
    # Run the Streamlit app
    subprocess.run([streamlit_path, 'run', streamlit_app_path])

if __name__ == "__main__":
    run_streamlit_app()
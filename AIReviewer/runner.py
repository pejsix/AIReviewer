import os
import subprocess
import sys

# Path to the file containing the OpenAI API key
OPENAI_API_KEY_PATH = "../openai_key.txt"

# Path to the file containing the source directory path
SOURCE_DIR_CONFIG_FILE_PATH = "../path_to_data.txt"


def get_openai_api_key():
    """
    Reads the OpenAI API key from a file and sets it as an environment variable.

    The function reads the API key from the file specified by `OPENAI_API_KEY_PATH`,
    strips any leading or trailing whitespace, and sets the key as the `OPENAI_API_KEY`
    environment variable.

    Returns:
    None
    """
    with open(OPENAI_API_KEY_PATH, "r", encoding="utf-8") as f:
        openai_api_key = f.readline().strip()
    os.environ["OPENAI_API_KEY"] = openai_api_key


def get_source_dir():
    """
    Reads the source directory path from a file and sets it as an environment variable.

    The function reads the directory path from the file specified by `SOURCE_DIR_CONFIG_FILE_PATH`,
    strips any leading or trailing whitespace, and sets the path as the `SOURCE_DIR_CONFIG_FILE_PATH`
    environment variable.

    Returns:
    None
    """
    with open(SOURCE_DIR_CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
        source_dir = f.readline().strip()
    os.environ["SOURCE_DIR_CONFIG_FILE_PATH"] = source_dir


def run_streamlit_app():
    """
    Sets environment variables and runs the Streamlit application.

    The function sets the `OPENAI_API_KEY` and `SOURCE_DIR_CONFIG_FILE_PATH` environment variables
    by reading from specified files. Then, it determines the path to the Streamlit executable and
    runs the Streamlit app specified by `streamlit_app_path`.

    Returns:
    None
    """
    # Set environment variables.
    get_openai_api_key()
    get_source_dir()

    # Define the path to your Streamlit app
    streamlit_app_path = os.path.abspath('AIReviewer\\streamlit_app.py')  # Replace with your Streamlit app path

    python_dir = os.path.dirname(sys.executable)
    streamlit_path = os.path.join(python_dir, 'streamlit.exe')
    print(streamlit_path)

    # Run the Streamlit app
    subprocess.run([streamlit_path, 'run', streamlit_app_path])


if __name__ == "__main__":
    """
    Entry point of the script. Executes the `run_streamlit_app` function.

    The script is designed to set necessary environment variables and launch the
    Streamlit application specified in the code.

    Returns:
    None
    """
    run_streamlit_app()

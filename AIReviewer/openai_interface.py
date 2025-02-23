import openai
import os


class ErrorsSolver:
    """
    Class for solving coding errors using OpenAI's language models.
    """
    OPENAI_API_KEY_PATH = "../openai_key.txt"
    MODEL = "gpt-4o"
    SYSTEM_MESSAGE = {
        'role': 'system',
        'content': "You are a skilled coding assistant. As an input, you get a codeblock with an error,"
                   "the location of the error and an error message. You should return the same codeblock"
                   "but the specified error should be removed."
                   "DO NOT USE MARKDOWN!!! Be careful not to introduce another error!"
                   "IT IS CRUCIAL TO RETURN ONLY CODE, no other text should be included!!!!!!!!!!!!!!"
    }

    ERROR_SPECIFICATION_TPL = ("THE BLOCK OF CODE: {0}\n"
                               "LINE: {1}\n"
                               "COLUMN: {2}\n"
                               "ERROR MESSAGE: {3}")

    def __init__(self):
        """
        Initialize the ErrorsSolver class by setting up the OpenAI API client.
        """
        if "OPENAI_API_KEY" not in os.environ:
            self.openai_api_key = self.get_openai_api_key()
            os.environ["OPENAI_API_KEY"] = self.openai_api_key
        self.client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

    def get_openai_api_key(self):
        """
        Retrieve the OpenAI API key from a file.

        Returns:
            str: The OpenAI API key.
        """
        with open(self.OPENAI_API_KEY_PATH, "r") as f:
            openai_api_key = f.readline().strip()
        return openai_api_key

    def get_error_correction(self, block: str, line: int, column: int, message: str) -> str:
        """
        Get corrected code for the given code block with an error.

        Args:
            block (str): The block of code containing the error.
            line (int): The line number where the error occurs.
            column (int): The column number where the error occurs.
            message (str): The error message describing the issue.

        Returns:
            str: The corrected code block.
        """
        user_message = self.create_user_message(block, line, column, message)
        response = self.client.chat.completions.create(
            model=self.MODEL,  # You can use other models as well
            messages=[self.SYSTEM_MESSAGE, user_message]
        )
        return response.choices[0].message.content

    def create_user_message(self, block: str, line: int, column: int, message: str) -> dict:
        """
        Create a user message for the OpenAI API call.

        Args:
            block (str): The block of code containing the error.
            line (int): The line number where the error occurs.
            column (int): The column number where the error occurs.
            message (str): The error message describing the issue.

        Returns:
            dict: The user message in the required format.
        """
        error_specification = self.ERROR_SPECIFICATION_TPL.format(block, line, column, message)
        user_message = {
            'role': 'user',
            'content': error_specification
        }
        return user_message


class ErrorsDetector:
    """
    Class for detecting coding errors in Python source files using OpenAI's language models.
    """
    OPENAI_API_KEY_PATH = "../openai_key.txt"
    MODEL = "gpt-4o"
    SYSTEM_MESSAGE = {
        'role': 'system',
        'content': "You are a skilled coding assistant. As an input, you get a python source code file."
                   "Detects common bugs and security vulnerabilities. Ensures consistency in code formatting and style."
                   "Checks for syntax errors, code smells, and adherence to coding standards."
                   "YOUR OUTPUT WILL BE IN FOLLOWING FORMAT!!!!!!!!!!!!!!!!!!"
                   "EACH PROBLEM YOU FIND WILL BE ON INDIVIDUAL LINE!!!!!!!!!!!!!!"
                   "ON THE LINE WILL BE JUST LINE_NUMBER FOLLOWED BY AN ERROR DESCRIPTION, NOTHING ELSE!!!!!!!!!!!!!!"
                   "YOU WILL GET A BIG REWARD IF YOU CORRECTLY FOLLOW ALL MY INSTRUCTION!!!!!!!!!!!!!!"
    }

    def __init__(self):
        """
        Initialize the ErrorsDetector class by setting up the OpenAI API client.
        """
        if "OPENAI_API_KEY" not in os.environ:
            self.openai_api_key = self.get_openai_api_key()
            os.environ["OPENAI_API_KEY"] = self.openai_api_key
        self.client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))
        print("class ErrorsDetector:")

    def get_openai_api_key(self):
        """
        Retrieve the OpenAI API key from a file.

        Returns:
            str: The OpenAI API key.
        """
        with open(self.OPENAI_API_KEY_PATH, "r") as f:
            openai_api_key = f.readline().strip()
        return openai_api_key

    def get_error_detection(self, file_content: str) -> str:
        """
        Get a list of detected errors in the given Python source code.

        Args:
            file_content (str): The Python source code content.

        Returns:
            str: The list of detected errors, one per line.
        """
        secondary_system_message = self.create_secondary_system_message(file_content)
        user_message = self.create_user_message(file_content)
        response = self.client.chat.completions.create(
            model=self.MODEL,  # You can use other models as well
            messages=[self.SYSTEM_MESSAGE, secondary_system_message, user_message],
            temperature=0
        )
        return response.choices[0].message.content

    def create_user_message(self, file_content: str) -> dict:
        """
        Create a user message for the OpenAI API call.

        Args:
            file_content (str): The Python source code content.

        Returns:
            dict: The user message in the required format.
        """
        user_message = {
            'role': 'user',
            'content': f'Here is my python code, where you should find the problems:\n'
                       f'{file_content}'
        }
        return user_message

    def create_secondary_system_message(self, file_content: str) -> dict:
        """
        Create a secondary system message specifying the file's line count.

        Args:
            file_content (str): The Python source code content.

        Returns:
            dict: The secondary system message.
        """
        max_line_number = len(file_content.splitlines())
        secondary_system_message = {
            'role': 'system',
            'content': f"MAKE SURE THAT YOU HAVE THE LINE NUMBERS CORRECT!!!!!!!!!!!!!!!!!!"
                       f"FILE CONTENT HAS {max_line_number} LINES. "
                       f"YOU WILL NOT RETURN LINE NUMBER HIGHER THAN {max_line_number}"
        }
        return secondary_system_message


if __name__ == "__main__":
    block = ("def add(a, b):\n"
             "return a + b\n"
             "\n"
             "def unused_function()\n:"
             "    pass"
             "\n"
             "result = add(2, 3)\n"
             "print(result)")
    line = 2
    column = 0
    message = "E111 indentation is not a multiple of four"
    errors_solver = ErrorsSolver()
    response = errors_solver.get_error_correction(block, line, column, message)
    print(response)

import openai
import os

class ErrorsSolver:
    OPENAI_API_KEY_PATH = "../openai_key.txt"
    MODEL = "gpt-4o"
    SYSTEM_MESSAGE = {
        'role': 'system',
        'content': "You are a skilled coding assistant. As an input, you get a codeblock with an error,"
                   "the location of the error and an error message. You should return the same codeblock"
                   "but the specified error should be removed. Be careful not to introduce another error!"
                   "IT IS CRUCIAL TO RETURN ONLY CODE, no other text should be included!!!!!!!!!!!!!!"
        }
    
    ERROR_SPECIFICATION_TPL = ("THE BLOCK OF CODE: {0}\n"
                               "LINE: {1}\n"
                               "COLUMN: {2}\n"
                               "ERROR MESSAGE: {3}")

    def __init__(self):
        self.openai_api_key = self.get_openai_api_key()
        os.environ["OPENAI_API_KEY"] = self.openai_api_key
        self.client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))
    
    def get_openai_api_key(self):
        with open(self.OPENAI_API_KEY_PATH, "r") as f:
            openai_api_key = f.readline().strip()
        return openai_api_key

    def get_error_correction(self, block: str, line: int, column: int, message: str):
        user_message = self.create_user_message(block, line, column, message)
        response = self.client.chat.completions.create(
            model=self.MODEL,  # You can use other models as well
            messages=[self.SYSTEM_MESSAGE, user_message]
        )
        return response.choices[0].message.content

    def create_user_message(self, block: str, line: int, column: int, message: str):
        error_specification = self.ERROR_SPECIFICATION_TPL.format(block, line, column, message)
        user_message = {
            'role': 'user',
            'content': error_specification
        }
        return user_message


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

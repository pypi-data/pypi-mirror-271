"""
This file contains code for the application "Gemini Random Generator".
Author: SoftwareApkDev
"""


# Importing necessary libraries


import re
import google.generativeai as gemini
import sys
import os
from dotenv import load_dotenv
from mpmath import mp, mpf

mp.pretty = True


# Creating static functions to be used in this application.


def is_number(string: str) -> bool:
    try:
        mpf(string)
        return True
    except ValueError:
        return False


def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System


# Creating main function used to run the application.


def main() -> int:
    """
    This main function is used to run the application.
    :return: an integer
    """

    load_dotenv()
    gemini.configure(api_key=os.environ['GEMINI_API_KEY'])

    # Asking user input values for generation config
    temperature: str = input("Please enter temperature (0 - 1): ")
    while not is_number(temperature) or float(temperature) < 0 or float(temperature) > 1:
        temperature = input("Sorry, invalid input! Please re-enter temperature (0 - 1): ")

    float_temperature: float = float(temperature)

    top_p: str = input("Please enter Top P (0 - 1): ")
    while not is_number(top_p) or float(top_p) < 0 or float(top_p) > 1:
        top_p = input("Sorry, invalid input! Please re-enter Top P (0 - 1): ")

    float_top_p: float = float(top_p)

    top_k: str = input("Please enter Top K (at least 1): ")
    while not is_number(top_k) or int(top_k) < 1:
        top_k = input("Sorry, invalid input! Please re-enter Top K (at least 1): ")

    float_top_k: int = int(top_k)

    max_output_tokens: str = input("Please enter maximum input tokens (at least 1): ")
    while not is_number(max_output_tokens) or int(max_output_tokens) < 1:
        max_output_tokens = input("Sorry, invalid input! Please re-enter maximum input tokens (at least 1): ")

    int_max_output_tokens: int = int(max_output_tokens)

    # Set up the model
    generation_config = {
        "temperature": float_temperature,
        "top_p": float_top_p,
        "top_k": float_top_k,
        "max_output_tokens": int_max_output_tokens,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_ONLY_HIGH"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_ONLY_HIGH"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_ONLY_HIGH"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_ONLY_HIGH"
        },
    ]

    model = gemini.GenerativeModel(model_name="gemini-1.0-pro",
                                   generation_config=generation_config,
                                   safety_settings=safety_settings)

    convo = model.start_chat(history=[
    ])

    while True:
        clear()
        rndgen_file_path: str = input("Please enter path of the \".rndgen\" file you want to parse: ")
        while not rndgen_file_path[-7:] == ".rndgen":
            rndgen_file_path: str = input("Sorry, invalid input! "
                                          "Please enter path of the \".rndgen\" file you want to parse: ")

        rndgen_file = open(rndgen_file_path, "r")
        rndgen_file_contents: str = rndgen_file.read()
        rndgen_file.close()

        matches: list = re.findall(r"\$\{([^\}]*)\}", rndgen_file_contents)
        for match in matches:
            convo.send_message("Please generate a random " + str(match) + " (safe response only please)!")
            replacement_text: str = str(convo.last.text)
            rndgen_file_contents = rndgen_file_contents.replace("${" + str(match) + "}", replacement_text, 1)

        text_file_name: str = input("Please enter the name of the text file you want the "
                                    "generated text to be placed in (include the extension please): ")
        text_file = open("../texts/" + str(text_file_name), "w")
        text_file.write(rndgen_file_contents)
        text_file.close()

        print("Enter \"Y\" for yes.")
        print("Enter anything else for no.")
        continue_using: str = input("Do you want to continue using the random generator? ")
        if continue_using != "Y":
            return 0


if __name__ == '__main__':
    main()

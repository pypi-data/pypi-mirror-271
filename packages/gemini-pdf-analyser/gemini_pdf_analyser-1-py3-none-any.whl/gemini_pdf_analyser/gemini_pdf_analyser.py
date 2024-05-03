"""
This file contains code for the application "Gemini PDF Analyser".
Author: SoftwareApkDev
"""


# Importing necessary libraries


import PyPDF2
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


def extract_text_from_pdf(pdf_path: str):
    text: str = ""
    with open(pdf_path, "rb") as file:
        pdf_reader: PyPDF2.PdfReader = PyPDF2.PdfReader(file)
        num_pages: int = len(pdf_reader.pages)
        for page_number in range(num_pages):
            page: PyPDF2.PageObject = pdf_reader.pages[page_number]
            text += page.extract_text()
    return text


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
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    model = gemini.GenerativeModel(model_name="gemini-1.0-pro",
                                   generation_config=generation_config,
                                   safety_settings=safety_settings)

    convo = model.start_chat(history=[
    ])

    while True:
        clear()
        pdf_file_path: str = input("Please enter the path of the PDF file you want to analyse: ")
        pdf_file_contents: str = extract_text_from_pdf(pdf_file_path)
        question: str = input("Please enter your question: ")
        prompt: str = """
        """ + str(pdf_file_contents) + """

        The contents of the PDF file """ + str(pdf_file_path) + """ are as above.
        Please answer the following question based on the information given above!
        If the answer cannot be deduced from the given information, please answer "I don't know"!        

        Question: """ + str(question) + """
        """
        convo.send_message(prompt)
        response: str = str(convo.last.text)
        print("Answer: " + str(response))

        print("Enter 'Y' for yes.")
        print("Enter anything else for no.")
        continue_translating: str = input("Do you want to continue analysing PDF files? ")
        if continue_translating != "Y":
            return 0


if __name__ == '__main__':
    main()

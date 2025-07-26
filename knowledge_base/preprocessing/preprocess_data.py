import os
from bnlp import CleanText
from pdfminer.high_level import extract_text


clean_config = CleanText(
        fix_unicode=True,
        unicode_norm=True,
        unicode_norm_form="NFKC",
        remove_url=False,
        remove_email=False,
        remove_emoji=True,
        remove_number=False,
        remove_digits=False,
        remove_punct=False,
        replace_with_url="<URL>",
        replace_with_email="<EMAIL>",
        replace_with_number="<NUMBER>",
        replace_with_digit="<DIGIT>",
        replace_with_punct="<PUNC>"
)


def process_data_file(file_path: str, save_txt: bool = False, clean_output: bool = False) -> [str]:
    """
    Primary function for processing a data file, which in this case is a pdf file. This calls all the actual
    processing functions defined in this file.

    Args:
        file_path: path to the pdf file to extract text from
        save_txt: whether or not to save the extracted text as a text file before processing
        clean_output: whether or not to clean the extracted text

    Returns: processed and cleaned text as a list of strings
    """

    extracted_text = extract_text(file_path)

    if save_txt:
        save_text_output(og_file_path=file_path, extracted_text=extracted_text)

    if clean_output:
        cleaned_text = clean_extracted_text(text_to_clean=extracted_text)
        return cleaned_text

    return extracted_text.split("\n")


def save_text_output(og_file_path: str, extracted_text: str):
    """
    Save the extracted text as a text file inside the output directory.

    Args:
        og_file_path: path to the original pdf file
        extracted_text: extracted text as a single string

    """

    file_name = og_file_path.split(os.sep)[-1]

    os.makedirs(os.path.join("..", "output"), exist_ok=True)
    text_save_path = os.path.join("..", "output", file_name.split(".")[0] + ".txt")

    with open(text_save_path, "w", encoding="utf-8") as f:
        f.write(extracted_text)


def clean_extracted_text(text_to_clean: str) -> [str]:
    """
    Clean the extracted text and return a list of strings. Cleaning is done using bnlp's clean function.

    Args:
        text_to_clean: the text to be cleaned as a single string

    Returns: the text, separated into lines and cleaned, as a list of strings
    """

    text_lines = text_to_clean.split("\n")
    cleaned_text_lines = []

    for _, line_text in enumerate(text_lines):

        if len(line_text) < 5:
            continue

        clean_text = clean_config(line_text)
        clean_text = clean_text.strip()

        cleaned_text_lines.append(clean_text)

    return cleaned_text_lines


if __name__ == '__main__':

    """The main is mainly for testing purposes. This file is only used for the cleaning functions."""

    data_source = os.path.join("..", "data")
    data_files = os.listdir(data_source)

    for file in data_files:
        process_data_file(file_path=os.path.join(data_source, file), save_txt=False, clean_output=True)




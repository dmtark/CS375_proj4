'''Creates a dictionary based off of CS375 assignment pdfs'''
from tika import parser # pip install tika
import os
import re


def parse_latex_file(pdf_filename: str) -> set:
    """Return a set containing all words in a pdf file."""
    raw = parser.from_file(pdf_filename)
    raw_data = raw['content']
    words = re.findall(r"[a-zA-Z\'\-]+", raw_data)
    words = [word.lower() for word in words]
    return set(words)

def pdf_to_string(pdf_filename: str) -> str:
    """Return a string of raw text contained in a pdf."""
    raw = parser.from_file(pdf_filename)
    raw_data = raw['content']
    pdf_string = str(raw_data)
    return pdf_string


def pdf_file_names(directory: str) -> list:
    """Return a list of the pdf filenames in a given directory."""
    all_files = os.listdir(directory)
    pdf_files = [f"{directory}/{str(filename)}" for filename in all_files if str(filename).endswith(".pdf")]

    return pdf_files


def master_set_from_pdf_list(pdf_list: list) -> set:
    """Return a master set of all words in a list of pdf files."""
    master_set = set()

    for filename in pdf_list:
        file_set = parse_latex_file(filename)
        master_set.update(file_set)

    return master_set


def write_set_to_txt_file(word_set: set, filepath: str) -> None:
    """Write a set of words to a txt file, one word per line."""
    set_list = list(word_set)

    with open(filepath, "w") as file:
        file.write("\n".join(set_list))


def main():
    names = pdf_file_names("./assignments")
    master_set = master_set_from_pdf_list(names)
    write_set_to_txt_file(master_set, "cs375_word_set.txt")



if __name__ == "__main__":
    main()
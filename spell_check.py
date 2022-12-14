# spell check file for unimproved spell check
from tika import parser
import re
import sys
import csv
import pprint

class SpellCheck:
    def __init__(self, pdf_filename, dict_name):
        self.pdf_filename = pdf_filename
        self.dict_name = dict_name
        # self.text = "this is a semple santence with a frw gramnatixal erors"

        # load_dictionary
        with open(self.dict_name, 'r') as f:
            lines = []
            for line in f:
                lines.append(line.strip().lower())

        self.word_set = set(lines)

        # load in pdf file
        raw = parser.from_file(pdf_filename)
        raw_data = raw['content']
        pdf_string = str(raw_data)
        self.text = pdf_string


    def edit_distance(self, S: str, T: str) -> int:
        """Return the edit distance from s to t iteratively."""
        s = len(S)
        t = len(T)
        result = [[0] * (t + 1) for _ in range(s+ 1)]
        for i in range(s + 1):
            result[i][0] = i
        for j in range(t + 1):
            result[0][j] = j

        for i in range(1, s+1):
            for j in range(1, t+1):
                min_val = min( result[i-1][j], result[i][j-1], result[i-1][j-1] )
                # left: result[i-1][j]
                # up: result[i][j-1]
                # diagnol: result[i-1][j-1]
                if S[i-1] == T[j-1]: # same
                    result[i][j] = result[i-1][j-1]
                else:
                    result[i][j] = 1 + min_val

        return result[s][t]
            # if current cells have different letters, add one to minimum between left, up, and diagonol
            # if the same, add zero to the minimum of those

    def spell_check_word_basic(self, word: str) -> list:
        """Return a list containing the closest word to input word."""
        dictionary = self.word_set
        min_words = []
        min_distance = 1000
        for correct_word in dictionary:
            dist = self.edit_distance(word, correct_word)
            if dist < min_distance:
                min_words = [correct_word] # all of the words with min_distance
                min_distance = dist
            elif dist == min_distance:
                min_words.append(correct_word)
        return min_words


    def spell_check_word_with_edit_distance(self, word:str):
        """Return a tuple (spelled_correctly, suggestions, num_suggestions).
        Receives a pre-cleaned word."""
        if word in self.word_set:
            spelled_correctly = True
            suggestions = [word]
            num_suggestions = 0
        else:
            spelled_correctly = False
            # get suggested words
            min_words = self.spell_check_word_basic(word)
            suggestions = min_words
            num_suggestions = len(min_words)
        return spelled_correctly, suggestions, num_suggestions

    
    def get_basic_dict(self, typo_list):
        # creates and returns a dictionary containing:
            # key: misspelled word
            # value: the length of the suggested replacements (only the primary words)
        basic_dict = {}
        for i, item in enumerate(typo_list):
            basic_dict[typo_list[i][1]] = typo_list[i][3]
        return basic_dict


    def spell_check_text_basic(self) -> list:
        """Return a list of misspelled words.
        Each index has form:
        (text_index, misspelled_word, suggestions, num_suggestions)."""

        # create a list of misspelled words
        typo_list = []

        for index, word in enumerate(self.text.split()):
        # for index, word in enumerate(re.split('\s|\u8212|\u0045', self.text)):
            
            # make lowercase
            word = word.lower()
            # remove anything that's not a lowercase letter
            word = re.sub(r'[^a-z]', '', word)

            if len(word) > 0:

                spelled_correctly, min_words, num_suggestions = self.spell_check_word_with_edit_distance(word)

                if not spelled_correctly:
                    # add the index, misspelled word, and best suggestion to the typo list
                    typo_list.append(
                        (index, word, min_words, num_suggestions)
                    )

        return typo_list

    '''
    def spell_check_text(self, verbose=False):
        dictionary = self.word_set
        for word in self.text.split():
            word = word.lower() # interesting... names??
            # word = word.strip(".,!/;'")
            word = word.strip("1234567890")
            word = re.sub(r'[^a-zA-Z0-9]', '', word)
            word = re.sub(r"[\n\t\s]*", "", word)
            if word == "":
                continue
            if word not in dictionary:
                print("\nMispelled word: " + word)
                potential_correct_words = self.spell_check_word(word)
                print("Potential correct words: " + str(potential_correct_words))
        if verbose:
            return word, potential_correct_words

        return potential_correct_words
    '''

    def write_to_csv(self, dictionary):
        fields = ['Misspelled Word', 'Improved Number of Suggestions']
        rows = []
        for item in dictionary:
            rows.append([item, dictionary[item]])

        with open('basic_dict.csv', 'w') as csvfile: 
            csvwriter = csv.writer(csvfile) 
            csvwriter.writerow(fields) 
            csvwriter.writerows(rows)
        

    def run_spell_check(self):
        return self.spell_check_text_basic()


    def print_spell_check(self):
        """Print the typos in readable format."""
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint( self.spell_check_text_basic() )


def main():
    basic = SpellCheck('CS375f22_proj4_DynamicProgramming.pdf', 'cs375_word_set.txt')
    basic.print_spell_check()


if __name__ == "__main__":
    main()
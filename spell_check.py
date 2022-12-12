# spell check file for unimproved spell check
from tika import parser
import re
import sys

class SpellCheck:
    def __init__(self, pdf_filename, dict_name, text):
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

    def spell_check_word(self, word: str) -> list:
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


    def spell_check_text(self):
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
        return potential_correct_words

    def run_spell_check(self):
        return self.spell_check_text()


def main():
    spell_check1 = SpellCheck('cs375f22_SA3.pdf', 'en_US-large.txt', 'cs375f22_SA3.pdf')

    print("Running normal spell check:\n")
    spell_check = spell_check1.run_spell_check()
    print(spell_check)

if __name__ == "__main__":
    main()
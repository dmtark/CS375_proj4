from temp import edit_distance
from tika import parser
import re
import sys
import pprint
import csv


class Improvements:

    def __init__(self, pdf_filename, dict_name):
        self.pdf_filename = pdf_filename
        self.dict_name = dict_name
        self.word_scores = {}

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

        self.graph = { "a" : ["q", "w", "s", "z"],
                "b" : ["v", "g", "h", "n"],
                "c" : ["x", "d", "f", "v"],
                "d" : ["s", "e", "r", "f", "v", "c", "x"],
                "e" : ["w", "r", "d", "s"],
                "f" : ["d", "e", "r", "t", "g", "v", "c"],
                "g" : ["f", "t", "y", "h", "b", "v"],
                "h" : ["g", "y", "u", "j", "n", "b"],
                "i" : ["u", "o", "l", "k", "j"],
                "j" : ["h", "u", "i", "k", "m", "n"],
                "k" : ["j", "i", "o", "l", "m"],
                "l" : ["k", "o", "p"],
                "m" : ["n", "j", "k"],
                "n" : ["b", "h", "j", "m"],
                "o" : ["p", "l", "k", "i"],
                "p" : ["o", "l"],
                "q" : ["a", "s"],
                "r" : ["e", "d", "f", "g", "t"],
                "s" : ["a", "w", "e", "d", "x", "z"],
                "t" : ["r", "f", "g", "h", "y"],
                "u" : ["y", "h", "j", "k", "i"],
                "v" : ["c", "f", "g", "b"],
                "w" : ["q", "a", "s", "d", "e"],
                "x" : ["z", "s", "d", "c"],
                "y" : ["t", "g", "h", "u"],
                "z" : ["a", "s", "x"]
            }

        print("object created")

    def getNeighbors(self, node):
        "Return a list of neighbors of node"
        return self.graph.get(node, [node])
        # second [node] gives us default


    def find_edit_distance(self, S: str, T: str) -> int:
        """Return the edit distance from s to t iteratively."""
        s = len(S)
        t = len(T)
        # Create a table for storing values
        result = [[0] * (t + 1) for _ in range(s + 1)]
        # Populate table with 0s on the top row and left column
        for i in range(s + 1):
            result[i][0] = i
        for j in range(t + 1):
            result[0][j] = j

        for i in range(1, s+1):
            for j in range(1, t+1):
                # left: result[i-1][j]
                # up: result[i][j-1]
                # diagnol: result[i-1][j-1]
                if S[i-1] == T[j-1]: # same
                    result[i][j] = result[i-1][j-1]
                else:
                    min_val = min( result[i-1][j], result[i][j-1], result[i-1][j-1] )
                    result[i][j] = 1 + min_val

        return result[s][t]
            # if current cells have different letters, add one to minimum between left, up, and diagonol
            # if the same, add zero to the minimum of those


    def spell_check_word_improved(self, word):
        """Return two lists:
        lowest edit distance and second-lowest edit distance."""
        min_words = []
        min_words_secondary = []
        min_distance = 1000
        min_distance_secondary = 1000
        for correct_word in self.word_set:
            dist = self.find_edit_distance(word, correct_word)
            if dist < min_distance:
                min_words_secondary = min_words
                min_distance_secondary = min_distance
                min_words = [correct_word]
                min_distance = dist
            elif dist == min_distance:
                min_words.append(correct_word)
            elif min_distance < dist < min_distance_secondary:
                min_distance_secondary = dist
                min_words_secondary = [correct_word]

        return min_words, min_words_secondary

    def get_score(self, orig_word, min_words):
        word_scores = {}
        # print("The typo:", orig_word)
        # print("The minimum words:", min_words)
        for suggested_word in min_words:
            # strip word and original word, then revert back to list
            correct_chars = set(suggested_word).difference(set(orig_word))
            chars_changed  = set(orig_word).difference(set(suggested_word))
            correct_chars = list(correct_chars)
            chars_changed = list(chars_changed)
            score = 0
            # for each correct character, see if the changed character is a neighbor of the new correct character
            for c in correct_chars:
                neighbors = self.getNeighbors(c)
                for cc in chars_changed:
                    if cc in neighbors:
                        score = score + 1
            # add the score to the word
            word_scores[suggested_word] = score

        return word_scores


    def spell_check_word(self, word:str):
        """Return a tuple (spelled_correctly, best_suggestion).
        Receives a pre-cleaned word."""
        if word in self.word_set:
            spelled_correctly = True
            best_suggestion = word
            num_suggestions = 0
        else:
            spelled_correctly = False
            # get suggested words
            (min_words, secondary) = self.spell_check_word_improved(word)
            num_suggestions = len(min_words)
            # if there is only one suggestion, return it
            if len(min_words) == 1:
                best_suggestion = min_words[0]
            else:
                # get the scores of all minimum words
                scores = self.get_score(word, min_words)

                # get the best score
                best_score = -1
                for score in scores:
                    suggestion_score = scores[score]
                    # if this is the best score yet
                    if suggestion_score > best_score:
                        best_suggestion = score
                        best_score = suggestion_score
        return spelled_correctly, best_suggestion, num_suggestions


    def get_improved_dict(self, typo_list):
        # creates and returns a dictionary containing:
            # key: misspelled word
            # value: the length of the suggested replacements (only the primary words)
        improvement_dict = {}
        for i, item in enumerate(typo_list):
            improvement_dict[typo_list[i][1]] = typo_list[i][3]
        return improvement_dict


    def spell_check_text(self) -> list:
        """Return a list of misspelled words.
        Each index has form:
        (text_index, misspelled_word, best_suggestion)."""

        # create a list of misspelled words
        typo_list = []

        for index, word in enumerate(self.text.split()):
        # for index, word in enumerate(re.split('\s|\u8212|\u0045', self.text)):
            
            # make lowercase
            word = word.lower()
            # remove anything that's not a lowercase letter
            word = re.sub(r'[^a-z]', '', word)

            if len(word) > 0:

                spelled_correctly, best_suggestion, num_suggestions = self.spell_check_word(word)

                if not spelled_correctly:
                    # add the index, misspelled word, and best suggestion to the typo list
                    typo_list.append(
                        (index, word, best_suggestion, num_suggestions)
                    )

        return typo_list

    def write_to_csv(self, dictionary):
        fields = ['Misspelled Word', 'Improved Number of Suggestions']
        rows = []
        for item in dictionary:
            rows.append([item, dictionary[item]])

        with open('improvements_dict.csv', 'w') as csvfile: 
            csvwriter = csv.writer(csvfile) 
            csvwriter.writerow(fields) 
            csvwriter.writerows(rows)

    def run_spell_check(self):
        """Print the typos in readable format."""
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint( self.spell_check_text() )

def main():
    improvement = Improvements('CS375f22_proj4_DynamicProgramming.pdf', 'cs375_word_set.txt')
    improvement.run_spell_check()


if __name__ == "__main__":
    main()

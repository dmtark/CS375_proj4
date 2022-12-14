"""
CS375 - Project 4 - Implementing edit distance
Calvin Whitley
Daniel Tarkoff
Milo Lani-Caputo
Brett Torra
"""

from timeit import default_timer as timer
import pprint
from tika import parser
import re
import sys

class EditDistance:

    def __init__():
        pass


    def find_edit_distance_recursive(s: str, t: str) -> int:
        """Return the edit distance of s to t recursively."""
        if s == "" or t == "":
            if s == "":
                return len(t)
            elif t == "":
                return len(s)
        else:
            if s[len(s) - 1] == t[len(t) - 1]:
                return find_edit_distance_recursive(
                    s[0:len(s) - 1],
                    t[0:len(t) - 1]
                )
            else:
                min_val = min(
                    find_edit_distance_recursive(
                        s[0:len(s) - 1],
                        t[0:len(t) - 1]
                    ),
                    find_edit_distance_recursive(
                        s[0:len(s) - 1],
                        t[0:len(t)]
                    ),
                    find_edit_distance_recursive(
                        s[0:len(s)],
                        t[0:len(t) - 1]
                    ),
                )

                return min_val + 1


    def find_edit_distance_iterative(S: str, T: str) -> int:
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
                if S[i-1] == T[j-1]:
                    result[i][j] = result[i-1][j-1]
                else:
                    min_val = min( result[i-1][j], result[i][j-1], result[i-1][j-1] )
                    result[i][j] = 1 + min_val

        return result[s][t]


    def multiple_trials():
        '''Runs both recursive and iterative edit distance methods 
        with simulated increasing input sizes and returns two lists
        of times, one for recursive and iterative. It returns the time
        taken to run the edit_distance on each input size.'''
        iter_list = []
        recur_list = []
        my_dict = {'crozy':'crazy', 'elehabet':'elephant', 'grapt':'graph', 'grann':'grown', 'krll':'kill',
                    'jnin':'water', 'llugh':'laugh', 'eig':'eight', 'ninine':'nine', 'teni':'tennis'}
        for i in range(10):
            start_recursive = timer()
            for x in range(0,2**i):
                for word in my_dict.items():
                    find_edit_distance_recursive(word[0],word[1])
            end_recursive = timer()

            start_iter = timer()
            for x in range(0,2**i):
                for word in my_dict.items():
                    find_edit_distance_iterative(word[0],word[1])
            end_iter = timer()
            print(2**i)
            iter_list.append(end_iter-start_iter)
            recur_list.append(end_recursive-start_recursive)
        return iter_list,recur_list


class SpellCheck:
    '''
    Spell-check class to create our basic spell checking algorithm (unimproved)
    Takes 2 parameters:
        pdf_filename: the pdf you want to spell check (we will be using 'cs375_proj4_DynammicProgramming.pdf)
        dict_name: the dictionary you want to use for spell checkgin (we use 'cs375_word_set')
    '''
    def __init__(self, pdf_filename, dict_name):
        self.pdf_filename = pdf_filename
        self.dict_name = dict_name

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
        """Return the edit distance from S to T iteratively."""
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


    def spell_check_text_basic(self) -> list:
        """Return a list of misspelled words.
        Each index has form:
        (text_index, misspelled_word, suggestions, num_suggestions)."""

        # create a list of misspelled words
        typo_list = []

        for index, word in enumerate(self.text.split()):            
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
        

    def run_spell_check(self):
        return self.spell_check_text_basic()


    def print_spell_check(self):
        """Print the typos in readable format."""
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint( self.spell_check_text_basic() )


class Improvements:
    """
    Improved spell-check class to create our basic spell checking algorithm.
    Selects best option among words with lowest edit distance.
    Takes 2 parameters:
        pdf_filename: the pdf you want to spell check (we will be using 'cs375_proj4_DynammicProgramming.pdf)
        dict_name: the dictionary you want to use for spell checking (we use 'cs375_word_set')
        """

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

        # keyboard adjacency map
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


    def getNeighbors(self, node):
        """Return a list of neighbors of node."""
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
        """Return the scores of suggested words based on keyboard adjacency.
        Higher scores mean higher keyboard adjacency."""
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


    def spell_check_text(self) -> list:
        """Return a list of misspelled words.
        Each index has form:
        (text_index, misspelled_word, best_suggestion)."""

        # create a list of misspelled words
        typo_list = []

        for index, word in enumerate(self.text.split()):
            
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


    def run_spell_check(self):
        """Print the typos in readable format."""
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint( self.spell_check_text() )


def main():

    if len(sys.argv) == 3:
        dict_method = sys.argv[2]
    else:
        dict_method = "cs375_word_set.txt"

    if sys.argv[1] == "basic":
            basic_spell_checker = SpellCheck('CS375f22_proj4_DynamicProgramming.pdf', dict_method)
            basic_spell_checker.print_spell_check()
    elif sys.argv[1] == "improved":
        improvement = Improvements('CS375f22_proj4_DynamicProgramming.pdf', dict_method)
        improvement.run_spell_check()
    else:
        print("usage: <basic | improved> <cs375_word_set.txt | cs375_combined_set.txt>")
        print("file CS375f22_proj4_DynamicProgramming.pdf must be in same directory")


if __name__ == "__main__":
    main()
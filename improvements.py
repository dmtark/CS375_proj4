from temp import edit_distance
from tika import parser
import re
import sys

# TODO: make load_dictionary method a field

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

    def getNeighbors(self, node):
        graph = { "a" : ["q", "w", "s", "z"],
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

        return graph.get(node, [node])
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
            elif dist == min_distance:
                min_distance.append(correct_word)
        return min_words, min_words_secondary

    def get_score(self, orig_word, min_words):
        word_scores = {}
        print("The typo:", orig_word)
        print("The minimum words:", min_words)
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
            word_scores[suggested_word] = [self.find_edit_distance(orig_word, suggested_word), score]

        return word_scores


    # def score(self, potential, real):
    #     # how do we want to weight this??
    #     score = 10 - self.find_edit_distance(potential, real)
    #     if potential[0] == real[0]:
    #         score += 1
    #     if len(potential) == len(real):
    #         score += 1
    #     if potential[-1] == real[-1]:
    #         score += 1
    #     print(potential + " score: " + str(score))
    #     return score
    #     # takes in a word, gives us a "score" for a word - return the word with the maximum score


    def spell_check_text(self):
        for word in self.text.split():
            word = word.lower() # interesting... names??
            # word = word.strip(".,!/;'()0123456789:`")

            word = word.strip("1234567890")
            word = re.sub(r'[^a-zA-Z0-9]', '', word)
            word = re.sub(r"[\n\t\s]*", "", word)

            if word not in self.word_set and len(word) != 0:
                # print("\nMispelled word: " + word)
                (min_words, secondary) = self.spell_check_word_improved(word)
                scores = self.get_score(word,min_words)

                # get the best score
                best_score = -1
                best_word = None
                for x in scores:
                    if scores[x][1] > best_score:
                        best_word = x
                        best_score = int(word_scores[x][1])
                # print(scores)
                # print("Minimum edit distance words:\n" + str(min_words))
                # print("Secondary edit distance words:\n" + str(secondary) + "\n\n\n")


        # return "Replacement: " + max(min_words + secondary, key=lambda x: score(x, word))

    def run_spell_check(self):
        return self.spell_check_text()

def main():
    improvement = Improvements('cs375f22_hw0.pdf', 'cs375_word_set.txt')
    improvement.get_score("fyn", ["fun", "fin"])

if __name__ == "__main__":
    main()

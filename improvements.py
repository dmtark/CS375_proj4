from temp import edit_distance
from tika import parser
import re
import sys

# TODO: make load_dictionary method a field

class Improvements:

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


    def improved_edit_distance(self, S, T):

        s = len(S)
        t = len(T)
        result = [[0] * (t + 1) for _ in range(s+ 1)]
        for i in range(s + 1):
            result[i][0] = i
        for j in range(t + 1):
            result[0][j] = j

        for i in range(1, s+1):
            for j in range(1, t+1):
                # making list of potential values for this spot in the array
                # three options we always have + 2 other options: if equal to matching character, that's the best option; or: 
                potential_values = [result[i-1][j] + 1, result[i][j-1] + 1, result[i-1][j-1] + 1]
                if S[i-1] == T[j-1]: # same
                    potential_values.append(result[i-1][j-1])
                elif S[i-1] in self.getNeighbors(T[j-1]):
                    # in the neighbor list
                    potential_values.append(result[i-1][j-1] + 0.5) # maybe change value from 0.5 to something else            
                result[i][j] = min(potential_values)
        return result[s][t]


    def spell_check_word_improved(self, word):
        min_words = []
        min_words_secondary = []
        min_distance = 1000
        min_distance_secondary = 1000
        for correct_word in self.word_set:
            dist = self.improved_edit_distance(word, correct_word)
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


    def score(self, potential, real):
        # how do we want to weight this??
        score = 10 - self.improved_edit_distance(potential, real)
        if potential[0] == real[0]:
            score += 1
        if len(potential) == len(real):
            score += 1
        if potential[-1] == real[-1]:
            score += 1
        print(potential + " score: " + str(score))
        return score
        # takes in a word, gives us a "score" for a word - return the word with the maximum score


    def spell_check_text(self):
        for word in self.text.split():
            word = word.lower() # interesting... names??
            word = word.strip(".,!/;'")
            if word not in self.word_set:
                print("\nMispelled word: " + word)
                (min_words, secondary) = self.spell_check_word_improved(word)
                print("Minimum edit distance words:\n" + min_words)
                print("\nSecondary edit distance words:\n" + secondary)

        return "Replacement: " + max(min_words + secondary, key=lambda x: score(x, word))

    def run_spell_check(self):
        return self.spell_check_text()

def main():
    improvement = Improvements('cs375f22_SA3.pdf', 'en_US-large.txt', 'cs375f22_SA3.pdf')
    print(improvement.spell_check_text())

if __name__ == "__main__":
    main()
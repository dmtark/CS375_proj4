import temp

def load_dictionary(filename):
        with open(filename, 'r') as f:
            lines = []
            for line in f:
                lines.append(line.strip())
        return lines

def edit_distance(S, T):
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

def spell_check_word(word, dictionary):
    min_words = []
    min_distance = 1000
    for correct_word in dictionary:
        dist = edit_distance(word, correct_word)
        if dist < min_distance:
            min_words = [correct_word]
            min_distance = dist
        elif dist == min_distance:
            min_words.append(correct_word)
    return min_words

def spell_check(text, dictionary):
    for word in text.split():
        word = word.lower() # interesting... names??
        word = word.strip(".,!/;'")
        if word not in dictionary:
            print("wrong word: " + word)
            correct_word = spell_check_word(word, dictionary)
            print("correct word: " + str(correct_word))
    # new
    return correct_word


# potential improvement:
def pick_best_words(potential_words, original_word):
    # removes potentially correct words that do not start with the same letter
    final_words = []
    for word in potential_words:
        if word[0] == original_word[0]:
            final_words.append(word)
    return final_words


def spell_check_better(text, dictionary):
    dict_set = set(dictionary) # will have O(1) lookup time
    for word in text.split():
        word = word.lower() # interesting... names??
        word = word.strip(".,!/;'") # splits on any of these characters
        if word not in dict_set:
            print("wrong word: " + word + "\n\n")
            correct_words = spell_check_word(word, dictionary) # returns a list of words with minimum edit distance
            improved_correct_words = pick_best_words(correct_words, word)
            print("potentially correct words: " + str(improved_correct_words))
    # new
    return improved_correct_words



def run_spell_check(text):
    dictionary = load_dictionary('en_US-large.txt')
    spell_check(text, dictionary)

def run_spell_check_better(text):
    # runs with normal US dictionary AND first improvement
    dictionary = load_dictionary('en_US-large.txt')
    spell_check_better(text, dictionary)


# create general method that scores the quality of the words


def add_keyboard_graph(keyboard_graph):
    # what we want to do:
        # add a graph connecting all letters to each other
    graph = { "a" : ["q", "w", "s", "z"],
          "b" : ["v", "g", "h", "n"],
          "c" : ["x", "d", "f", "v"],
          "d" : ["s", "e", "r", "f", "v", "c", "x"],
          "e" : ["w", "r", "d", "s"],
          "f" : ["d," "e", "r", "t", "g", "v", "c"]
    }

def getNeighbors(graph, node):
    return graph[node]



# implementation attempt for pick_best_words_NEW
# def pick_best_words_NEW(potential_words, original_word):
#     # removes potentially correct words that do not start with the same letter
#     final_words = []
#     for word in potential_words:
#         if word[0] == original_word[0]:
#             for i in range(len(word-1)): # might be issues with index out of bounds?
#                 if original_word[i] in word[i+1].getNeighbors():
#                     final_words.append(word)
#     return final_words


def spell_check_with_keyboard_graph(text, graph):
    dict_set = set(dictionary)
    for word in text.split():
        word = word.lower()
        word = word.strip(".,!/;'")
        if word not in dict_set:
            print("wrong word: " + word + "\n\n")
            correct_words = spell_check_word(word, dictionary) # returns a list of words with minimum edit distance
            improved_correct_words = pick_best_words_NEW(correct_words, word)
            print("potentially correct words: " + str(improved_correct_words))
    # new
    return improved_correct_words


def main():
    text = "helro what is uour nam? nice to mert you"
    print("Running normal spell check:\n")
    spell_check_normal = run_spell_check(text)

    print("Running improved spell check:\n")
    spell_check_better = run_spell_check_better(text)
    


if __name__ == "__main__":
    main()
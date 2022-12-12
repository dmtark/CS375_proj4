from temp import edit_distance

def getNeighbors(node):
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


def edit_distance_with_graph(S, T):

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
            elif S[i-1] in getNeighbors(T[j-1]):
                # in the neighbor list
                potential_values.append(result[i-1][j-1] + 0.5) # maybe change value from 0.5 to something else            
            result[i][j] = min(potential_values)
    return result[s][t]


def spell_check_word(word, dictionary):
    min_words = []
    min_distance = 1000
    for correct_word in dictionary:
        dist = edit_distance_with_graph(word, correct_word)
        if dist < min_distance:
            min_words = [correct_word]
            min_distance = dist
        elif dist == min_distance:
            min_words.append(correct_word)
    return min_words

def spell_check_word_improved(word, dictionary):
    min_words = []
    min_words_secondary = []
    min_distance = 1000
    min_distance_secondary = 1000
    for correct_word in dictionary:
        dist = edit_distance_with_graph(word, correct_word)
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


def load_dictionary(filename):
        with open(filename, 'r') as f:
            lines = []
            for line in f:
                lines.append(line.strip())
        return lines


def score(potential, real):
    # how do we want to weight this??
    score = 10 - edit_distance_with_graph(potential, real)
    if potential[0] == real[0]:
        score += 1
    if len(potential) == len(real):
        score += 1
    if potential[-1] == real[-1]:
        score += 1
    print(potential + " score: " + str(score))
    return score
    # takes in a word, gives us a "score" for a word - return the word with the maximum score


def main():
    my_dict = load_dictionary('us_dict.txt')
    text = "helro what is yoor nam? nice to mert you"
    word = 'broim'
    (min_words, secondary) = spell_check_word_improved(word, my_dict)
    print("min words: \n" + str(min_words))
    print("\nSecondary words:\n" + str(secondary))

    result = max(min_words + secondary, key=lambda x: score(x, word))
    # gets the max based off the above lambda function
    print(result)

if __name__ == "__main__":
    main()
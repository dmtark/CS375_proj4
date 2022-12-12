class SpellCheck:

    def __init__(filename):
        this.filename = filename


    def load_dictionary(filename):
        with open(self.filename, 'r') as f:
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

    def spell_check_better(text, dictionary):
        dict_set = set(dictionary) # will have O(1) lookup time
        for word in text.split():
            word = word.lower() # interesting... names??
            word = word.strip(".,!/;'")
            if word not in dict_set:
                print("wrong word: " + word)
                correct_word = spell_check_word(word, dictionary)
                print("correct word: " + str(correct_word))


    def pick_best_word(potential_words, original_word):
        final_words = []
        for word in potential_words:
            if word[0] == original_word:
                final_words.append(word)
        return final_words



def main():
    # S = "aaaDaniel"
    # T = "DanielTarkoff"

    # result = edit_distance(S, T)
    # print(result)

    test1 = SpellCheck('sample.txt')

    text = "Hello. My namm is Daniel and I donnut like to go shoping"
    dictionary = load_dictionary('en_US-large.txt')
    spell_check(text, dictionary)



main()
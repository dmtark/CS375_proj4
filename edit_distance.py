from timeit import default_timer as timer
from time import perf_counter
import pprint

from improvements import Improvements


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


def multiple_trials():
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


def all_combinations():
    time_trial_info = []

    dict_files = [
        "en_US-large.txt",
        "cs375_word_set.txt",
        "mit_top_10000.txt",
        "rupert_top_1000.txt"
    ]

    pdf_name = "CS375f22_proj4_DynamicProgramming.pdf"

    for dict_file in dict_files:
        print(f"starting dict: {dict_file}")

        start = perf_counter()

        improvement = Improvements(pdf_name, dict_file)
        misspelled = improvement.spell_check_text()

        end = perf_counter()

        # add the time to a tuple
        time_diff = end - start
        num_misspelled = len(misspelled)

        time_trial_info.append(
            (time_diff, num_misspelled)
        )

    return time_trial_info


def print_combinations(combinations):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(combinations)





def main():
    # print("recursive")
    # print(find_edit_distance_recursive("bear", "brie"))
    # print(find_edit_distance_recursive("aaacolby", "colby"))
    # print(find_edit_distance_recursive("speaker", "speaks"))
    # print("iterative")
    # print(find_edit_distance_iterative("bear", "brie"))
    # print(find_edit_distance_iterative("aaacolby", "colby"))
    # print(find_edit_distance_iterative("speaker", "speaks"))

    data = multiple_trials()

    diff = [data[0][i] - data[1][i] for i in range(10)]

    print_combinations(diff)

    # combos = all_combinations()
    # print_combinations(combos)


if __name__ == "__main__":
    main()
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







def main():
    print("Recursive:")
    print(find_edit_distance_recursive("bear", "brie"))
    print("Iterative:")
    print(find_edit_distance_iterative("bear", "brie"))

    print(multiple_trials())



if __name__ == "__main__":
    main()
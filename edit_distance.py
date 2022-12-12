from timeit import default_timer as timer


def find_edit_distance_recursive(s: str, t: str) -> int:
    """Return the edit distance of one string to another."""


def find_edit_distance(S, T):
    s = len(S)
    t = len(T)
    result = [[0] * (t + 1) for _ in range(s + 1)]
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

def empirical_differences(S,T):
    '''Find empirical running time'''
    start_recursive = timer()
    recursive_num = find_edit_distance_recursive(S, T)
    end_recursive = timer()
    start_iter = timer()
    iter_num = find_edit_distance(S, T)
    end_iter = timer()
    # if recursive_num == iter_num:
    return (end_recursive - start_recursive), (end_iter - start_iter)
    # else:
        # return 0,0

def lots_of_em(dict): #dict is a dictionary of S,T words to mispell and find edit distance?
    start_recursive = timer()
    for word in dict.items():
        find_edit_distance_recursive(word[0],word[1])
    end_recursive = timer()

    start_iter = timer()
    for word in dict.items():
        find_edit_distance(word[0],word[1])
    end_iter = timer()

    return (end_recursive - start_recursive), (end_iter - start_iter)



def main():
    print(find_edit_distance("bear", "brie"))
    print(find_edit_distance("aaacolby", "colby"))
    print(find_edit_distance("speaker", "speaks"))


if __name__ == "__main__":
    main()
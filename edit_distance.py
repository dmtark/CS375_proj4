
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


def main():
    print("recursive")
    print(find_edit_distance_recursive("bear", "brie"))
    print(find_edit_distance_recursive("aaacolby", "colby"))
    print(find_edit_distance_recursive("speaker", "speaks"))
    print("iterative")
    print(find_edit_distance_iterative("bear", "brie"))
    print(find_edit_distance_iterative("aaacolby", "colby"))
    print(find_edit_distance_iterative("speaker", "speaks"))


if __name__ == "__main__":
    main()
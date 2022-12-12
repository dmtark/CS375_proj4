# creating 375 dictionary
from tika import parser # pip install tika

'''
load all 375 files
split them into words
create a set of all words --> that's our intial dictionary
some refinement... 
    take intersection of this set of all words with actual dictionary (SCOWL)
        --> that will spit out a list of potentially invalid words in our new dictionary
            --> if there's an error in another assignment (accidental typo) - you don't want to include that typo in our dictionary
            --> if there are issues with parser, exclude those

to keep:
- acronyms, etc - we want those in our 375 dictionary
'''

'''
ideas for data representation:
- false positives/false negatives?


'''


def parse_latex_file(filename):
    raw = parser.from_file(filename)
    raw_data = raw['content']
    words = re.find_all(r"[a-zA-Z\'\-]+", raw_data) # splitting words based off of this pattern
        # splits on everything that is not a letter, backslash, apostrophe or dash
        # this doesn't include numbers...
        # r makes this a raw string (\w is just treated like a character)
    return set(words) # do not want duplicates...
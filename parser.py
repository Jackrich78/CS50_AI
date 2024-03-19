import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | S NP
NP -> N | Det N | Det AdjP N | NP PP | Det N AdjP
VP -> V | V NP | V PP | V NP PP | Adv VP | VP Conj VP | V AdjP | V P NP
AdjP -> Adj | Adj AdjP | Adv
PP -> P NP
""" 

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Initialise a list
    processed_words = []

    # Use nltk's word_tokenize function
    preprocessed_words = nltk.word_tokenize(sentence)

    for word in preprocessed_words:
        # check if any character in word is alphabetic. 
        if any(char.isalpha() for char in word):
            # add word to list and make lower
            processed_words.append(word.lower())
            
    # return a list of lowercased words as strings
    return processed_words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # initialise list to store NP chunks
    np_chunks = []
    # iterate over all subtrees
    for subtree in tree.subtrees():
        # if 'NP' is found append to np_chunks
        if subtree.label() == 'NP':

            # check if subtree contains another NP subtree
            contains_other_np = any(child for child in subtree.subtrees(lambda t: t.label() == 'NP' and t != subtree))
            
            if not contains_other_np:
                np_chunks.append(subtree)

    return np_chunks


if __name__ == "__main__":
    main()

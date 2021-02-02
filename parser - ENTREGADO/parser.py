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
S -> NP VP | DP VP | S Conj S
DP -> Det NP
NP -> N | Adj NP | NP Conj NP | NP PP
VP -> V | V NP | V DP | VP PP | Adv VP | VP Conj VP | VP Adv | VP Adv PP
PP -> P NP | P DP
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
    # nltk.download('punkt')

    # return list with no punctuation
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    words = tokenizer.tokenize(sentence)

    # lower case
    words = list(map(lambda word: word.lower(), words))

    return words


def no_np_child(tree):
    for s in tree.subtrees(filter=lambda t: t.label() == "NP"):
        if s == tree:
            continue
        return False
    return True


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np = []

    subtrees = list(tree.subtrees(filter=lambda t: t.label() == "NP"))

    for s in subtrees:
        if no_np_child(s):
            np.append(s)

    return np


if __name__ == "__main__":
    main()

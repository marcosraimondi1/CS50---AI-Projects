import nltk
import sys
import os
import string
import numpy

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()

    for file in os.listdir(directory):
        with open(os.path.join(directory, file), encoding="utf8") as f:
            files[file] = f.read()

    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # nltk.download('stopwords')
    stopwords = nltk.corpus.stopwords.words("english")

    words = nltk.word_tokenize(document)

    words = list(filter(
        lambda w: w not in string.punctuation and w.lower() not in stopwords, words))

    words = list(map(lambda w: w.lower(), words))

    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()
    words = set()

    number_of_docs = len(documents)

    for doc in documents:
        for w in documents[doc]:
            words.add(w)

    for w in words:
        i = 0
        for doc in documents:
            if w in documents[doc]:
                i += 1
        idfs[w] = numpy.log((number_of_docs / i))

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    tfidf = dict()

    # initialize tf-idf values to 0 for each file
    for f in files:
        tfidf[f] = 0

    for w in query:
        for f in files:
            if w in files[f]:
                # update tf-idf values for each word from query that's in the file
                tf = files[f].count(w)
                tfidf[f] += (tf * idfs[w])

    def sort_key(e):
        return tfidf[e]

    # sort files given its tf-idf values
    topFiles = list(tfidf.keys())
    topFiles.sort(reverse=True, key=sort_key)
    # return the n top files
    return topFiles[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    sentenceRank = dict()

    for s in sentences:
        sentenceRank[s] = {
            "matchMesure": 0,
            "termDensity": 0
        }
        i = 0
        for w in query:
            if w in sentences[s]:
                i += 1
                sentenceRank[s]["matchMesure"] += idfs[w]
        sentenceRank[s]["termDensity"] = i/len(s)

    def sort_match(e):
        return sentenceRank[e]["matchMesure"]

    def sort_density(e):
        return sentenceRank[e]["termDensity"]

    # sort sentences given its “termDensity” first:
    # so if there's a tie in the match mesure,
    # higher term density is first in the list

    topSentences = list(sentenceRank.keys())
    topSentences.sort(reverse=True, key=sort_density)

    # sort sentences given its “matching word measure”
    topSentences.sort(reverse=True, key=sort_match)

    return topSentences[:n]


if __name__ == "__main__":
    main()

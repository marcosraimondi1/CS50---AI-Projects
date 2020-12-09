import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])

    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    suma = sum(list(ranks.values()))
    print("SUM: ", suma)
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    suma = sum(list(ranks.values()))
    print("SUM: ", suma)


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    distribution = {}
    N = len(corpus)
    rand_prob = (1 - damping_factor) / N

    links = corpus[page]

    if len(links) == 0:

        for pag in corpus:
            distribution[pag] = 1/N

        return distribution

    for pag in corpus:
        if pag not in links:
            distribution[pag] = rand_prob

    for link in links:
        distribution[link] = (damping_factor / len(links)) + rand_prob

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pageRank = {}

    samples = []
    page = random.choice(list(corpus.keys()))
    samples.append(page)

    for i in range(n):
        next_prob = transition_model(corpus, page, damping_factor)
        page = random.choices(list(next_prob.keys()),
                              list(next_prob.values()), k=1)[0]
        samples.append(page)

    N = len(samples)

    for pag in corpus:
        prob = samples.count(pag) / N
        pageRank[pag] = prob

    return pageRank


def equalDicts(dict1, dict2):

    for page in dict1:
        if abs((dict1[page] - dict2[page])) > 0.001:
            return False

    return True


def linksSum(page, pageRank, corpus):
    # sum(PR(i)/numLinks)

    summ = 0

    for i in corpus:
        if page in corpus[i] and page != i:
            summ += pageRank[i] / len(corpus[i])

    return summ


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pageRank = {}
    newPageRank = {}
    N = len(corpus)
    rand_prob = (1 - damping_factor) / N

    for page in corpus:
        pageRank[page] = 1/N
        newPageRank[page] = 1/N

    while True:
        for page in pageRank:
            newProb = rand_prob + \
                (damping_factor * linksSum(page, newPageRank, corpus))

            newPageRank[page] = newProb
        if equalDicts(pageRank, newPageRank):
            break
        else:
            pageRank = newPageRank

    return pageRank


if __name__ == "__main__":
    main()

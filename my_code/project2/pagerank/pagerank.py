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
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


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

"""
Examples:
Input form:
    corpus = {"1.html": {"2.html", "3.html"}, 
              "2.html": {"3.html"}, 
              "3.html": {"2.html"}}
Output form:
    Function `transition_model`, `sample_pagerank`, `iterate_pagerank`:
        return = {"1.html": 0.05,
                  "2.html": 0.475,
                  "3.html": 0.475}
"""

def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    result = dict()
    # If the page has no links, then just pick from all pages arbitrarily
    if len(corpus[page]) == 0:
        page_count = len(corpus)
        
        for k in corpus:
            result[k] = 1 / page_count
    
    # Else, pick page regarding damping factor
    else:
        # Firstly, calculate possibility without damping factor
        page_count = len(corpus)
        
        for k in corpus:
            result[k] = (1 - damping_factor) / page_count
        
        # Secondly, add possibility with damping factor
        links = corpus[page]
        link_count = len(links)
        
        for link in links:
            result[link] += damping_factor / link_count
    
    return result
  
    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Construct a dict for recording how many times a certain page has been browsed
    record = dict()
    
    # Construct a dict of possibility of first pick
    poss = dict()
    
    page_count = len(corpus)
    for k in corpus:
        # Possibility of first pick
        poss[k] = 1 / page_count
        
        # Initialize record
        record[k] = 0
    
    # Arbitrarily pick one page to start
    start = random_pick(poss)
    record[start] += 1
    
    # Loop n-1 times for sampling
    for i in range(n - 1):
        poss = transition_model(corpus, start, damping_factor)
        start = random_pick(poss)
        record[start] += 1
        
    # Construct rank
    rank = dict()
    for k, v in record.items():
        rank[k] = v / n
    
    return rank
    
    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Deal with problem that a page has no links
    allPages = set(corpus.keys())
    
    for page in corpus:
        if len(corpus[page]) == 0:
            corpus[page] = allPages
    
    # Parse pages' father page
    fatherPages = corpus.copy()
    for k in fatherPages:
        fatherPages[k] = set()
    
    for k in corpus:
        for link in corpus[k]:
            fatherPages[link].add(k)
    
    # Initialize rank
    rank = dict()
    page_count = len(corpus)
    
    for k in corpus:
        rank[k] = 1 / page_count
    
    # Iterate rank until their change is less then 0.001
    ACCURACY = 0.001
    flag = True
    
    while(flag):
        flag = False
        oldRank = rank.copy()
        
        for k in oldRank:
            # Calculate sum of (PR(i) / NumLinks(i))
            tempSum = 0
            for fatherPage in fatherPages[k]:
                tempSum += oldRank[fatherPage] / len(corpus[fatherPage])
            
            # Calculate PR(p)
            rank[k] = (1 - damping_factor) / page_count + damping_factor * tempSum
                    
            # See if PR changes more than 0.001, if YES, then loop
            if abs(rank[k] - oldRank[k]) > ACCURACY:
                flag = True
    
    return rank
    
    raise NotImplementedError

def random_pick(possibility_dict):
    # Construct a list consist of tuple of (keyname, pstart, pend) for random pick
    possibility_list = list()
    p = 0
    for k, v in possibility_dict.items():
        possibility_list.append((k, p, p+v))
        p += v

    # Produce a number ranging in [0, 1)    
    random.seed()
    num = random.random()
    
    # See which range the num falls in
    for i in range(len(possibility_list)):
        if num >= possibility_list[i][1] and num < possibility_list[i][2]:
            return possibility_list[i][0]
    
"""def test():
    dict1 = {"a": [1], "b": [2], "c": [3]}
    dict2 = dict1.copy()
    
    dict2["a"][0] = 2
    
    print(f"dict1: {dict1}")
    print(f"dict2: {dict2}")
"""
if __name__ == "__main__":
    main()

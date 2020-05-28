import os
import random
import re
import sys
import math

# damping factor
DAMPING = 0.85
SAMPLES = 10000


def main():
    #expects the name of the directory
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    # corpus has a dictionary (hash table)
    # key is a html file
    # value is all the html files it links to
    corpus = crawl(sys.argv[1])
    #return a dictionary
    # keys: page_name, values: page_rank
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
            #utilize regex to get all the links
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
    transition = dict()
    if len(corpus[page]) == 0:
        #every page including itself have an equal probability
        probability = 1 / len(corpus)
        for html_page in corpus:
            transition[html_page] = probability
    else:
        #two parts to this
        #first we deal with the outgoing link
        # probabilty of d
        #fill corpus with zeros
        for html_page in corpus:
            transition[html_page] = 0
        # deal with outgoing links
        link_prob = damping_factor / len(corpus[page])
        #accounted for the outgoing link
        for link in corpus[page]:
            transition[link] += link_prob
        #now we deal with a random page being selected
        #including current page
        page_prob = (1 - damping_factor) / len(corpus)
        for html_page in corpus:
            transition[html_page] += page_prob

    
    return transition

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    distribution = dict()
    #initialize the occurrence of every page to 0
    for page in corpus:
        distribution[page] = 0

    #get a list of all keys in th corpus
    all_keys = corpus.keys()
    # print(f"Length: {len(corpus)}")
    #print(f"corpus: {corpus}")
    #randomly generate a page to start with
    random_index = random.randint(0, len(all_keys) - 1)
    count = 0
    for key in all_keys:
        if count == random_index:
            page = key
            break
        count += 1
    
    distribution[page] += 1
    #print(f"distribution: {distribution}")

    for i in range(n):
        #print(f"Page: {page}")
        transition = transition_model(corpus, page ,damping_factor)
        #print(f"transition: {transition}")
        page = get_next_page(transition)
        #print(f"highest_page_prob: {page}")
        distribution[page] += 1

    #normalize our distribution
    for element in distribution:
        distribution[element] = distribution[element] / n

    return distribution

def get_next_page(transition):
    highest = -1
    highest_page = [] 

    for state in transition:
        highest_page += [state]*math.ceil(100* transition[state]) 

    #print(highest_page)
    return random.choice(highest_page)

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #print(f"corpus: {corpus}")
    distribution = dict()
    previous_links = get_links_to_page(corpus)
    #print(f"previous_links: {previous_links}")

    N = len(corpus)
    #initialize the distribution to 1/N
    for page in corpus:
        distribution[page] = 1 / N

    done = False
    while not done:
        old_distribution = distribution.copy()
        for page in corpus:
            new_rank = (1 - damping_factor) / N
            old_page_rank = 0
            linkers = previous_links[page]
            for link in linkers:
                old_page_rank += old_distribution[link]/len(corpus[link])

            distribution[page] = new_rank + damping_factor * old_page_rank
        #now compare to check if difference is less than 0.001
        donzo = True
        for page in old_distribution:
            if abs(old_distribution[page] - distribution[page]) > 0.001:
                donzo = False
                break
        
        if(donzo):
            done = True

    return distribution


def get_links_to_page(corpus):
    previous_links = dict()

    for page in corpus:
        previous_links[page] = set()

    # for page in corpus:
        # for interior in corpus[page]:
    for page in corpus.keys():
        #print("Page: "+page)
        for p in corpus:
            #print("P: "+ p)
            #print(f"Corpus[p]: {corpus[p]}")
            if page in corpus[p]:
                #print("True")
                previous_links[page].add(p)

    return previous_links



if __name__ == "__main__":
    main()

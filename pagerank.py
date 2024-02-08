import os
import random
import re
import sys
import math

DAMPING = 0.855
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


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    N = len(corpus)

    # initialise the probably distribution with equal probability for each page
    prob_dist = {page: (1 - damping_factor) / N for page in corpus}

    # get links from current page 
    links = corpus[page]

    if links:
        # calculate probability for links on current page
        linked_prob = damping_factor / len(links)
        for link in links:
            prob_dist[link] += linked_prob
    
    else:
        # pages with no outgoing links
        for page in corpus:
            prob_dist[page] += damping_factor / N

    # check probability distribution sums to 1
        total_probability = sum(prob_dist.values())
        if not math.isclose(total_probability, 1.0, abs_tol=0.001):
            raise ValueError(f"Total probability is off by {1.0 - total_probability:.3f}")
    return prob_dist


"""
# Manual tests
corpus = {
    "1.html": {"2.html", "3.html"},
    "2.html": {"3.html"},
    "3.html": {"2.html"}
}

damping_factor = 0.85
current_page = "1.html"
"""
# test transition model in isolation
# transition_probs = transition_model(corpus, current_page, damping_factor)


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # pagerank dictionary 
    pagerank = {}
    n = SAMPLES

    # intialise pagerank for each page
    for page in corpus:
        pagerank[page] = 0

    # intialise current page to None
    current_page = None

    # loop through each sample
    for i in range(1, n + 1):
        # choose random page to start
        if i == 1:
            current_page = random.choice(list(corpus.keys()))
        else:
            # get transition probabilities for each page
            transition_probabilities = transition_model(corpus, current_page, damping_factor)

            # generate a random number
            random_number = random.random()

            running_total = 0

            # loop through transition probabilities
            for page, probability in transition_probabilities.items(): # use .items to get both keys and values
                running_total += probability

                # heck if random number is less than running total
                if random_number <= running_total:
                    # update current page
                    current_page = page
                    break
        # increment count of visits for the current page
        pagerank[current_page] += 1

    # convert to proportions
    for page, count in pagerank.items():
        pagerank[page] = count / n 

    return pagerank
    
# test sample_pagerank in isolation
# sampled_pagerank = sample_pagerank(corpus, damping_factor, SAMPLES)

# print(f"Sampled pagerank values with {SAMPLES} samples:")
# for page, rank in sampled_pagerank.items():
#    print(f"{page}: {rank}")


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    pagerank = {}  # dictionary for the pagerank of each page

    # intialise pagerank
    for page in corpus:
        pagerank[page] = 1 / N

    # intialise change variable to track change between iterations
    change = 1

    # recursively update pagerank
    while change > 0.001:  # threshold for when pageranks have converged
        new_pagerank = {}  # temp dictionary
        change = 0  # reset change 

        for page in pagerank:
            sum = 0  # initialise sum to 0 for pages linking together

            # calculate sum based on pagerank formula
            for page_links in corpus.keys():
                # pages with no links
                if not corpus[page_links]:
                    sum += pagerank[page_links] / N
                # if there is a page link add to pagerank
                elif page in corpus[page_links]:
                    sum += pagerank[page_links] / len(corpus[page_links])

            # update pagerank for current page
            new_rank = (1 - damping_factor) / N + damping_factor * sum
            new_pagerank[page] = new_rank

            # track max change in pagerank value
            current_change = abs(new_pagerank[page] - pagerank[page])
            if current_change > change:
                change = current_change
        
        # update pageranks for next iteration
        pagerank = new_pagerank.copy()

    return pagerank
 
# test iterate_pagerank in isolation
# iterated_pagerank = iterate_pagerank(corpus, damping_factor)

# print("Iterated pagerank values:")
# for page, rank in iterated_pagerank.items():
#     print(f"{page}: {rank}")


if __name__ == "__main__":
    main()

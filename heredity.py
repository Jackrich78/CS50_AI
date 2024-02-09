import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}

                
def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    joint_prob = 1 

    for person in people:
        # calculate how many genes the person has
        if person in one_gene:
            gene_count = 1
        elif person in two_genes:
            gene_count = 2
        else:
            gene_count = 0
    
        # check if person has the trait
        trait = person in have_trait

        # if parents are known calc prob based on parents gene count
        mother = people[person]["mother"]
        father = people[person]["father"]

        
        # if both parents exist
        if mother and father:
            #reset parent probabilities
            prob_from_parents = {parent: 0 for parent in [mother, father]}

            for parent in [mother, father]:
                parent_gene_count = (
                    2 if parent in two_genes else
                    1 if parent in one_gene else
                    0 
                )

                # calculate gene probability inherited from parents
                if parent_gene_count == 2:
                    prob_from_parents[parent] = 1 - PROBS["mutation"]  # inherites and doens't mutate 
                elif parent_gene_count == 1:
                    prob_from_parents[parent] += 0.5 * (1 - PROBS["mutation"])  # inherits and doesn't mutate
                    prob_from_parents[parent] += 0.5 * PROBS["mutation"]  # inherits safe gene but mutates
                else:
                    prob_from_parents[parent] = PROBS["mutation"]  # only prob that a safe gene could mutate

            # calculate probability based on parents
            if gene_count == 2:
                gene_prob = prob_from_parents[mother] * prob_from_parents[father]
            elif gene_count == 1:
                gene_prob = prob_from_parents[mother] * (1 - prob_from_parents[father]) + (1 - prob_from_parents[mother]) * prob_from_parents[father]
            else:
                gene_prob = (1 - prob_from_parents[mother]) * (1 - prob_from_parents[father])
        else:
            # if no parents in database
            gene_prob = PROBS["gene"][gene_count]
        
        # calculate probability of trait
        trait_prob = PROBS["trait"][gene_count][trait]

        # joint probability 
        joint_prob *= gene_prob * trait_prob

    return joint_prob

"""
# example test
people = {
  'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
  'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
  'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
}

# Assume these sets based on the scenario
one_gene = {"Harry"}
two_genes = {"James"} 
have_trait = {"James"}


result = joint_probability(people, one_gene, two_genes, have_trait)
print(f"Joint Probability: {result}")
"""


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # update each persons probabilities
    for person in probabilities:
        # check how many genes person has
        if person in two_genes:
            probabilities[person]["gene"][2] += p
        elif person in one_gene:
            probabilities[person]["gene"][1] += p
        else:
            probabilities[person]["gene"][0] += p

        # update if person has the trait
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p



def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        # normalise gene probability for each person
        # calc total sum of gene probabilities
        gene_total = sum(probabilities[person]["gene"].values())
        for gene_count in probabilities[person]["gene"]:
            if gene_total > 0:  # avoid dividing by zero
                # divid each gene prob by the gene total to sum to 1
                probabilities[person]["gene"][gene_count] /= gene_total

        # normalise trait probability
        # calc total sum of trait probabilities
        trait_total = sum(probabilities[person]["trait"].values())
        for trait_status in probabilities[person]["trait"]:
            if trait_total > 0:  # avoid dividing by zero
                # divide each trait prob by the total to sum to 1
                probabilities[person]["trait"][trait_status] /= trait_total
                        

if __name__ == "__main__":
    main()

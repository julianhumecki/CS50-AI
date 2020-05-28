import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having this gene
    # if we don't know anything about this person's parents
    # genes, then we use this unconditional probabilitiy
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },
    #conditional probabilities of you exhibiting the trait (of say hearing impairment)
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

    #map each person's name to a dictionary with info
    #about them including: their name, their mom and dad (if listed), and their trait
    # trait: yes, no, dont know
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        #create a copy of person for each entry in people
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
    #anyone not in one gene, or two genes, what are the odds
    #they have zero copies
    #anyone not in have_trait
    #get the odds of them not having the trait
    joint_probs = 1
    # print()
    # print(f"One gene {one_gene}")
    # print(f"Two gene {two_genes}")
    # print(f"Traits: {have_trait}")
    # print()

    for person in people:
        #get appropriate gene count
        gene_count = get_gene_count(person, one_gene, two_genes)
        #get the right trait value
        trait_value = None
        if person in have_trait:
            trait_value = True
        else:
            trait_value = False

        value = 0
        # print(f"Person: {person}")
        # print(f"Gene count {gene_count}")
        # print(f"trait_value: {trait_value}")
        # get the joint probability of person having gene_count genes
        # and having a trait_value of the trait
        if people[person]["mother"] == None and people[person]["father"] == None:
            #the joint probability is the probability of
            #the person having n genes * the probability of having the trait given you know you have n genes
            
            value = PROBS["gene"][gene_count] * PROBS["trait"][gene_count][trait_value]
            #print(f"Value math: {value}")
        #here you need to consider the data of your parents (assume both parents are known)
        # parents genes influence your genes
        # how can the child get n gene_count
        # need to check the parents
        # if the parents both have the trait
        # elif one parent has the trait
        # else none have it
        else: 
            mother_gene_count = get_gene_count(people[person]["mother"], one_gene, two_genes)
            father_gene_count = get_gene_count(people[person]["father"], one_gene, two_genes)

            #if gene_count = 0 then
            #both mother and father have the genes (both undergo mutations) or
            #mother has gene, father doesnt, mother gene undergoes mutation and the father's doesnt or
            #father has gene, mother doesnt, father gene mutates and mother's doesnt or
            #both dont have the gene and neither (undergo a mutation) 

            if gene_count == 0:
                if mother_gene_count == 0 and father_gene_count == 0:
                    #1 option:
                    # don't get it from either
                    #does not get the gene from the father and does not get the gene from the mother (no mutations)
                    # (mom) won't get passed on and wont mutate, (dad) won't get passed on and wont mutate
                    # FFFF
                    value = 1 * (0.99) * 1 * (0.99)
                #inheiting from mother and/or father are independent variables
                elif (mother_gene_count == 1 and father_gene_count == 0) or (mother_gene_count == 0 and father_gene_count == 1):
                    #options:
                    # dont get it from the mother and you dont get it from the father

                    # the mother doesn't pass the gene and there's no mutation and father doesn't pass the gene
                    # the mother passes the gene, it mutates and father doesn't pass the gene
                    # FFFF | TTFF
                    value = 0.50 * 0.99 * 1 * (0.99) + 0.50 * 0.01 * 1 * 0.99

                elif mother_gene_count == 1 and father_gene_count == 1:
                    # the mother doesn't pass the gene and there's no mutation and father doesn't pass the gene and there's no mut
                    # the mother doesn;t pass the gene and no mutation; father pass gene and mutate
                    # the mother passes the gene, it mutates and father doesn't pass the gene and no mut
                    # the mother pass gene, it mutates and father pass the gene and mut
                    # FFFF | FFTT | TTFF | TTTT
                    value = 0.50 * 0.99 * 0.50 * (0.99) + 0.50 * 0.99 * 0.5 * 0.01 + 0.5 * 0.01 * 0.5 * 0.99 + 0.5 * 0.01 * 0.5 * 0.01
                elif (mother_gene_count == 2 and father_gene_count == 0) or (mother_gene_count == 0 and father_gene_count == 2):
                    #mother passes and mutates and father doesn't pass, no mut
                    # TTFF
                    value = 1 * 0.01 * 1 * 0.99
                    # mother doesn't pass no mut, father passes with mut

                elif (mother_gene_count == 2 and father_gene_count == 1) or (mother_gene_count == 1 and father_gene_count == 2):
                    #mother pass and mut, father doesnt pass no mut
                    #mother pass and mut, father pass, mut
                    # TTFF | TTTT
                    value = 1 * 0.01 * 0.5 * 0.99 + 1 * 0.01 * 0.5 * 0.01 

                elif mother_gene_count == 2 and father_gene_count == 2:      
                    #mother pass and mut, faather pass and mut
                    # TTTT
                    value = 1 * 0.01 * 1 * 0.01
            
            elif gene_count == 1:

                if mother_gene_count == 0 and father_gene_count == 0:
                    #mother no pass, mut, father no pass, no mut
                    #mother no pass, no mut, father no pass, mut
                    # FFFT | FTFF
                    value = 1 * 0.01 * 1* 0.99 + 1 * 0.99 * 1 * 0.01
                elif (mother_gene_count == 1 and father_gene_count == 0) or (mother_gene_count == 0 and father_gene_count == 1):
                    #mother pass, no mut, father no pass. no mut
                    #mother no pass, no mut, father no pass, mut
                    #mother pass, mut, father no pass, mut
                    # FFFT | FTFF | TFFF | TTFT
                    value = 0.5*0.99*1*0.01 + 0.5*0.01*1*0.99 + 0.5*0.99*1*0.99 + 0.5*0.01*1*0.01
        
                elif mother_gene_count == 1 and father_gene_count == 1:
                    #mother no pass, no mut, father no pass, mut
                    #mother no pass, no mut, father pass, no mut
                    #mother pass, no mut, father no pass, no mut 
                    #mother pass, mut, father no pass, mut
                    #mother pass, mut, father pass, mut
                    # FFFT | FFTF | FTFF | FTTT | 
                    # TFFF | TFTT | TTFT | TTTF
                    value = 0.5*0.99*0.5*0.01 + 0.5*0.99*0.5*0.99 + 0.5*0.01*0.5*0.99 + 0.5*0.01*0.5*0.01 + 0.5*0.99*0.5*0.99 + 0.5*0.99*0.5*0.01 + 0.5*0.01*0.5*0.01 + 0.5*0.01*0.5*0.99
                elif (mother_gene_count == 2 and father_gene_count == 0) or (mother_gene_count == 0 and father_gene_count == 2):
                    
                    # TFFF | TTFT
                    value = 1 * 0.99 * 1 * 0.99 + 1 * 0.01 * 1 * 0.01 
                    
                elif (mother_gene_count == 2 and father_gene_count == 1) or (mother_gene_count == 1 and father_gene_count == 2):
                    
                    # TFFF | TFTT | TTFT | TTTF 
                    value = 1 * 0.99 * 0.5 * 0.99 + 1 * 0.99 * 0.5 * 0.01 + 1 * 0.01 * 0.5 * 0.01 + 1 * 0.01 * 0.5 * 0.99 

                elif mother_gene_count == 2 and father_gene_count == 2:      
                    #mother pass and mut, father pass and mut
                    # TFTT | TTTF
                    value = 1 * 0.99 * 1 * 0.01 + 1 * 0.01 * 1 * 0.99

            elif gene_count == 2:
                if mother_gene_count == 0 and father_gene_count == 0:
                    #mother no pass, mut, father no pass, no mut
                    #mother no pass, no mut, father no pass, mut
                    # FTFT
                    value = 1 * 0.01 * 1* 0.01
                elif (mother_gene_count == 1 and father_gene_count == 0) or (mother_gene_count == 0 and father_gene_count == 1):
                    #mother pass, no mut, father no pass. no mut
                    #mother no pass, no mut, father no pass, mut
                    #mother pass, mut, father no pass, mut
                    # FTFT | TFFT 
                    value = 0.5*0.01*1*0.01 + 0.5*0.99*1*0.01
        
                elif mother_gene_count == 1 and father_gene_count == 1:
                    #mother no pass, no mut, father no pass, mut
                    #mother no pass, no mut, father pass, no mut
                    #mother pass, no mut, father no pass, no mut 
                    #mother pass, mut, father no pass, mut
                    #mother pass, mut, father pass, mut
                    # FTFT | FTTF | TFFT | TFTF 
                    
                    value = 0.5*0.01*0.5*0.01 + 0.5*0.01*0.5*0.99 + 0.5*0.99*0.5*0.01 + 0.5*0.99*0.5*0.99 
                        
                elif (mother_gene_count == 2 and father_gene_count == 0) or (mother_gene_count == 0 and father_gene_count == 2):
                    
                    # TFFT
                    value = 1 * 0.99 * 1 * 0.01  
                    
                elif (mother_gene_count == 2 and father_gene_count == 1) or (mother_gene_count == 1 and father_gene_count == 2):
                    
                    # TFFT | TFTF
                    value = 1*0.99*0.5*0.01 + 1*0.99*0.5*0.99 

                elif mother_gene_count == 2 and father_gene_count == 2:      
                    #mother pass and no mut, father pass and no mut
                    # TFTF
                    value = 1 * 0.99 * 1 * 0.99

            #print(f"Value math: {value}")
            value = value * PROBS["trait"][gene_count][trait_value]
            #print(f"Total: {value}")

        #combine the probabilities    
        joint_probs = joint_probs * value
        #print(f"Joint probs: {joint_probs}")

    #print(f"Final Probs: {joint_probs}")
    return joint_probs

                


def get_gene_count(person, one_gene, two_genes):
    gene_count = -1
    if person in one_gene:
        gene_count = 1
    elif person in two_genes:
        gene_count = 2
    #no genes
    else:
        gene_count = 0
    return gene_count

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        gene_count = get_gene_count(person, one_gene, two_genes)
        trait_value = None
        if person in have_trait:
            trait_value = True
        else:
            trait_value = False

        probabilities[person]["gene"][gene_count] += p 
        probabilities[person]["trait"][trait_value] += p

    return


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    
    for person in probabilities:

        sum = 0
        #normalize the genes
        
        sum = probabilities[person]["gene"][0] + probabilities[person]["gene"][1] + probabilities[person]["gene"][2]
            
        multiple = 1/sum
        
        probabilities[person]["gene"][0] = probabilities[person]["gene"][0] * multiple
        probabilities[person]["gene"][1] = probabilities[person]["gene"][1] * multiple
        probabilities[person]["gene"][2] = probabilities[person]["gene"][2] * multiple

        #normalize the traits
        sum = probabilities[person]["trait"][True] + probabilities[person]["trait"][False]
        multiple = 1/sum 
        probabilities[person]["trait"][True] = probabilities[person]["trait"][True]*multiple
        probabilities[person]["trait"][False] = probabilities[person]["trait"][False]*multiple

    return


        


if __name__ == "__main__":
    main()

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
    
    result_p = 1
    conditions = dict()
    # Loop to collect conditions that is set in the question
    for person in people:
        if person in one_gene:
            gene_count = 1
        elif person in two_genes:
            gene_count = 2
        else:
            gene_count = 0
            
        if person in have_trait:
            trait = True
        else:
            trait = False
            
        conditions[person] = {"gene_count": gene_count, "trait": trait}
    
    # Loop to calculate probabilities of all persons and multiply them to get joint probability
    for person in people:
        temp_p = 1
        
        gene_count = conditions[person]["gene_count"]
        trait = conditions[person]["trait"]
        
        # Firstly, calculate the probability of gene
            # For persons without data of parents, just calculate the gene probability using the unconditional data
        if people[person]["mother"] == None:
            temp_p *= PROBS["gene"][gene_count]

            # For persons with data of parent, consider how many genes his parents have, and then calculate the probability
            # that his parents inherit a certain number of genes to him
        else:
            father = people[person]["father"]
            mother = people[person]["mother"]
            father_gene_count = conditions[father]["gene_count"]
            mother_gene_count = conditions[mother]["gene_count"]  
            
            temp_p *= cal_inherit_prob(gene_count, father_gene_count, mother_gene_count)
        
        # Secondly, calculate the probability that the person behave the trait given the number of gene is known
        temp_p *= PROBS["trait"][gene_count][trait]
        
        # Finally, multiply the probability to calculate joint probability
        result_p *= temp_p
        
    return result_p
    raise NotImplementedError


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    
    conditions = dict()
    # Loop to collect conditions that is set in the question
    for person in probabilities:
        if person in one_gene:
            gene_count = 1
        elif person in two_genes:
            gene_count = 2
        else:
            gene_count = 0
            
        if person in have_trait:
            trait = True
        else:
            trait = False
    
        conditions[person] = {"gene_count": gene_count, "trait": trait}
    
    # Add p to probability respectively
    for person in conditions:
        gene_count = conditions[person]["gene_count"]
        trait = conditions[person]["trait"]
        
        probabilities[person]["gene"][gene_count] += p
        probabilities[person]["trait"][trait] += p
    
    return
    raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    
    # Loop to normalize probabilities of gene and trait of each person
    for property in probabilities.values():
        # Loop over "gene" and "trait"
        for property_data in property.values():
            # Sum up the current probability
            cur_sum_p = 0
            for v in property_data.values():
                cur_sum_p += v
            
            # Calculate the coefficient -- alpha
            alpha = 1 / cur_sum_p
            
            # Normalize the probabilities with alpha
            for k in property_data.keys():
                property_data[k] *= alpha

    return                
    raise NotImplementedError


def cal_inherit_prob(inherit, father, mother):
    """
    Calculate the probability of the number of genes inherited is `inherit`,
    given the number of genes of father is `father`, 
    and the number of genes of mother is `mother`
    """
    parents = {"father": father, "mother": mother}
    parent_inherit_p = dict()
    
    # Calculate the probability that a parent inherits the gene to the child
    for parent in parents:
        temp_p = 1
        match parents[parent]:
            case 0:
                temp_p = PROBS["mutation"]
            case 1:
                temp_p = 0.5*(1-PROBS["mutation"]) + 0.5*PROBS["mutation"]
            case 2:
                temp_p = 1 - PROBS["mutation"]
        
        parent_inherit_p[parent] = temp_p
    
    # Calculate the probability that both parents inherit certain number of genes to the child
    match inherit:
        case 0:
            result_p = (1 - parent_inherit_p["father"]) * (1 - parent_inherit_p["mother"])
        case 1:
            result_p = (
                (1 - parent_inherit_p["father"]) * parent_inherit_p["mother"] +
                (1 - parent_inherit_p["mother"]) * parent_inherit_p["father"]
                        )
        case 2:
            result_p = parent_inherit_p["father"] * parent_inherit_p["mother"]
    
    return result_p

if __name__ == "__main__":
    main()

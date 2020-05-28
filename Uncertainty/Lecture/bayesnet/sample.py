import pomegranate

from collections import Counter

from model import model

def generate_sample():

    # Mapping of random variable name to sample generated
    sample = {}

    # Mapping of distribution to sample generated
    parents = {}

    # Loop over all states, assuming topological order
    # some vertex u comes before vertex v given the edge goes from u to v
    for state in model.states:

        # If we have a non-root node, sample conditional on parents
        # if it is a conditional distribution, sample based on the parent's value
        # state.distribution is the probability distribution
        if isinstance(state.distribution, pomegranate.ConditionalProbabilityTable):
            #prior, you defined, which state is dependent upon which parents
            # so when you pass in the all the parents to this sample, it filters out
            # the irrelevant ones, and generates a sample based on the conditional requirements of the
            # parent 
            sample[state.name] = state.distribution.sample(parent_values=parents)

        # Otherwise, just sample from the distribution alone
        # not conditional, so it's unconditional, sample directly from the 
        # probability distribution
        else:
            sample[state.name] = state.distribution.sample()

        # Keep track of the sampled value in the parents mapping
        parents[state.distribution] = sample[state.name]

    # Return generated sample
    return sample

# Rejection sampling
# Compute distribution of Appointment given that train is delayed
# number of samples
N = 10000
#in rejection sampling, you only consider cases where the train was delayed  
#so it matches our conditional check (of our train being delayed) 
data = []
for i in range(N):
    sample = generate_sample()
    #of the samples generated
    #if the train was delayed, the condition is met
    #and from there, we get the value of our random
    #variable appointment and add it to our list
    if sample["train"] == "delayed":
        data.append(sample["appointment"])

#counts how many times our appointment was made
#and how many times it was missed
print(Counter(data))


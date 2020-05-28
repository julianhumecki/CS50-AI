from pomegranate import *

# Define starting probabilities
# every markov model begins at some point in time
# so I need to give it some starting distribution
start = DiscreteDistribution({
    "sun": 0.5,
    "rain": 0.5
})

# Define transition model
# how to transition from one day to the next
transitions = ConditionalProbabilityTable([
    ["sun", "sun", 0.8],
    ["sun", "rain", 0.2],
    ["rain", "sun", 0.3],
    ["rain", "rain", 0.7]
], [start])

# Create Markov chain
model = MarkovChain([start, transitions])

# Sample 50 states from chain
# sample 50 days worth of weather
print(model.sample(50))

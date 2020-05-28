#importing the bayesian network
from model import model

# Calculate probability for a given observation

# Calculate the joint probability of a 
# particular scenario happening
probability = model.probability([["none", "no", "on time", "attend"]])
probability_miss = model.probability([["none", "no", "on time", "miss"]]) 
print(probability)
print(f"Missed: {probability_miss}")

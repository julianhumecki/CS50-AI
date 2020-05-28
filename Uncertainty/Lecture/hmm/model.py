from pomegranate import *

# Observation model for each state
# define the model for when it's sunny
# based on the sensor model
sun = DiscreteDistribution({
    "umbrella": 0.2,
    "no umbrella": 0.8
})

#define the model for when it's rainy
# based on the sensor model
rain = DiscreteDistribution({
    "umbrella": 0.9,
    "no umbrella": 0.1
})

states = [sun, rain]

# Transition model
# define how you change from one state to the next
transitions = numpy.array(
    [[0.8, 0.2], # Tomorrow's predictions if today = sun
     [0.3, 0.7]] # Tomorrow's predictions if today = rain
)

# Starting probabilities (base point)
starts = numpy.array([0.5, 0.5])

# Create the model
model = HiddenMarkovModel.from_matrix(
    transitions, states, starts,
    state_names=["sun", "rain"]
)
model.bake()

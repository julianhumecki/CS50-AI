from model import model

# Observed data
observations = [
    "umbrella",
    "umbrella",
    "no umbrella",
    "umbrella",
    "umbrella",
    "umbrella",
    "umbrella",
    "no umbrella",
    "no umbrella"
]

# Predict underlying states for each day of the sequence
predictions = model.predict(observations)
for prediction in predictions:
    print(model.states[prediction].name)

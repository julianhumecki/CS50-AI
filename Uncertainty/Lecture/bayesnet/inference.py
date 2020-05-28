#import the bayesian model
from model import model

# Calculate predictions
# pass in the evidence that you have observed
# tells us what we can infer about the hidden variables

# make the predictions, then you can look up the result
# you want to know the probability of 
predictions = model.predict_proba({
	"rain": "heavy",
    "train": "delayed"
})

# Print predictions for each node
# zip is a list of stuff you can iterate over
for node, prediction in zip(model.states, predictions):
    if isinstance(prediction, str):
       #known information
       print(f"{node.name}: {prediction}")
    else:
    	#inferences
        print(f"{node.name}")
        for value, probability in prediction.parameters[0].items():
            print(f"    {value}: {probability:.4f}")

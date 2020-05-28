import csv
import random

#import bunch of resources from scikit learn
from sklearn import svm
from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

#set to the appropriate learning model
#Perceptron Model: figure out some of the weights
#that divides our data into 2 different groups
#model = Perceptron()

#Use the Support Vector Machine Model
#model = svm.SVC()
# Use the K-Nearest-Neighbour Model; specify the number of neighbours you want to look at
model = KNeighborsClassifier(n_neighbors=3)
# model = GaussianNB()

# Read data in from file
with open("banknotes.csv") as f:
    reader = csv.reader(f)
    next(reader)

    data = []
    for row in reader:
        data.append({
            #read the first four columsn as evidence
            "evidence": [float(cell) for cell in row[:4]],
            #read the last column of each row to determine
            #if bill is real or fake
            "label": "Authentic" if row[4] == "0" else "Counterfeit"
        })

#next we want to split up our data into a training set 
#and a testing set so we can see how well our model responds
#to unknown data

# Separate data into training and testing groups

#holdout is how much data we are gonna hold out for our
#TESTING phase
holdout = int(0.50 * len(data))
#results are usually different each time since the data is getting RANDOMLY shuffled
random.shuffle(data)
#our testing data will be all our data upto the holdout
testing = data[:holdout]
#our trainign data will be the remainder of it
training = data[holdout:]

# Train model on training set

# Next we need to split up our training set 
# into inputs and outputs
# inputs being our evidence (X_training)
# outputs being our label (counterfeit vs not) (Y_training) 

X_training = [row["evidence"] for row in training]
y_training = [row["label"] for row in training]
#train our model
model.fit(X_training, y_training)

#Once this model has been trained,
#we can test to see how well it performed on our
#testing set

# Make predictions on the testing set
# split up our testing data into two sets
# inputs - evidence (X_testing)
# outputs - label (y_testing)
X_testing = [row["evidence"] for row in testing]
y_testing = [row["label"] for row in testing]
#predict based on our model the labels
predictions = model.predict(X_testing)

# Compute how well we performed

#goal is now to compare out predictions with 
#testing data set's results
correct = 0
incorrect = 0
total = 0
#zip allows us to look through 2 different lists
#at the same time, so we can simulatenously compare
#our predictions with our results
for actual, predicted in zip(y_testing, predictions):
    total += 1
    if actual == predicted:
        correct += 1
    else:
        incorrect += 1

# Print results
print(f"Results for model {type(model).__name__}")
print(f"Correct: {correct}")
print(f"Incorrect: {incorrect}")
print(f"Accuracy: {100 * correct / total:.2f}%")

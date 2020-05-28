import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


MONTHS = {
    "Jan":0,
    "Feb":1,
    "Mar":2,
    "Apr":3,
    "May":4,
    "June":5,
    "Jul":6,
    "Aug":7,
    "Sep":8,
    "Oct":9,
    "Nov":10,
    "Dec":11
}
def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    #print(evidence[0])
    #print(labels[277])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )
    #print(len(X_train))
    #print(len(y_train))
    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = list()
    labels = list()
    with open(filename) as f:
        reader = csv.reader(f)
        #skip the titles
        next(reader)
        for row in reader:
            sub_evidence = list()
            count = 0
            for element in row:
                if not count == 17:
                    if count == 0 or count == 2 or count == 4 or count == 11 or count == 12 or count == 13 or count == 14:
                        sub_evidence.append(int(element))
                    elif count == 10:
                        sub_evidence.append(MONTHS[element])
                    elif count == 15:
                        value = -1
                        
                        if element == "Returning_Visitor":
                            value = 1
                        else:
                            value = 0
                        sub_evidence.append(value)
                    elif count == 16:
                        value = -1
                        #print(element)
                        if element == "TRUE":
                            value = 1
                        else:
                            value = 0
                        sub_evidence.append(value)

                    else:
                        sub_evidence.append(float(element))
                count = count + 1
            #evidence.append([cell for cell in row[:17]])
            #add the label
            evidence.append(sub_evidence)
            labelling = -1
            if element == "TRUE":
                labelling = 1
            else:
                labelling = 0
            labels.append(labelling)
    
    return evidence, labels


def train_model(X_train, y_train):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    #fit the model
    model.fit(X_train, y_train)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity = 0
    total_sens = 0
    specificity = 0
    total_specs = 0
    for label, predict in zip(labels, predictions):
        #correct true positive prediction 
        if label == 1 and label == predict:
            sensitivity += 1
            total_sens += 1
        #incorrect prediction of true positive
        elif label == 1:
            total_sens += 1
        #correct true negative prediction
        if label == 0 and label == predict:
            specificity += 1
            total_specs += 1
        #incorrect true negative prediction
        elif label == 0:
            total_specs += 1

    # print(f"Right sens: {sensitivity}")
    # print(f"Total sens: {total_sens}")
    # print(f"RIght specs: {specificity}")
    # print(f"Total specs: {total_specs}")
    # print(f"Len: {len(labels)}")

    sensitivity = sensitivity / total_sens
    specificity = specificity / total_specs

    return sensitivity, specificity


if __name__ == "__main__":
    main()

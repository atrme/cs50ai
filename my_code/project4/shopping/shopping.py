import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

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
    data = list()
    evidence = list()
    labels = list()
    int_column = [0, 2, 4, 10, 11, 12, 13, 14, 15, 16]
    float_column = [1, 3, 5, 6, 7, 8, 9]
    # Digitalize_column = [10, 15, 16, 17]
    
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            data.append(row)
            
    # Transfer data into appropriate form
    # Store data in list `evidence` and `labels`
    for row in data:
        # Column Month
        match(row[10]):
            case "Jan": row[10] = 0
            case "Feb": row[10] = 1
            case "Mar": row[10] = 2
            case "Apr": row[10] = 3
            case "May": row[10] = 4
            case "June": row[10] = 5
            case "Jul": row[10] = 6
            case "Aug": row[10] = 7
            case "Sep": row[10] = 8
            case "Oct": row[10] = 9
            case "Nov": row[10] = 10
            case "Dec": row[10] = 11
        # Column VisitorType
        row[15] = 1 if row[15] == "Returning_Visitor" else 0
        
        # Column Weekend
        row[16] = 1 if row[16] == "TRUE" else 0
        
        # Column Revenue
        row[17] = 1 if row[17] == "TRUE" else 0
        
        # Transfer data type to int
        for i in int_column:
            row[i] = int(row[i])
            
        # Transfer data type to float
        for i in float_column:
            row[i] = float(row[i])
        
        # Store data in specific lists
        evidence.append(row[:-1])
        labels.append(row[-1])
        
            
    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    length = len(labels)
    pos_label_count = 0
    neg_label_count = 0
    true_pos_count = 0
    true_neg_count = 0
    
    # Start counting
    for i in range(length):
        if labels[i] == 0:
            neg_label_count += 1
        else:
            pos_label_count += 1
        
        if labels[i] == predictions[i]:
            if labels[i] == 0:
                true_neg_count += 1
            else:
                true_pos_count += 1
    
    sensitivity = true_pos_count / pos_label_count
    specificity = true_neg_count / neg_label_count
    
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()

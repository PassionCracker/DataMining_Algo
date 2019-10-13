import csv
import random
import math
import pandas as pd
''' defining functions for individual tasks...
1. To open iris CSV file as dataframe
2. For splitting given dataset into taining and testing set( based on given split ratio)
3. Divide dataset into dictionary based on class labels. '''
def loadCSV(csv_filepath):
    dataframe = pd.read_csv(csv_filepath)
    #dataframe is like 2D matrix. If any data is non numeric, convert it into numeric one's.
    #Here in iris dataset, target variable,"variety" is non numeric. hence , need to be converted.
    num = {'Setosa':0,'Versicolor':1,'Virginica':2}
    dataframe = dataframe.replace(num)
    dataset=[]
    for index,rows in dataframe.iterrows():
        row = []
        for item in rows:
            row.append(item)
        dataset.append(row)
    
    return dataset
def trainTestSplit(dataset, splitratio):
    training_rows = int(splitratio*len(dataset))
    train = dataset[ : training_rows]
    test = dataset[training_rows : ]
    return train,test
def divideIntoDict(dataset):
    dict={}
    for row in dataset:
        if row[-1] not in dict:
            dict[row[-1]] = []
        dict[row[-1]].append(row)
    return dict
'''!!!!!!!!!     The above is a dictionary holding rows for each class label         !!!!!!!!!!!!!!!
This Naive bayes is000000 based on calculating probabilities.For discrete values like in play tennis dataset, it's fine.
 What about continuous values as attributes like in iris dataset?
Hence use gaussian probability density function to decide probabilities for each class variable.
 Follow the tuto link---> https://www.saedsayad.com/naive_bayesian.htm '''
def mean(numbers):
    return sum(numbers)/float(len(numbers))
 
def stdev(numbers):
    avg = mean(numbers)
    variance = 0
    for item in numbers:
        variance += (item-avg)*(item-avg)
    variance = variance/float(len(numbers)-1)
    return math.sqrt(variance)
''' Importance of zip function in python here
 x = zip([1,2],[3,4])
print(tuple(x))
o/p : ((1,3),(2,4))
 Here dict[0] is a list of lists. To extract all the lists at a time, use *dict[0]
summary_dict contains key as target and values as list of tuples, where each tuple corresponds to mean and std dev of an attribute   '''
def get_summary_dict(dict):
    summary_dict = {}
    for key in dict:
        summary_dict[key] = []
        for item in tuple(zip(*dict[key])):
            summary_dict[key].append((mean(item),stdev(item)))
        del summary_dict[key][-1]
    return summary_dict
# Gaussian Probability density function
def calculateProbability(x, mean, stdev):
    exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
    val=(1 / (math.sqrt(2*math.pi) * stdev)) * exponent
    return val
def calculateClassProbabilities(summary_dict,input_vector):
    probabilities = {}
    for key in summary_dict:
        probabilities[key] = 1
        i = 0
        for item in summary_dict[key]:
            x = input_vector[i] 
            probabilities[key] *= calculateProbability(x, item[0], item[1])
            i+=1
    return probabilities            
'''The above probabilities dictionary comprises of key as class and probability of tuple belongs to that class as value.
The input tuple belongs to the class of highest probability '''
def predict_class_label(summary_dict,input_vector):
    probabilities = calculateClassProbabilities(summary_dict,input_vector)
    highest_prob = 0
    for key in probabilities:
        if(probabilities[key]) >= highest_prob:
            label = key
            highest_prob = probabilities[key]
    return label
def getPredictions(summary_dict,test):
    predictions = []
    for row in test:
        result = predict_class_label(summary_dict,row)
        predictions.append(result)
    return predictions
 
def getAccuracy(test, predictions):
    correct = 0
    i=0
    for row in test:
        if row[-1] == predictions[i]:
            correct += 1
        i+=1
    return (correct/float(len(test))) * 100.0

def main():
    filepath = "iris.csv"
    split_ratio = 0.68
    dataset = loadCSV(filepath)
    train,test = trainTestSplit(dataset,split_ratio)
    dict = divideIntoDict(train)
    summary_dict = get_summary_dict(dict)
    predictions = getPredictions(summary_dict,test)
    accuracy = getAccuracy(test, predictions)
    print(accuracy)
    #label=predict_class_label(summary_dict,[5.1,2.5,3,1.1])
    #print(label)

#Calling main driver function
main()    

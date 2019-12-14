import csv
import pandas as pd
import numpy as np

dataframe = pd.read_csv('durudataset.csv')
    #dataframe is like 2D matrix. If any data is non numeric, convert it into numeric one's.
    #Here in iris dataset, target variable,"variety" is non numeric. hence , need to be converted.
dataset=[]
for index,rows in dataframe.iterrows():
    row = []
    for item in rows:
        row.append(item)
    dataset.append(row)

instances = len(dataset)    

def calc_dist(point,center):
    distance = 0
    for i in range(len(point)):
        distance+= (point[i]-center[i])*(point[i]-center[i])
    return distance

def calc_center(points_list):
    zipped = tuple(zip(*points_list))
    center=[]
    for item in zipped:
        center.append(sum(item)/len(item))
    return center

def kmeans(k):
    centroids = []
    for item in np.random.randint(instances-1, size=k):
        centroids.append(dataset[item])
    dict = {}
    for i in range(k):
        dict[i] = []
        dict[i].append(centroids[i])
    new_dict = {}
    while dict != new_dict:
        new_dict = dict
        for point in dataset:
            dist = []
            for center in centroids:
                dist.append(calc_dist(point,center))
            cluster = dist.index(min(dist))
            dict[cluster].append(point)
        centroids = []
        for key in dict:
            centroids.append(calc_center(dict[key]))
    print(dict)

kmeans(2)
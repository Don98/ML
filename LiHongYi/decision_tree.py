#coding: utf-8
import numpy as np
import pandas as pd

 
def generate_data(seed):
    np.random.seed(seed)
    
    data_size_1 = 300
    
    x1_1 = np.random.normal(loc = 5.0 , scale = 1.0 , size = data_size_1)
    x2_1 = np.random.normal(loc = 4.0 , scale = 1.0 , size = data_size_1)
    y1 = [0 for i in range(data_size_1)]
    
        
    data_size_2 = 400
    
    x1_2 = np.random.normal(loc = 5.0 , scale =2.0 , size = data_size_2)
    x2_2 = np.random.normal(loc = 4.0 , scale = 2.0 , size = data_size_2)
    y2 = [1 for i in range(data_size_2)]
    
    x1 = np.concatenate((x1_1 , x1_2) , axis = 0)
    x2 = np.concatenate((x2_1 , x2_2) , axis = 0)
    
    x = np.hstack((x1.reshape(-1,1), x2.reshape(-1,1)))
    y = np.concatenate((y1,y2),axis = 0)
    
    data_size_all = data_size_1 + data_size_2
    
    shuffle_index = np.random.permutation(data_size_all)
    
    x = x[shuffle_index]
    y = y[shuffle_index]
    
    return x,y.reshape((data_size_all,1))
   
def calcShannonEnt(data):
    numEntries = len(data)
    labelCounts = {}
    for featVec in data:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt -= prob*np.log2(prob)
    return shannonEnt

def splitdata(data, axis, value):
    retdata = []
    for featVec in data:
        if featVec[axis] == value:
            reducedFeatVec = list(featVec[:axis])
            reducedFeatVec.extend(featVec[axis+1:])
            retdata.append(reducedFeatVec)
    return retdata

def chooseBestFeature(data):
    numFeature = len(data[0])-1
    baseEntroy = calcShannonEnt(data)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeature):
        featureList = [example[i] for example in data]
        uniqueVals = set(featureList)
        newEntropy = 0.0
        for value in uniqueVals:
            subdata = splitdata(data, i, value)
            prob = len(subdata) / float(len(data))
            newEntropy += prob * np.log2(prob)
        inforGain = baseEntroy - newEntropy
        
        if inforGain > bestInfoGain:
            bestInfoGain = inforGain
            bestFeature = i
    return bestFeature

def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount += 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def createTree(data, labels):
    classList = [example[-1] for example in data]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if (len(data[0]) == 1):
        return majorityCnt(classList)
    
    bestFeat = chooseBestFeature(data)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel[0]:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in data]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel[0]][value] = createTree(splitdata(data, bestFeat, value), subLabels)
    return myTree
    

if __name__ == '__main__':
    x , y = generate_data(100)
    data = np.hstack((x,y))
    data = list(data)
    x = list(x);y = list(y)
    shannonEnt = calcShannonEnt(data)
    tree = createTree(data, y)
    print (tree)
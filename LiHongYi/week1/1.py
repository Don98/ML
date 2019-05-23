import numpy as np
import scipy 
import pandas as pd
from sklearn.metrics import r2_score
lr = 0.1**6
# lr = 0.001

def get_train():
    #获得PM2.5的训练数据
    with open("train.csv") as f:
        data = f.readlines()
    data = [i.strip().split(',') for i in data]
    train_data = [];train_label = [];
    for i in data[10::18]:
        for j in range(len(i[3:]) - 10):
            train_data.append(i[3:][j : j + 9])
            train_label.append(i[3:][j + 10])
    return np.array(train_data,dtype = np.float64),np.array(train_label,dtype = np.float64)

def get_test():
    #获得PM2.5的测试数据
    with open("test(1).csv") as f:
        data = f.readlines()
    data = [i.strip().split(',') for i in data]
    test_data = [];test_label = [];
    for i in data[9::18]:
        test_data.append(i[2:])
    with open("answer.csv") as f:
        data = f.readlines()
    data = [i.strip().split(',') for i in data]
    for i in data[1:]:
        test_label.append(i[1])
    return np.array(test_data,dtype = np.float64),np.array(test_label,dtype = np.float64)


def get_r2(pre,label):
    print(1 - np.sum((pre - label) ** 2) / np.sum((np.mean(label) - label) ** 2))
    # print(r2_score(label, pre, multioutput='raw_values'))

def all_dg(train_data,w,test_data,test_label,train_label,num):
    for i in range(num):
        pre = np.dot(train_data,w)
        w = np.sum((w.T - lr * train_data * (pre - train_label) / train_data.shape[1]).T,axis = 1) / train_data.shape[0]
        
        w.resize((len(w)),1)
        
        # error = np.sum((pre - train_label)**2)
        # print(np.sqrt(error))
    
    pre = np.dot(train_data,w)
    
    print("train".center(20,'-'))
    
    get_r2(pre,train_label)
    error = np.sum((pre - train_label)**2)
    print(np.sqrt(error))
    
    test_data =np.concatenate((np.ones((test_data.shape[0],1)),test_data),axis=1)
    
    pre = np.dot(test_data,w)
    
    print("test".center(20,'-'))
    get_r2(pre,test_label)
    
    error = np.sum((pre - test_label)**2)
    print(np.sqrt(error))

def all_ada(train_data,w,test_data,test_label,train_label,num):
    sum_gra = 0
    for i in range(num):
        pre = np.dot(train_data,w)
        print(pre.shape)
        loss = (pre - train_label)* 2
        sum_gra += loss**2
        ada = np.sqrt(sum_gra)
        
        w = np.sum((w.T - lr / ada * train_data * loss / train_data.shape[1]).T,axis = 1) / train_data.shape[0]
        
        w.resize((len(w)),1)
        
        # error = np.sum((pre - train_label)**2)
        # print(np.sqrt(error))
    
    get_r2(pre,train_label)
    
    test_data =np.concatenate((np.ones((test_data.shape[0],1)),test_data),axis=1)
    pre = np.dot(test_data,w)
    error = np.sum((pre - test_label)**2)
    get_r2(pre,test_label)
    print(np.sqrt(error))
    

if __name__ == '__main__':
    train_data , train_label = get_train()
    test_data , test_label = get_test()
    test_label.resize((test_label.shape[0],1))
    train_data = np.concatenate((np.ones((train_data.shape[0],1)),train_data),axis=1)
    train_label.resize((train_label.shape[0],1))
    w = np.zeros((train_data.shape[1],1))
    # print(train_data)
    #使用全梯度下降,进行一万次迭代
    all_dg(train_data,w,test_data,test_label,train_label,10000)
    # all_ada(train_data,w,test_data,test_label,train_label,10000)
        
    # pre = np.dot(train_data,w)
    # error = np.sum((pre - train_label)**2)
    # print(np.sqrt(error))
                
import numpy as np
import scipy 
import pandas as pd

lr = 0.001
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

if __name__ == '__main__':
    train_data , train_label = get_train()
    test_data , test_label = get_test()
    train_data = np.concatenate((np.ones((train_data.shape[0],1)),train_data),axis=1)
    train_label.resize((train_label.shape[0],1))
    w = np.zeros((train_data.shape[1],1))
    # print(train_data)
    
    #使用全梯度下降,进行一万次迭代
    for i in range(10000):
        pre = np.dot(train_data,w)
        loss = pre - train_label
        w = np.sum((w.T - lr * train_data * loss / train_data.shape[1]).T,axis = 1) / train_data.shape[0]
        
        w.resize((len(w)),1)
        
    # test_data =np.concatenate((np.ones((test_data.shape[0],1)),test_data),axis=1)
    # pre = np.dot(test_data,w)
    # error = np.sum((pre - test_label)**2)
    # print(np.sqrt(error))
        
    pre = np.dot(train_data,w)
    error = np.sum((pre - train_label)**2)
    print(np.sqrt(error))
                
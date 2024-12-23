# -*- coding: utf-8 -*-
"""Лабораторная работа №1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xWeDtpLu1pvlygk6RoOX867SGO0FY_00
"""

import numpy as np
import pandas as pd

class Perceptron:
    def __init__(self, inputSize, hiddenSizes, outputSize):

        self.Win = np.zeros((1+inputSize,hiddenSizes))
        self.Win[0,:] = (np.random.randint(0, 3, size = (hiddenSizes)))
        self.Win[1:,:] = (np.random.randint(-1, 2, size = (inputSize,hiddenSizes)))

        self.Wout = np.random.randint(0, 2, size = (1+hiddenSizes,outputSize)).astype(np.float64)
        #self.Wout = np.random.randint(0, 3, size = (1+hiddenSizes,outputSize))

    def predict(self, Xp):
        hidden_predict = np.where((np.dot(Xp, self.Win[1:,:]) + self.Win[0,:]) >= 0.0, 1, -1).astype(np.float64)
        out = np.where((np.dot(hidden_predict, self.Wout[1:,:]) + self.Wout[0,:]) >= 0.0, 1, -1).astype(np.float64)
        return out, hidden_predict

    def train(self, X, y, n_iter=5, eta = 0.01):
        errors_is_epoch_count = 0
        for i in range(n_iter):
            prev_wout = self.Wout.copy()
            print('Веса на итерации ', i, ': ', self.Wout.reshape(1, -1))
            for xi, target, j in zip(X, y, range(X.shape[0])):
                pr, hidden = self.predict(xi)
                if target.sum()-pr.sum() != 0:
                    errors_is_epoch_count += 1
                self.Wout[1:] += ((eta * (target - pr)) * hidden).reshape(-1, 1)
                self.Wout[0] += eta * (target - pr)
            if errors_is_epoch_count == 0:
                print('Перцептрон сошёлся')
                break
            else:
                print('Ошибок в эпохе: ', errors_is_epoch_count)
                errors_is_epoch_count = 0
            if np.array_equal(prev_wout,self.Wout):
                print('Перцептрон "зациклился"')
                print('Веса на итерации ', i, ': ', self.Wout.reshape(1, -1))
                break
        return self

df = pd.read_csv('/content/drive/MyDrive/Глубокое обучение/1/data.csv');

df = df.iloc[np.random.permutation(len(df))]
y = df.iloc[0:100, 4].values
y = np.where(y == "Iris-setosa", 1, -1)
X = df.iloc[0:100, [0, 2]].values

inputSize = X.shape[1]
hiddenSizes = 10
outputSize = 1 if len(y.shape) else y.shape[1]

NN = Perceptron(inputSize, hiddenSizes, outputSize)
NN.train(X, y, n_iter=100, eta = 0.01)
# -*- coding: utf-8 -*-
"""20200626-ML-Tensorflow-KNN-credit.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mbxkODvo7Zlvx7dgrr5sfqbqyJwIIdST
"""

# module import
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# dataset path
DATA_path = '/content/drive/My Drive/멀티캠퍼스/[혁신성장] 인공지능 자연어처리 기반/[강의]/조성현 강사님/dataset'

# load data
data = pd.read_csv(f"{DATA_path}/3-4.credit_data.csv")

# data to numpy array
data = np.array(data)

# split data
def splitData(data, train_size=0.8):
    train_num = int(len(data) * train_size)
    X_train, X_test = data[:train_num, :-1], data[train_num:, :-1]
    y_train, y_test = data[:train_num, -1], data[train_num:, -1]
    return X_train, X_test, y_train, y_test

X_train, X_test, y_train, y_test = splitData(data)

# reshape labels
y_train = y_train.reshape(len(y_train), 1)
y_test = y_test.reshape(len(y_test), 1)

# KNN 학습
accuracy_history = []
opt_K, opt_accuracy = 0, 0.0 
min_K, max_K = 2, 100
y_hat_opt = [] 

for k in range(min_K, max_K+1):
    y_hat = []

    # 각각의 테스트 데이터에 대해 거리 계산 후 클래스 평균 점수 계산
    for x in X_test:
        x = x.reshape(1, 6)
        distance = tf.sqrt(tf.reduce_sum(tf.math.square(tf.subtract(X_train, x)), axis=1))
        values, indices = tf.math.top_k(tf.negative(distance), k=k, sorted=False) 
        classMean = tf.reduce_mean(tf.cast(tf.gather(y_train, indices), dtype=tf.float32))
        y_hat.append(classMean.numpy())

    y_hat = np.array(y_hat)
    y_hat = y_hat.reshape(len(y_hat), 1)

    # 추정치가 0.5보다 크면 클래스를 1로, 아니면 0으로 판단.
    y_hat_pred = np.where(y_hat > 0.5, 1, 0)

    # accuracy
    accuracy = (y_test == y_hat_pred).sum()/len(y_test)
    # accuracy_2 = tf.reduce_mean(tf.cast(tf.equal(y_test, y_hat_pred), dtype=tf.float32)) # 문쌤 방식

    # 최적일 때 정확도 기록.
    if accuracy > opt_accuracy:
        y_hat_opt = y_hat.copy() # 추정치를 모두 복사
        opt_K = k
        opt_accuracy = accuracy
    
    # history 기록
    accuracy_history.append(accuracy)
    print("k = %d done" % k)

# 결과 확인
print(f"최적 이웃 수: {opt_K}, 그 때의 정확도: {opt_accuracy}")

# plot
fig = plt.figure(figsize=(10, 4))
p1 = fig.add_subplot(1, 2, 1)
p2 = fig.add_subplot(1, 2, 2)

X_range = np.arange(min_K, max_K+1)

# 정확도
p1.plot(X_range, accuracy_history)
p1.set_title('Accuracy (optimal K = ' + str(opt_K) + ')')
p1.set_xlabel('K')
p1.set_ylabel('accuracy')

# 추정치
n, bins, patches = p2.hist(y_hat_opt, 50, facecolor='blue', alpha=0.5)
p2.set_title('y_hat distribution')

plt.show()
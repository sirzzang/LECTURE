# -*- coding: utf-8 -*-
"""20200626-ML-Keras-Classification-LogisticRegression-Credit.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uOQDNxp4w0kmYFvgXqKHb7wElpRznz__
"""

# module import
import pandas as pd
import numpy as np
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# path
data_path = "/content/drive/My Drive/멀티캠퍼스/[혁신성장] 인공지능 자연어처리 기반/[강의]/조성현 강사님/dataset"

"""# 랜덤하지 않은 데이터"""

# load data
data = pd.read_csv(f"{data_path}/3-4.credit_data.csv")

# data to array
data = np.array(data)

# split data
train_num = int(len(data) * 0.8)

X_train, X_test = data[:train_num, :-1], data[train_num:, :-1]
y_train, y_test = data[:train_num, -1], data[train_num:, -1]

# reshape labels
y_train = y_train.reshape(len(y_train), 1)
y_test = y_test.reshape(len(y_test), 1)

# check shape
X_train.shape, X_test.shape, y_train.shape, y_test.shape

# 그래프 모델 생성
X_input = Input(batch_shape=(None, X_train.shape[1])) # 이거 그냥 shape이나 batch_size 아닌가?
y_output = Dense(y_train.shape[1], activation='sigmoid')(X_input)
model = Model(X_input, y_output)
model.compile(loss='binary_crossentropy',
              optimizer=Adam(lr=0.05))
print(model.summary())

# 학습
train_epoch = int(input('학습 횟수를 설정하세요. :'))
BATCH = int(input('batch 사이즈를 설정하세요. :'))

hist = model.fit(X_train, y_train,
                 validation_data = (X_test, y_test), # 이거 나중에 test에 써야 하는 거 아닌가?
                 epochs = train_epoch,
                 batch_size = BATCH,
                 shuffle=True)

# 정확도 측정
y_hat = model.predict(X_test)
y_hat_pred = np.where(y_hat > 0.5, 1, 0)
accuracy_1 = (y_test == y_hat_pred).sum() / len(y_test)
accuracy_2 = tf.reduce_mean(tf.cast(tf.equal(y_test, y_hat_pred), dtype=tf.float32))
print(accuracy_1, accuracy_2.numpy())

# plot loss
plt.plot(hist.history['loss'], label='Train Loss')
plt.plot(hist.history['val_loss'], label='Test Loss')
plt.legend()
plt.title('Loss Function')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.show()

# plot y_hat
n, bins, patches = plt.hist(y_hat, 50)
plt.title('y_hat Distribution')
plt.show()

"""# 랜덤 데이터 
* 강사님이 임의로 라벨 임의로 바꾼 데이터
* 정확도 낮아진다.
"""

# load data
data = pd.read_csv(f"{data_path}/3-4.credit_data(rand).csv")
data = np.array(data)

# split data into train, test
X_data, y_data = data[:, :-1], data[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2)
y_train, y_test = y_train.reshape(len(y_train), 1), y_test.reshape(len(y_test), 1)

# 그래프 모델 생성
X_input = Input(batch_shape=(None, X_train.shape[1]))
y_output = Dense(y_train.shape[1], activation='sigmoid')(X_input)
model = Model(X_input, y_output)
model.compile(loss='binary_crossentropy',
              optimizer=Adam(lr=0.05))
print(model.summary())

# 학습
hist = model.fit(X_train, y_train,
                 validation_data = (X_test, y_test),
                 epochs=100,
                 batch_size=30,
                 shuffle=True)

# 정확도 측정
y_hat = model.predict(X_test)
y_hat_pred = np.where(y_hat > 0.5, 1, 0)
accuracy = tf.reduce_mean(tf.cast(tf.equal(y_test, y_hat_pred), dtype=tf.float32))
print(f"정확도: {accuracy.numpy()}")

# plot loss
plt.plot(hist.history['loss'], label='Train Loss')
plt.plot(hist.history['val_loss'], label='Test Loss')
plt.legend()
plt.title('Loss Function')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.show()

# plot y_hat distribution
plt.hist(y_hat, bins=50)
plt.title('y_hat Distribution')
plt.show()
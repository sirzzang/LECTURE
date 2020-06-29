# -*- coding: utf-8 -*-
"""20202629-DL-Keras-Classification-LogisticRegression-credit-practice.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Xyksvt6Vb8tRFHvBeT_wsT8cJYYw1eY0
"""

# module import
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras import optimizers, regularizers
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt

# dataset folder
data_path = '/content/drive/My Drive/멀티캠퍼스/[혁신성장] 인공지능 자연어처리 기반/[강의]/조성현 강사님/dataset'

# load and prepare data
data = pd.read_csv(f'{data_path}/3-4.credit_data.csv')
data = np.array(data)
X_data = data[:, :-1]
y_data = data[:, -1]
y_data = y_data.reshape(len(y_data), 1) # 2차원 배열

# split data
X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2)

# 모델 그래프 생성
X_input = Input(batch_shape=(None, X_train.shape[1]))
X_hidden = Dense(8, kernel_regularizer=regularizers.l2(0.05), activation='relu')(X_input)
y_output = Dense(y_train.shape[1], kernel_regularizer=regularizers.l2(0.05), activation='sigmoid')(X_hidden)

# 모델
model = Model(X_input, y_output)
model.compile(loss='binary_crossentropy', optimizer=optimizers.Adam(lr=0.01))
print(model.summary())

# 학습
hist = model.fit(X_train, y_train,
                 validation_data = (X_test, y_test),
                 epochs=100,
                 batch_size=50)

# 정확도
y_hat = model.predict(X_test)
y_hat_pred = np.where(y_hat > 0.5, 1, 0)
test_accuracy = 100 * (y_test == y_hat_pred).mean()
print(f'Final Test Accuracy: {test_accuracy}')

# 결과 확인
fig = plt.figure(figsize=(10, 4))
p1 = fig.add_subplot(1,2,1)
p2 = fig.add_subplot(1,2,2)

# plot loss
p1.plot(hist.history['loss'], label='Train Loss')
p1.plot(hist.history['val_loss'], label='Test Loss')
p1.legend()
p1.set_title('Loss Function')
p1.set_xlabel('Epoch')
p1.set_ylabel('Loss')

# plot y_hat
n, bins, patches = p2.hist(y_hat, 50, facecolor='blue', alpha=0.5)
p2.set_title('y_hat Distribution')
plt.show()
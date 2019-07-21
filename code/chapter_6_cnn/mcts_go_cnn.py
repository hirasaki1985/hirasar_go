# -*- coding: utf-8 -*-

from __future__ import print_function

# tag::mcts_go_cnn_preprocessing[]
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D

np.random.seed(123)
X = np.load('../generated_games/features-200.npy')
Y = np.load('../generated_games/labels-200.npy')

samples = X.shape[0]
size = 9
input_shape = (size, size, 1)

X = X.reshape(samples, size, size, 1)

train_samples = 10000
X_train, X_test = X[:train_samples], X[train_samples:]
Y_train, Y_test = Y[:train_samples], Y[train_samples:]
# end::mcts_go_cnn_preprocessing[]

# tag::mcts_go_cnn_model[]
model = Sequential()
"""
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=input_shape))
"""

# filter = 48
# 3×3の畳み込みカーネルを選択する
# 通常、畳み込みの出力は入力よりも小さくなる。
# padding = 'same'を追加することで、Kerasに行列をエッジの周りに０で埋めるようにできるため、出力は入力と同じ次元を持つようになる。
model.add(Conv2D(filters=48,  # <1>
                 kernel_size=(3, 3),  # <2>
                 activation='sigmoid',
                 padding='same',
                 input_shape=input_shape))

model.add(Dropout(rate=0.6))
model.add(Conv2D(64, (3, 3), activation='relu'))

# 最大プーリング
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(rate=0.6))

# 平坦化
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(rate=0.6))

# ソフトマックス
model.add(Dense(size * size, activation='softmax'))
model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer='sgd',
              metrics=['accuracy'])
# end::mcts_go_cnn_model[]

# tag::mcts_go_cnn_eval[]
model.fit(X_train, Y_train,
          batch_size=64,
          epochs=5,
          verbose=1,
          validation_data=(X_test, Y_test))
score = model.evaluate(X_test, Y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
# end::mcts_go_cnn_eval[]

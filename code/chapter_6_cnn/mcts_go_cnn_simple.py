# -*- coding: utf-8 -*-

from __future__ import print_function

# tag::mcts_go_cnn_simple_preprocessing[]
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Conv2D, Flatten  # <1>

np.random.seed(123)
X = np.load('../generated_games/features-200.npy')
Y = np.load('../generated_games/labels-200.npy')

samples = X.shape[0]
size = 9
input_shape = (size, size, 1)  # <2>

X = X.reshape(samples, size, size, 1)  # <3>

train_samples = 10000
X_train, X_test = X[:train_samples], X[train_samples:]
Y_train, Y_test = Y[:train_samples], Y[train_samples:]

# <1> We import two new layers, a 2D convolutional layer and one that flattens its input to vectors.
# <2> The input data shape is 3-dimensional, we use one plane of a 9x9 board representation.
# <3> We then reshape our input data accordingly.
# end::mcts_go_cnn_simple_preprocessing[]

# tag::mcts_go_cnn_simple_model[]
model = Sequential()

"""
model.add(Conv2D(filters=32,  # <1>
                 kernel_size=(3, 3),  # <2>
                 activation='sigmoid',
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

# 二番目の別の畳み込み層。
model.add(Conv2D(64, (3, 3), activation='sigmoid'))  # <3>

# 前の畳み込み層の３D出力を平坦化する
model.add(Flatten())  # <4>

model.add(Dense(128, activation='sigmoid'))
model.add(Dense(size * size, activation='sigmoid'))  # <5>
model.summary()

# <1> The first layer in our network is a Conv2D layer with 32 output filters.
# <2> For this layer we choose a 3 by 3 convolutional kernel.
# <3> The second layer in another convolution. We leave out the "filters" and "kernel_size" arguments for brevity.
# <4> We then flatten the 3D output of the previous convolutional layer...
# <5> ... and follow up with two more dense layers, as we did in the MLP example.
# end::mcts_go_cnn_simple_model[]

# tag::mcts_go_cnn_simple_eval[]
model.compile(loss='mean_squared_error',
              optimizer='sgd',
              metrics=['accuracy'])

model.fit(X_train, Y_train,
          batch_size=64,
          epochs=5,
          verbose=1,
          validation_data=(X_test, Y_test))

score = model.evaluate(X_test, Y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
# end::mcts_go_cnn_eval[]

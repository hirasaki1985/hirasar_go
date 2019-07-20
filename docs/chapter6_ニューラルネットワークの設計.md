# 囲碁データのためのニューラルネットワークの設計
## 深層学習ライブラリKeras

```
$ python code/chapter_6_cnn/mcts_go_mlp.py
Using TensorFlow backend.
WARNING: Logging before flag parsing goes to stderr.
W0720 16:05:43.698403 4632757696 deprecation_wrapper.py:119] From ~/.pyenv/versions/hirasar-go/lib/python3.7/site-packages/keras/backend/tensorflow_backend.py:74: The name tf.get_default_graph is deprecated. Please use tf.compat.v1.get_default_graph instead.

W0720 16:05:43.708019 4632757696 deprecation_wrapper.py:119] From ~/.pyenv/versions/hirasar-go/lib/python3.7/site-packages/keras/backend/tensorflow_backend.py:517: The name tf.placeholder is deprecated. Please use tf.compat.v1.placeholder instead.

W0720 16:05:43.709558 4632757696 deprecation_wrapper.py:119] From ~/.pyenv/versions/hirasar-go/lib/python3.7/site-packages/keras/backend/tensorflow_backend.py:4138: The name tf.random_uniform is deprecated. Please use tf.random.uniform instead.

_________________________________________________________________
Layer (type)                 Output Shape              Param #
=================================================================
dense_1 (Dense)              (None, 200)               16400
_________________________________________________________________
dense_2 (Dense)              (None, 300)               60300
_________________________________________________________________
dense_3 (Dense)              (None, 200)               60200
_________________________________________________________________
dense_4 (Dense)              (None, 81)                16281
=================================================================
Total params: 153,181
Trainable params: 153,181
Non-trainable params: 0
_________________________________________________________________
W0720 16:05:43.751164 4632757696 deprecation_wrapper.py:119] From ~/.pyenv/versions/hirasar-go/lib/python3.7/site-packages/keras/optimizers.py:790: The name tf.train.Optimizer is deprecated. Please use tf.compat.v1.train.Optimizer instead.

W0720 16:05:43.879193 4632757696 deprecation_wrapper.py:119] From ~/.pyenv/versions/hirasar-go/lib/python3.7/site-packages/keras/backend/tensorflow_backend.py:986: The name tf.assign_add is deprecated. Please use tf.compat.v1.assign_add instead.

W0720 16:05:43.904242 4632757696 deprecation_wrapper.py:119] From ~/.pyenv/versions/hirasar-go/lib/python3.7/site-packages/keras/backend/tensorflow_backend.py:973: The name tf.assign is deprecated. Please use tf.compat.v1.assign instead.

Train on 10000 samples, validate on 1705 samples
Epoch 1/5
2019-07-20 16:05:43.931442: I tensorflow/core/platform/cpu_feature_guard.cc:142] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
10000/10000 [==============================] - 0s 38us/step - loss: 0.2301 - acc: 0.0166 - val_loss: 0.2027 - val_acc: 0.0170
Epoch 2/5
10000/10000 [==============================] - 0s 24us/step - loss: 0.1798 - acc: 0.0166 - val_loss: 0.1581 - val_acc: 0.0170
Epoch 3/5
10000/10000 [==============================] - 0s 25us/step - loss: 0.1405 - acc: 0.0166 - val_loss: 0.1242 - val_acc: 0.0170
Epoch 4/5
10000/10000 [==============================] - 0s 24us/step - loss: 0.1112 - acc: 0.0166 - val_loss: 0.0992 - val_acc: 0.0170
Epoch 5/5
10000/10000 [==============================] - 0s 24us/step - loss: 0.0898 - acc: 0.0166 - val_loss: 0.0811 - val_acc: 0.0170
Test loss: 0.08112459710616171
Test accuracy: 0.017008797653958945
```

Trainable params: 153,181
訓練プロセスがTrainable paramsの数の個々の重みの値を更新していることを意味している。


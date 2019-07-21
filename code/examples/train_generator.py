# tag::train_generator_imports[]
from dlgo.data.parallel_processor import GoDataProcessor
from dlgo.encoders.oneplane import OnePlaneEncoder

from dlgo.networks import small
from keras.models import Sequential
from keras.layers.core import Dense

# モデルのチェックポイントでは、時間のかかる実験の進捗状況を保存できる
from keras.callbacks import ModelCheckpoint  # <1>

# <1> With model checkpoints we can store progress for time-consuming experiments
# end::train_generator_imports[]

# tag::train_generator_generator[]
go_board_rows, go_board_cols = 19, 19
num_classes = go_board_rows * go_board_cols
num_games = 100

# 盤のサイズのエンコーダーを作成する
encoder = OnePlaneEncoder((go_board_rows, go_board_cols))  # <1>

# Go Data Processorを初期化する
processor = GoDataProcessor(encoder=encoder.name())  # <2>

# プロセッサから、訓練とテストのための２つのデータジェネレータを作成する
generator = processor.load_go_data('train', num_games, use_generator=True)  # <3>
test_generator = processor.load_go_data('test', num_games, use_generator=True)

# <1> First we create an encoder of board size.
# <2> Then we initialize a Go Data processor with it.
# <3> From the processor we create two data generators, for training and testing.
# end::train_generator_generator[]

# tag::train_generator_model[]
# 小さな層のアーキテクチャからKerasモデルを定義する
input_shape = (encoder.num_planes, go_board_rows, go_board_cols)
network_layers = small.layers(input_shape)
model = Sequential()
for layer in network_layers:
    model.add(layer)
model.add(Dense(num_classes, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])
# end::train_generator_model[]

# tag::train_generator_fit[]
# ジェネレータを使用したKerasモデルの適合と評価
epochs = 5
batch_size = 128

# バッチサイズの訓練ジェネレータを指定
model.fit_generator(generator=generator.generate(batch_size, num_classes),  # <1>
                    epochs=epochs,

                    # エポックごとにいくつの訓練ステップが実行されるかを指定する
                    steps_per_epoch=generator.get_num_samples() / batch_size,  # <2>

                    # 検証のために追加のジェネレータが使用される
                    validation_data=test_generator.generate(batch_size, num_classes),  # <3>

                    # ステップ数
                    validation_steps=test_generator.get_num_samples() / batch_size,  # <4>

                    # 各エポックの後、モデルのチェックポイントを保存する
                    callbacks=[ModelCheckpoint('../checkpoints/small_model_epoch_{epoch}.h5')])  # <5>

# 評価のためのジェネレータとステップ数を指定する
model.evaluate_generator(generator=test_generator.generate(batch_size, num_classes),
                         steps=test_generator.get_num_samples() / batch_size)  # <6>
# <1> We specify a training data generator for our batch size...
# <2> ... and how many training steps per epoch we execute.
# <3> An additional generator is used for validation...
# <4> ... which also needs a number of steps.
# <5> After each epoch we persist a checkpoint of the model.
# <6> For evaluation we also speficy a generator and the number of steps.
# end::train_generator_fit[]

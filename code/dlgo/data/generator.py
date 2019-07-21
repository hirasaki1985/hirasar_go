# -*- coding: utf-8 -*-

# tag::data_generator[]
import glob
import numpy as np
from keras.utils import to_categorical


class DataGenerator:
    def __init__(self, data_directory, samples):
        self.data_directory = data_directory
        self.samples = samples

        # ジェネレータは、先にサンプリングした一連のファイルにアクセスする
        self.files = set(file_name for file_name, index in samples)  # <1>
        self.num_samples = None

    # アプリケーションによっては、どれくらいのサンプルがあるか知る必要があるかもしれない
    def get_num_samples(self, batch_size=128, num_classes=19 * 19):  # <2>
        if self.num_samples is not None:
            return self.num_samples
        else:
            self.num_samples = 0
            for X, y in self._generate(batch_size=batch_size, num_classes=num_classes):
                self.num_samples += X.shape[0]
            return self.num_samples
# <1> Our generator has access to a set of files that we sampled earlier.
# <2> Depending on the application, we may need to know how many examples we have.
# end::data_generator[]

# tag::private_generate[]
    # 囲碁データの次のバッチを生成してyieldするプライベートメソッド
    def _generate(self, batch_size, num_classes):
        for zip_file_name in self.files:
            file_name = zip_file_name.replace('.tar.gz', '') + 'train'
            base = self.data_directory + '/' + file_name + '_features_*.npy'
            for feature_file in glob.glob(base):
                label_file = feature_file.replace('features', 'labels')
                x = np.load(feature_file)
                y = np.load(label_file)
                x = x.astype('float32')
                y = to_categorical(y.astype(int), num_classes)
                while x.shape[0] >= batch_size:
                    x_batch, x = x[:batch_size], x[batch_size:]
                    y_batch, y = y[:batch_size], y[batch_size:]
                    yield x_batch, y_batch  # <1>

# <1> We return or "yield" batches of data as we go.
# end::private_generate[]

# tag::generate[]
    # モデル訓練用のジェネレータを取得するためのgenerateメソッドを呼び出す
    def generate(self, batch_size=128, num_classes=19 * 19):
        while True:
            for item in self._generate(batch_size, num_classes):
                yield item
# end::generate[]

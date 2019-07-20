# hirasar_go
## versions
```
$ pyenv -v
pyenv 1.2.13
$ python -V
Python 3.7.3
```

## install
### 必要なライブラリのインストール
```
$ brew install pyenv
$ brew install pyenv-virtualenv
$ pyenv install anaconda3-5.3.1
$ pyenv global anaconda3-5.3.1
```

### 環境構築
```
$ pyenv virtualenv anaconda3-5.3.1 hirasar-go
$ pyenv local hirasar-go
$ pyenv versions
(hirasar-go)$ pip install -r requirements.txt
```

## execution
### simple bot vs bot
```
$ python code/bot_v_bot.py
```

### section 6
MCTSで打ったものを正解ラベルとしてテストデータ生成。このゲーム生成はかなり遅い。

```
$ python code/generate_mcts_games.py -n 20 --board-out feature.npy --move-out labels.npy
```

学習
```
$ python code/chapter_6_cnn/mcts_go_mlp.py
```


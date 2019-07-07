## 内容
### ミニマックスアルゴリズムで最前の手を見つける
#### すぐにゲームに勝つ手を見つける関数
```
def find_winning_move(game_state, next_player):
  # 全ての合法手についてループする
  for candidate_move in game_state.legal_moves(next_player):
    # この手を選ぶと盤がどうなるかを計算する
    next_state = game_state.apply_move(candidate_move)

    if next_state.is_over() and next_state.winner == next_player:
      # 勝利する手の場合はこれ以上調べる必要がないので返す
      return candidate_move

  # この手盤では勝てない
  return None
```

#### 相手に勝つ手を与えないようにする関数
```
def eliminate_losing_moves(game_state, next_player):
  opponent = next_player.othr()

  # 検討する価値のある全ての手のリストになる
  possible_moves = []

  # 全ての合法手についてループする
  for candidate_move in game_state.legal_moves(next_player):
    # この手を選ぶと盤がどうなるかを計算する
    next_state = game_state.apply_move(candidate_move)

    # この手で相手が勝つだろうか？そうでなければ、この手が候補となる
    opponent_winning_move = find_winning_move(next_state, opponent)

    if opponent_winning_move is None:
      possible_moves.append(candidate_move)

  return possible_moves
```

#### 勝ちを保証する２手の手順を見つける関数
```
def find_two_step_win(game_state, next_player):
  opponent = next_player.other()

  # 全ての合法手についてループする
  for candidate_move in game_state.legal_moves(next_player):
    # この手を選ぶと盤がどうなるかを計算する
    next_state = game_state.apply_move(candidate_move)

    相手は防ぐ手はあるか？そうでない場合は、この手を選択する
    good_response = eliminate_losing_moves(next_state, opponent)

    if not good_response:
      return candidate_move

  # どんな手を選んでも、相手は勝利を防ぐことができる
  return None
```


### スピードアップのためのミニマックス木探索の枝刈り


### ゲームへのモンテカルロ木探索の適用


## まとめ
* 木探索アルゴリズムは、最良の選択肢を見つけるために多くの可能な手順を評価する。木探索はゲームや一般的な最適化問題でも取り上げられる。
* ゲームに適用される木探索の形態は、ミニマックス木探索です。ミニマックス木探索では、反対の目標を持つ二人のプレイヤーを交互に入れ替える。
* 完全なミニマックス木探索は、非常に単純なゲームでのみ実用的。複雑なゲームに適用するには探索する木のサイズを小さくする必要がある。
* 局面評価関数は、特定の局面からどのプレイヤーが勝つ可能性が高いかを推定する。局面評価関数が優れていれば、決定をするためにゲームの最後まで探索する必要はありません。この戦略が深さの枝刈りです。
* αβ法は、各手番で考慮する必要のある手数を減らすため、チェスのように複雑なゲームでも実用的。αβ法の考え方は直感で理解できる。可能な手を評価する時に相手の手に１つの強い応手を見つけた場合、その手をすぐに考慮から完全に取り除くことができる。
* 良い局面評価のヒューリスティックがない場合、モンテカルロ木探索アルゴリズムを使用することがある。このアルゴリズムは特定の局面からランダムにゲームをシュミレートし、どのプレイヤーがより頻繁に勝つかを追跡する。
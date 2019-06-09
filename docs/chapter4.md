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



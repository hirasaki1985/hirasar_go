# -*- coding: utf-8 -*-

import random

from dlgo.agent import Agent
from dlgo.gotypes import Player

__all__ = [
    'AlphaBetaAgent',
]

MAX_SCORE = 999999
MIN_SCORE = -999999


# tag::alpha-beta-prune-1[]
def alpha_beta_result(game_state, max_depth, best_black, best_white, eval_fn):
    # すでに終局していれば、勝者が誰かわかる
    if game_state.is_over():                                   # <1>
        if game_state.winner() == game_state.next_player:      # <1>
            return MAX_SCORE                                   # <1>
        else:                                                  # <1>
            return MIN_SCORE                                   # <1>

    # 最大の検索の深さに達したので、ヒューリスティックを使用して、この手順がどの程度良いか判定する
    if max_depth == 0:                                         # <2>
        return eval_fn(game_state)                             # <2>

    best_so_far = MIN_SCORE

    # 全ての可能な手をループする
    for candidate_move in game_state.legal_moves():            # <3>
        # この手を取った場合、盤面がどうなるか調べる
        next_state = game_state.apply_move(candidate_move)     # <4>

        # この局面からの相手の最良の結果を見つける
        opponent_best_result = alpha_beta_result(              # <5>
            next_state, max_depth - 1,                         # <5>
            best_black, best_white,                            # <5>
            eval_fn)                                           # <5>

        # 相手が望む手と反対の手を求める
        our_result = -1 * opponent_best_result                 # <6>

        # この結果が、これまで調べた中で最高の結果よりも良いか確認する
        if our_result > best_so_far:                           # <7>
            best_so_far = our_result                           # <7>
# end::alpha-beta-prune-1[]

# tag::alpha-beta-prune-2[]
        if game_state.next_player == Player.white:
            # 白の基準値を更新する
            if best_so_far > best_white:                       # <8>
                best_white = best_so_far                       # <8>
            outcome_for_black = -1 * best_so_far               # <9>

            # 現在、白の手を選んでいる。それは前の黒の手よりも強い必要がある。
            # 黒の最良の選択に勝つ手が見つかると、すぐに探索を停止することができる。
            if outcome_for_black < best_black:                 # <9>
                return best_so_far                             # <9>
# end::alpha-beta-prune-2[]
# tag::alpha-beta-prune-3[]
        elif game_state.next_player == Player.black:
            # 黒の基準点を更新する
            if best_so_far > best_black:                       # <10>
                best_black = best_so_far                       # <10>


            # 現在、黒の手を選んでいる。それは前の黒の手よりも強い必要がある
            outcome_for_white = -1 * best_so_far               # <11>
            if outcome_for_white < best_white:                 # <11>
                return best_so_far                             # <11>
# end::alpha-beta-prune-3[]
# tag::alpha-beta-prune-4[]

    return best_so_far
# end::alpha-beta-prune-4[]


# tag::alpha-beta-agent[]
class AlphaBetaAgent(Agent):
    def __init__(self, max_depth, eval_fn):
        Agent.__init__(self)
        self.max_depth = max_depth
        self.eval_fn = eval_fn

    def select_move(self, game_state):
        best_moves = []
        best_score = None
        best_black = MIN_SCORE
        best_white = MIN_SCORE
        # Loop over all legal moves.
        for possible_move in game_state.legal_moves():
            # Calculate the game state if we select this move.
            next_state = game_state.apply_move(possible_move)
            # Since our opponent plays next, figure out their best
            # possible outcome from there.
            opponent_best_outcome = alpha_beta_result(
                next_state, self.max_depth,
                best_black, best_white,
                self.eval_fn)
            # Our outcome is the opposite of our opponent's outcome.
            our_best_outcome = -1 * opponent_best_outcome
            if (not best_moves) or our_best_outcome > best_score:
                # This is the best move so far.
                best_moves = [possible_move]
                best_score = our_best_outcome
                if game_state.next_player == Player.black:
                    best_black = best_score
                elif game_state.next_player == Player.white:
                    best_white = best_score
            elif our_best_outcome == best_score:
                # This is as good as our previous best move.
                best_moves.append(possible_move)
        # For variety, randomly select among all equally good moves.
        return random.choice(best_moves)
# end::alpha-beta-agent[]

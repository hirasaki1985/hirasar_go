# -*- coding: utf-8 -*-

import numpy as np
# tag::imports[]
import copy
from dlgo.gotypes import Player
# end::imports[]
from dlgo.gotypes import Point
from dlgo.scoring import compute_game_result

__all__ = [
    'Board',
    'GameState',
    'Move',
]


class IllegalMoveError(Exception):
    pass


# tag::strings[]
"""
石の連。同じ色の石でつながった石のグループ
"""
class GoString():  # <1>
    def __init__(self, color, stones, liberties):
        self.color = color              # 色
        self.stones = set(stones)       # {Point} 繋がっている石たち
        self.liberties = set(liberties) # {Point} 何も置いていない場所

    def remove_liberty(self, point):
        """
        呼吸点を削除する
        """
        self.liberties.remove(point)

    def add_liberty(self, point):
        """
        呼吸点を追加する
        """
        self.liberties.add(point)

    def merged_with(self, go_string):  # <2>
        """
        両方の連のすべての石を含む新しい連を返す
        """
        assert go_string.color == self.color
        combined_stones = self.stones | go_string.stones
        return GoString(
            self.color,
            combined_stones,
            (self.liberties | go_string.liberties) - combined_stones)

    @property
    def num_liberties(self):
        """
        呼吸点の数を返す
        """
        return len(self.liberties)

    def __eq__(self, other):
        return isinstance(other, GoString) and \
            self.color == other.color and \
            self.stones == other.stones and \
            self.liberties == other.liberties
# <1> Go strings are stones that are linked by a chain of connected stones of the same color.
# <2> Return a new Go string containing all stones in both strings.
# end::strings[]


"""
石を置くためのルールと取るためのルールを実装
"""
# tag::board_init[]
class Board():  # <1>
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {}

# <1> A board is initialized as empty grid with the specified number of rows and columns.
# end::board_init[]

# tag::board_place_0[]
    def place_stone(self, player, point):
        """
        Boardの石を置くメソッド
        """
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None
        adjacent_same_color = []        # 隣接した同じ色の石
        adjacent_opposite_color = []    # 隣接した違う色の石
        liberties = []                  # 何も置いていない石

        # この点の直接の隣を調べる
        for neighbor in point.neighbors():  # <1>
            if not self.is_on_grid(neighbor):
                continue

            # 隣接位置の連を取得
            neighbor_string = self._grid.get(neighbor)
            if neighbor_string is None:
                liberties.append(neighbor)
            elif neighbor_string.color == player:
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_string)
            else:
                if neighbor_string not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbor_string)
        new_string = GoString(player, [point], liberties)
# <1> First, we examine direct neighbors of this point.
# end::board_place_0[]
# tag::board_place_1[]

        # 同じ色の隣接する連をマージする
        for same_color_string in adjacent_same_color:  # <1>
            new_string = new_string.merged_with(same_color_string)
        for new_string_point in new_string.stones:
            self._grid[new_string_point] = new_string

        # 敵の色の隣接する連の呼吸点を減らす
        for other_color_string in adjacent_opposite_color:  # <2>
            other_color_string.remove_liberty(point)

        # 敵の色の連の呼吸点が０になっている場合は、それを取り除く
        for other_color_string in adjacent_opposite_color:  # <3>
            if other_color_string.num_liberties == 0:
                self._remove_string(other_color_string)
# <1> Merge any adjacent strings of the same color.
# <2> Reduce liberties of any adjacent strings of the opposite color.
# <3> If any opposite color strings now have zero liberties, remove them.
# end::board_place_1[]

# tag::board_remove[]
    def _remove_string(self, string):
        """
        連を取り除くと、他の連に対して呼吸点を作成できる
        """
        for point in string.stones:
            for neighbor in point.neighbors():  # <1>
                neighbor_string = self._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string is not string:
                    neighbor_string.add_liberty(point)
            self._grid[point] = None
# <1> Removing a string can create liberties for other strings.
# end::board_remove[]

# tag::board_utils[]
    def is_on_grid(self, point):
        """
        置こうとしている座標が盤上の範囲内か調べる
        """
        return 1 <= point.row <= self.num_rows and \
            1 <= point.col <= self.num_cols

    def get(self, point):  # <1>
        """
        盤上の点の内容を返す
        """
        string = self._grid.get(point)
        if string is None:
            return None
        return string.color

    def get_go_string(self, point):  # <2>
        """
        ある点における石の連全体を返す
        その点に石があればGoString, そうでない場合はNoneを返す
        """
        string = self._grid.get(point)
        if string is None:
            return None
        return string
# <1> Returns the content of a point on the board:  a Player if there is a stone on that point or else None.
# <2> Returns the entire string of stones at a point: a GoString if there is a stone on that point or else None.
# end::board_utils[]

    def __eq__(self, other):
        return isinstance(other, Board) and \
            self.num_rows == other.num_rows and \
            self.num_cols == other.num_cols and \
            self._grid == other._grid


# tag::moves[]
class Move():  # <1>
    def __init__(self, point=None, is_pass=False, is_resign=False):
        """
        プレイヤーが手番で取ることができるアクションは、is_play, is_pass, is_resignのいずれかになる
        """
        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def play(cls, point):  # <2>
        """
        この着手は盤上に石を置く
        """
        return Move(point=point)

    @classmethod
    def pass_turn(cls):  # <3>
        """
        この着手はパスする
        """
        return Move(is_pass=True)

    @classmethod
    def resign(cls):  # <4>
        """
        この着手は、現在のゲームを投了する
        """
        return Move(is_resign=True)
# <1> Any action a player can play on a turn, either is_play, is_pass or is_resign will be set.
# <2> This move places a stone on the board.
# <3> This move passes.
# <4> This move resigns the current game
# end::moves[]


"""
ゲーム状態を捉えて実際にゲームをプレイするクラス
"""
# tag::game_state[]
class GameState():
    def __init__(self, board, next_player, previous, move):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        self.last_move = move

    def apply_move(self, move):  # <1>
        """
        着手を適用した後、新しいGameStateを返す
        """
        if move.is_play:
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point)
        else:
            next_board = self.board
        return GameState(next_board, self.next_player.other, self, move)

    @classmethod
    def new_game(cls, board_size):
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        board = Board(*board_size)
        return GameState(board, Player.black, None, None)
# <1> Return the new GameState after applying the move.
# end::game_state[]

# tag::self_capture[]
    def is_move_self_capture(self, player, move):
        """
        自殺手のルールを強制する
        """
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        new_string = next_board.get_go_string(move.point)
        return new_string.num_liberties == 0
# end::self_capture[]

# tag::is_ko[]
    @property
    def situation(self):
        return (self.next_player, self.board)

    def does_move_violate_ko(self, player, move):
        """
        現在のゲーム状態はコウのルールに違反しているか？
        """
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        next_situation = (player.other, next_board)
        past_state = self.previous_state
        while past_state is not None:
            if past_state.situation == next_situation:
                return True
            past_state = past_state.previous_state
        return False
# end::is_ko[]

# tag::is_valid_move[]
    def is_valid_move(self, move):
        if self.is_over():
            return False
        if move.is_pass or move.is_resign:
            return True
        return (
            self.board.get(move.point) is None and
            not self.is_move_self_capture(self.next_player, move) and
            not self.does_move_violate_ko(self.next_player, move))
# end::is_valid_move[]

# tag::is_over[]
    def is_over(self):
        """
        終局しているか判定する
        """
        if self.last_move is None:
            return False
        if self.last_move.is_resign:
            return True
        second_last_move = self.previous_state.last_move
        if second_last_move is None:
            return False
        return self.last_move.is_pass and second_last_move.is_pass
# end::is_over[]

    def legal_moves(self):
        moves = []
        for row in range(1, self.board.num_rows + 1):
            for col in range(1, self.board.num_cols + 1):
                move = Move.play(Point(row, col))
                if self.is_valid_move(move):
                    moves.append(move)
        # These two moves are always legal.
        moves.append(Move.pass_turn())
        moves.append(Move.resign())

        return moves

    def winner(self):
        if not self.is_over():
            return None
        if self.last_move.is_resign:
            return self.next_player
        game_result = compute_game_result(self)
        return game_result.winner

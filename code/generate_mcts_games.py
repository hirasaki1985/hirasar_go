# -*- coding: utf-8 -*-

# tag::generate_mcts_imports[]
import argparse
import numpy as np

from dlgo.encoders import get_encoder_by_name
from dlgo import goboard_fast as goboard
from dlgo import mcts
from dlgo.utils import print_board, print_move
# end::generate_mcts_imports[]


# tag::generate_mcts[]
def generate_game(board_size, rounds, max_moves, temperature):
    # boardsにはエンコードされた盤の状態が格納され、movesにはエンコードされた着手が格納される
    boards, moves = [], []  # <1>

    # OnePlaneEncoderを指定された盤のサイズで初期化する
    encoder = get_encoder_by_name('oneplane', board_size)  # <2>

    # サイズboard_sizeの新しいゲームがインスタンス化される
    game = goboard.GameState.new_game(board_size)  # <3>

    # ラウンド数と温度が指定されたモンテカルロ木探索エージェントがボットになる
    bot = mcts.MCTSAgent(rounds, temperature)  # <4>

    num_moves = 0
    while not game.is_over():
        print_board(game.board)

        # 次の着手がボットによって選択される
        move = bot.select_move(game)  # <5>
        if move.is_play:
            # エンコードされた盤の状態がboardsに追加される
            boards.append(encoder.encode(game))  # <6>

            move_one_hot = np.zeros(encoder.num_points())
            move_one_hot[encoder.encode_point(move.point)] = 1

            # one-hotエンコードされた次の着手がmovesに追加される
            moves.append(move_one_hot)  # <7>

        print_move(game.next_player, move)

        # その後、ボットの着手が盤に適用される
        game = game.apply_move(move)  # <8>
        num_moves += 1

        # 最大手数に達していない限り、次の手番を続ける
        if num_moves > max_moves:  # <9>
            break

    return np.array(boards), np.array(moves)  # <10>

# <1> In `boards` we store encoded board state, `moves` is for encoded moves.
# <2> We initialize a OnePlaneEncoder by name with given board size.
# <3> An new game of size `board_size` is instantiated.
# <4> A Monte Carlo tree search agent with specified number of rounds and temperature will serve as our bot.
# <5> The next move is selected by the bot.
# <6> The encoded board situation is appended to `boards`.
# <7> The one-hot-encoded next move is appended to `moves`.
# <8> Afterwards the bot move is applied to the board.
# <9> We continue with the next move, unless the maximum number of moves has been reached.
# end::generate_mcts[]


# tag::generate_mcts_main[]
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--board-size', '-b', type=int, default=9)
    parser.add_argument('--rounds', '-r', type=int, default=1000)
    parser.add_argument('--temperature', '-t', type=float, default=0.8)
    parser.add_argument('--max-moves', '-m', type=int, default=60,
                        help='Max moves per game.')
    parser.add_argument('--num-games', '-n', type=int, default=10)
    parser.add_argument('--board-out')
    parser.add_argument('--move-out')

    # このアプリケーションは、コマンドライン引数でカスタマイズすることができる
    args = parser.parse_args()  # <1>
    xs = []
    ys = []

    for i in range(args.num_games):
        print('Generating game %d/%d...' % (i + 1, args.num_games))

        # 指定した数のゲームについて、ゲームデータを生成する
        x, y = generate_game(args.board_size, args.rounds, args.max_moves, args.temperature)  # <2>
        xs.append(x)
        ys.append(y)

    # すべてのゲームが生成されたら、それぞれの特徴量とラベルを連結する
    x = np.concatenate(xs)  # <3>
    y = np.concatenate(ys)

    # 特徴量とラベルのデータをコマンドラインオプションで指定された別々のファイルに保存する
    np.save(args.board_out, x)  # <4>
    np.save(args.move_out, y)


if __name__ == '__main__':
    main()

# <1> This application allows some customization via command line arguments.
# <2> For the specified number of games we generate game data.
# <3> After all games have been generated, we concatenate features and labels, respectively.
# <4> We store feature and label data to separate files, as specified by the command line options.
# end::generate_mcts_main[]

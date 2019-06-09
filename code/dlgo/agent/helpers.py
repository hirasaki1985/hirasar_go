# -*- coding: utf-8 -*-

# tag::helpersimport[]
from dlgo.gotypes import Point
# end::helpersimport[]

__all__ = [
    'is_point_an_eye',
]


# tag::eye[]
def is_point_an_eye(board, point, color):
    """
    盤上の指定された点は眼か？
    """

    # 空の眼の点
    if board.get(point) is not None:  # <1>
        return False

    # 隣接する全ての点には味方の石が含まれている必要がある
    for neighbor in point.neighbors():  # <2>
        if board.is_on_grid(neighbor):
            neighbor_color = board.get(neighbor)
            if neighbor_color != color:
                return False

    # 点が盤の中央にある場合、４つの角のうち３つの角を支配する必要がある。
    # 辺では全ての角を支配する必要がある
    friendly_corners = 0  # <3>
    off_board_corners = 0
    corners = [
        Point(point.row - 1, point.col - 1),
        Point(point.row - 1, point.col + 1),
        Point(point.row + 1, point.col - 1),
        Point(point.row + 1, point.col + 1),
    ]
    for corner in corners:
        if board.is_on_grid(corner):
            corner_color = board.get(corner)
            if corner_color == color:
                friendly_corners += 1
        else:
            off_board_corners += 1
    if off_board_corners > 0:
        # 点が角または辺にある
        return off_board_corners + friendly_corners == 4  # <4>

    # 点は中央にある
    return friendly_corners >= 3  # <5>

# <1> An eye is an empty point.
# <2> All adjacent points must contain friendly stones.
# <3> We must control 3 out of 4 corners if the point is in the middle of the board; on the edge we must control all corners.
# <4> Point is on the edge or corner.
# <5> Point is in the middle.
# end::eye[]

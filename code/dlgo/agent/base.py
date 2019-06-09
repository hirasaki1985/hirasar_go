# -*- coding: utf-8 -*-

__all__ = [
    'Agent',
]


# tag::agent[]
class Agent:
    def __init__(self):
        pass

    def select_move(self, game_state):
        raise NotImplementedError()
# end::agent[]

    def diagnostics(self):
        return {}

import tetris
from tetris import MinoType
from termcolor import colored
import random
from states import STZ_STATES
from dataclasses import dataclass
from typing import List

LJO_INDETERMINATE_ORDER = 'LJO_INDETERMINATE_ORDER'

@dataclass
class LjoState:
    order: List[str]
    placed: List[str]

def main():
    game = tetris.BaseGame(seed=14, board_size=(100,10))
    game.x_sonic_drop = lambda: x_sonic_drop(game)

    player = ForeverPlayer(game)

    rendered = False
    try:
        for _ in range(28):
            player.handle_one_piece()
    except:
        rendered = True
        print('Queue:', game.queue)
        print('Hold:', game.hold)
        render(game)
        raise

    if not rendered:
        print('Queue:', game.queue)
        print('Hold:', game.hold)
        render(game)

class ForeverPlayer:
    def __init__(self, game):
        self.game = game
        self.phase = 'main'
        self.stz_state = (0, 0)
        self.ljo_state = LJO_INDETERMINATE_ORDER
        self.i_state = -1

    def handle_one_piece(self):
        game = self.game
        piece = game.piece
        phase = 'main'  # 'main' | 'rebalance'
        if phase == 'main':
            if piece.type == MinoType.I:
                game.rotate(self.i_state)
                game.hard_drop()
                self.i_state = self._other_i_state()
            elif piece.type in [MinoType.L, MinoType.O, MinoType.J]:
                piece_type = {
                    MinoType.L: 'L',
                    MinoType.J: 'J',
                    MinoType.O: 'O',
                }[piece.type]
                self.handle_one_piece_main_ljo(piece_type)
            elif piece.type in [MinoType.S, MinoType.T, MinoType.Z]:
                piece_type = {
                    MinoType.S: 'S',
                    MinoType.T: 'T',
                    MinoType.Z: 'Z',
                }[piece.type]
                transitions = STZ_STATES[self.stz_state]
                if piece_type in transitions:
                    next_state = transitions[piece_type]
                    self.handle_one_piece_main_stz(piece_type)
                    self.stz_state = next_state
                else:
                    game.swap()
                    self.handle_one_piece()
            else:
                raise Exception('Not implemented')
        else:
            raise Exception('Not implemented')

    def _other_i_state(self):
        assert self.i_state in [-1, 1]
        if self.i_state == -1:
            return 1
        else:
            return -1

    def handle_one_piece_main_ljo(self, piece_type):
        game = self.game
        if self.ljo_state == LJO_INDETERMINATE_ORDER:
            order = self._determine_ljo_order(piece_type)
            self.ljo_state = LjoState(order, [])

        # Would it be cleaner to invert this hierarchy? (Instead of "if len" on the outside then "if
        # order" on the inside", "if order" on the outside" then "if len" on the inside)
        ljo_state = self.ljo_state
        if len(ljo_state.placed) == 0:
            # O first cases
            if ljo_state.order[0] == 'O':
                game.right(99)
                game.left()
                game.hard_drop()

            # O last cases
            elif ljo_state.order == [*'JLO']:
                game.rotate(-1)
                game.right(99)
                game.hard_drop()
            elif ljo_state.order == [*'LJO']:
                game.rotate(1)
                game.right(2)
                game.hard_drop()

            # O middle cases
            elif ljo_state.order == [*'JOL']:
                game.rotate(1)
                game.right(2)
                game.hard_drop()
            elif ljo_state.order == [*'LOJ']:
                game.rotate(-1)
                game.right(99)
                game.hard_drop()

            else:
                assert False

            self.ljo_state.placed.append(piece_type)

        elif len(ljo_state.placed) == 1:
            # O first cases
            if ljo_state.order == [*'OJL']:
                game.rotate(1)
                game.right(2)
                game.hard_drop()
            elif ljo_state.order == [*'OLJ']:
                game.rotate(-1)
                game.right(99)
                game.hard_drop()

            # O last cases
            elif ljo_state.order == [*'JLO']:
                game.rotate(1)
                game.right(2)
                game.hard_drop()
            elif ljo_state.order == [*'LJO']:
                game.rotate(-1)
                game.right(99)
                game.hard_drop()

            # O middle cases
            elif ljo_state.order == [*'JOL']:
                game.right(99)
                game.x_sonic_drop()
                game.left()
                game.hard_drop()
            elif ljo_state.order == [*'LOJ']:
                game.right(2)
                game.x_sonic_drop()
                game.right()
                game.hard_drop()

            else:
                assert False

            self.ljo_state.placed.append(piece_type)

        elif len(ljo_state.placed) == 2:
            # O first cases
            if ljo_state.order == [*'OJL']:
                game.rotate(-1)
                game.right(99)
                game.hard_drop()
            elif ljo_state.order == [*'OLJ']:
                game.rotate(1)
                game.right(2)
                game.hard_drop()

            # O last cases
            elif ljo_state.order == [*'JLO']:
                game.right(99)
                game.left()
                game.hard_drop()
            elif ljo_state.order == [*'LJO']:
                game.right(99)
                game.left()
                game.hard_drop()

            # O middle cases
            elif ljo_state.order == [*'JOL']:
                game.rotate(-1)
                game.right(99)
                game.hard_drop()
            elif ljo_state.order == [*'LOJ']:
                game.rotate(1)
                game.right(2)
                game.hard_drop()

            else:
                assert False

            self.ljo_state = LJO_INDETERMINATE_ORDER
        else:
            assert False


    def _determine_ljo_order(self, piece_type):
        order = []
        ljo_remaining = ['L', 'J', 'O']

        # First item in `order`
        order.append(piece_type)
        ljo_remaining.remove(piece_type)

        queue = [piece_type_to_str(item) for item in get_limited_queue(self.game)]
        first_ljo_in_queue = [item for item in queue if item in 'LJO'][0]

        # Second item in `order`
        order.append(first_ljo_in_queue)
        ljo_remaining.remove(first_ljo_in_queue)

        # Last item in `order`
        order.append(ljo_remaining[0])

        return order

    def handle_one_piece_main_stz(self, piece_type):
        game = self.game
        stz_state = self.stz_state

        if stz_state == (0, 0):
            if piece_type == 'S':
                game.rotate(-1)
                game.left()
                game.hard_drop()
            elif piece_type == 'T':
                raise Exception('TODO')
            else:
                assert False

        elif stz_state == (1, 0):
            if piece_type == 'Z':
                raise Exception('TODO')
            elif piece_type == 'S':
                raise Exception('TODO')
            else:
                assert False
        elif stz_state == (1, 1):
            if piece_type == 'T':
                game.rotate(1)
                game.left(99)
                game.x_sonic_drop()
                game.rotate(-1)
                game.hard_drop()
            elif piece_type == 'S':
                raise Exception('TODO')
            else:
                assert False

        elif stz_state == (2, 0):
            if piece_type == 'Z':
                raise Exception('TODO')
            elif piece_type == 'S':
                raise Exception('TODO')
            else:
                assert False
        elif stz_state == (2, 1):
            if piece_type == 'Z':
                game.rotate(-1)
                game.left(99)
                game.hard_drop()
            elif piece_type == 'S':
                raise Exception('TODO')
            else:
                assert False
        elif stz_state == (2, 2):
            if piece_type == 'T':
                raise Exception('TODO')
            else:
                assert False

        elif stz_state == (3, 0):
            if piece_type == 'T':
                raise Exception('TODO')
            elif piece_type == 'S':
                raise Exception('TODO')
            else:
                assert False
        elif stz_state == (3, 1):
            if piece_type == 'Z':
                raise Exception('TODO')
            elif piece_type == 'S':
                game.rotate(-1)
                game.left()
                game.hard_drop()
            else:
                assert False
        elif stz_state == (3, 2):
            if piece_type == 'Z':
                raise Exception('TODO')
            elif piece_type == 'T':
                raise Exception('TODO')
            else:
                assert False

        elif stz_state == (4, 0):
            if piece_type == 'S':
                raise Exception('TODO')
            else:
                assert False
        elif stz_state == (4, 1):
            if piece_type == 'T':
                raise Exception('TODO')
            elif piece_type == 'S':
                raise Exception('TODO')
            else:
                assert False
        elif stz_state == (4, 2):
            if piece_type == 'Z':
                game.rotate(-1)
                game.left(99)
                game.hard_drop()
            elif piece_type == 'T':
                raise Exception('TODO')
            else:
                assert False
        elif stz_state == (4, 3):
            if piece_type == 'Z':
                raise Exception('TODO')
            else:
                assert False
        elif stz_state == (4, 4):
            if piece_type == 'Z':
                raise Exception('TODO')
            elif piece_type == 'T':
                raise Exception('TODO')
            else:
                assert False

        elif stz_state == (5, 0):
            if piece_type == 'S':
                raise Exception('TODO')
            else:
                assert False
        elif stz_state == (5, 1):
            if piece_type == 'T':
                game.rotate(1)
                game.left(99)
                game.hard_drop()
            else:
                assert False
        elif stz_state == (5, 2):
            if piece_type == 'Z':
                raise Exception('TODO')
            else:
                assert False

        elif stz_state == (6, 0):
            if piece_type == 'S':
                game.rotate(-1)
                game.left(99)
                game.hard_drop()
            elif piece_type == 'T':
                raise Exception('TODO')
            else:
                assert False
        elif stz_state == (6, 1):
            if piece_type == 'T':
                raise Exception('TODO')
            elif piece_type == 'Z':
                raise Exception('TODO')
            else:
                assert False

        elif stz_state == (7, 0):
            if piece_type == 'S':
                raise Exception('TODO')
            elif piece_type == 'T':
                game.rotate(-1)
                game.left()
                game.hard_drop()
            else:
                assert False
        elif stz_state == (7, 1):
            if piece_type == 'S':
                raise Exception('TODO')
            elif piece_type == 'Z':
                raise Exception('TODO')
            else:
                assert False
        elif stz_state == (7, 2):
            if piece_type == 'T':
                raise Exception('TODO')
            elif piece_type == 'Z':
                raise Exception('TODO')
            else:
                assert False

        elif stz_state == (8, 0):
            if piece_type == 'T':
                raise Exception('TODO')
            else:
                assert False
        elif stz_state == (8, 1):
            if piece_type == 'S':
                raise Exception('TODO')
            elif piece_type == 'Z':
                game.rotate(-1)
                game.left()
                game.hard_drop()
            else:
                assert False
        elif stz_state == (8, 2):
            if piece_type == 'S':
                raise Exception('TODO')
            elif piece_type == 'Z':
                raise Exception('TODO')
            else:
                assert False
        elif stz_state == (8, 3):
            if piece_type == 'T':
                raise Exception('TODO')
            else:
                assert False

        elif stz_state == (9, 0):
            if piece_type == 'Z':
                raise Exception('TODO')
            else:
                assert False
        elif stz_state == (9, 1):
            if piece_type == 'Z':
                raise Exception('TODO')
            elif piece_type == 'S':
                game.rotate(-1)
                game.left(99)
                game.hard_drop()
            else:
                assert False
        elif stz_state == (9, 2):
            if piece_type == 'S':
                raise Exception('TODO')
            else:
                assert False

        elif stz_state == (10, 0):
            if piece_type == 'Z':
                game.rotate(-1)
                game.left()
                game.hard_drop()
            else:
                assert False
        elif stz_state == (10, 1):
            if piece_type == 'S':
                raise Exception('TODO')
            else:
                assert False

        elif stz_state == (11, 0):
            if piece_type == 'T':
                game.rotate(2)
                game.left(2)
                game.hard_drop()
            else:
                assert False
        else:
            raise Exception('TODO')

def x_sonic_drop(game):
    for _ in range(200):
        game.soft_drop()

def render(game):
    lines = (
        str(game.get_playfield())
            .replace('0', '.')
            .replace(']', ' ]')
            .replace('] ]', ']]')
            .replace('8 ', '[]')
            .replace('1 ', colored('[]', 'cyan'))
            .replace('2 ', colored('[]', 'blue'))
            .replace('3 ', colored('{}', 'yellow'))
            .replace('4 ', colored('[]', 'yellow'))
            .replace('5 ', colored('[]', 'green'))
            .replace('6 ', colored('[]', 'magenta'))
            .replace('7 ', colored('[]', 'red'))
            .splitlines()
            [-20:]
    )
    print(
        '\n'.join(lines)
    )

def piece_type_to_str(piece_type):
    s = repr(piece_type)
    assert s.startswith('PieceType.')
    return s[-1]

def get_limited_queue(game):
    # python-tetris shows the programmer the next 7 pieces in the queue, but many versions of Tetris
    # only show the next 5.
    return game.queue[:5]

main()

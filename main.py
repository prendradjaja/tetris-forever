import tetris
from tetris import MinoType
from termcolor import colored
import random
from states import STZ_STATES

def main():
    game = tetris.BaseGame(seed=14, board_size=(100,10))
    game.x_sonic_drop = lambda: x_sonic_drop(game)

    player = ForeverPlayer(game)

    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()
    player.handle_one_piece()

    print('Queue:', game.queue)
    print('Hold:', game.hold)

    render(game)

class ForeverPlayer:
    def __init__(self, game):
        self.game = game
        self.phase = 'main'
        self.stz_state = (0, 0)

    def handle_one_piece(self):
        game = self.game
        piece = game.piece
        phase = 'main'  # 'main' | 'rebalance'
        if phase == 'main':
            if piece.type == MinoType.I:
                game.rotate(random.choice([-1, 1]))
                game.hard_drop()
            elif piece.type in [MinoType.L, MinoType.O, MinoType.J]:
                game.right(99)
                game.hard_drop()
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
    for _ in range(99):
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

main()

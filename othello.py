import copy

from min_max import MinMax
from othello_utils import *


class Othello:
    def __init__(self):
        # Inicialización del tablero
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.board[3][3] = WHITE
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.board[4][4] = WHITE

    # Imprimir el tablero
    def print_board(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                print(self.board[i][j], end=" ")
            print()

    # Verificar si un movimiento es válido

    def play_test_min_max(self):
        min_max_black = MinMax(8, 10, False)
        min_max_white = MinMax(8, 10, True)
        current_player = BLACK
        while not is_game_over(self.board):
            player = "Black" if current_player == BLACK else "White"
            if current_player == WHITE:
                can_play, _, time_elapsed, nodes, row, col = min_max_white.run(self.board, current_player)
                if can_play:
                    print(f"\n\nCurrent player: {player}")
                    print(f"Board received")
                    self.print_board()
                    print('---------------')
                    make_move(self.board, row, col, current_player)
                    print(f"Board played -> Row: {row}, Col: {col}")
                    self.print_board()
                    current_player = get_opponent(current_player)
                else:
                    current_player = get_opponent(current_player)
            else:
                can_play, _, time_elapsed, nodes, row, col = min_max_black.run(self.board, current_player)
                if can_play:
                    print(f"\n\nCurrent player: {player}")
                    print(f"Board received")
                    self.print_board()
                    print('---------------')
                    make_move(self.board, row, col, current_player)
                    print(f"Board played -> Row: {row}, Col: {col}")
                    self.print_board()
                    current_player = get_opponent(current_player)
                else:
                    current_player = get_opponent(current_player)


if __name__ == '__main__':
    othello = Othello()
    othello.play_test_min_max()
    othello.print_board()

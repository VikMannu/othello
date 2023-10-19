import copy

BOARD_SIZE = 8

# Definir los posibles valores en el tablero
EMPTY = 0
WHITE = 1
BLACK = 2


def get_opponent(player):
    return WHITE if player == BLACK else BLACK


def is_valid_move(board, row, col, player):
    if board[row][col] != EMPTY:
        return False

    opponent = get_opponent(player)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for dr, dc in directions:
        r, c = row, col
        r += dr
        c += dc
        found_opponent = False

        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
            if board[r][c] == player:
                if found_opponent:
                    return True
                break
            elif board[r][c] == EMPTY:
                break
            elif board[r][c] == opponent:
                found_opponent = True
            r += dr
            c += dc

    return False


def find_valid_moves(board, player):
    valid_moves = []
    opponent = get_opponent(player)

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == EMPTY:
                directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
                is_valid = False

                for dr, dc in directions:
                    r, c = row, col
                    r += dr
                    c += dc
                    found_opponent = False

                    while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                        if board[r][c] == player:
                            if found_opponent:
                                is_valid = True
                                break
                            break
                        elif board[r][c] == EMPTY:
                            break
                        elif board[r][c] == opponent:
                            found_opponent = True
                        r += dr
                        c += dc

                    if is_valid:
                        valid_moves.append((row, col))
                        break

    return valid_moves


def can_play(board, player):
    valid_moves = find_valid_moves(board, player)
    return len(valid_moves) > 0


def is_game_over(board):
    return not (can_play(board, BLACK) or can_play(board, WHITE))


# Realizar un movimiento y voltear fichas del oponente
def make_move(board, row, col, player):
    if not is_valid_move(board, row, col, player):
        return False

    opponent = get_opponent(player)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for dr, dc in directions:
        r, c = row, col
        r += dr
        c += dc
        found_opponent = False

        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
            if board[r][c] == player:
                if found_opponent:
                    while r != row or c != col:
                        r -= dr
                        c -= dc
                        board[r][c] = player
                break
            elif board[r][c] == EMPTY:
                break
            elif board[r][c] == opponent:
                found_opponent = True
            r += dr
            c += dc

    board[row][col] = player
    return True


# Imprimir el tablero
def print_board(board):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            print(board[i][j], end=" ")
        print()


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


if __name__ == '__main__':
    othello = Othello()
    othello.print_board()
    print(is_valid_move(othello.board, 2, 4, BLACK))
    movements = find_valid_moves(othello.board, WHITE)
    print(find_valid_moves(othello.board, WHITE))

    for row, col in movements:
        new_board = copy.deepcopy(othello.board)
        print(f"Row: {row}, Col: {col}")
        print(make_move(new_board, row, col, WHITE))
        print_board(othello.board)

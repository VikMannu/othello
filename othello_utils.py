BOARD_SIZE = 8

# Definir los posibles valores en el tablero
EMPTY = '-'
WHITE = 'W'
BLACK = 'B'


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


def check_winner(board):
    # Count the number of pieces of each color on the board
    white_pieces = sum([row.count(WHITE) for row in board])
    black_pieces = sum([row.count(BLACK) for row in board])

    # Determine the winner
    if white_pieces > black_pieces:
        return "White"
    elif black_pieces > white_pieces:
        return "Black"
    else:
        return "Draw"


# Imprimir el tablero
def print_board(board):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            print(board[i][j], end=" ")
        print()

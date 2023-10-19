import time
import copy

from othello_utils import *


class MinMax:
    def __init__(self, cutting_level, max_cutting_time, is_alpha_beta):
        self.cutting_level = cutting_level
        self.max_cutting_time = max_cutting_time
        self.is_alpha_beta = is_alpha_beta
        self.position_weight = [
            [100, -20, 10, 5, 5, 10, -20, 100],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [10, -2, 2, 1, 1, 2, -2, 10],
            [5, -2, 1, 1, 1, 1, -2, 5],
            [5, -2, 1, 1, 1, 1, -2, 5],
            [10, -2, 2, 1, 1, 2, -2, 10],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [100, -20, 10, 5, 5, 10, -20, 100]
        ]
        self.nodes = 0
        self.start_time = 0

    def calculate_weight_difference(self, board, player):
        opponent = get_opponent(player)

        player_weight = 0
        opponent_weight = 0

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] == player:
                    player_weight += self.position_weight[row][col]
                if board[row][col] == opponent:
                    opponent_weight += self.position_weight[row][col]

        return player_weight - opponent_weight

    def max_value(self, level, board, player, alpha, beta):
        movements = find_valid_moves(board, player)
        time_remaining = time.time() - self.start_time
        if level == 0 or len(movements) == 0 or time_remaining > self.max_cutting_time:
            self.nodes += 1
            return self.calculate_weight_difference(board, player), None, None

        best_weight = float("-inf")
        best_move = None

        for row, col in movements:
            new_board = copy.deepcopy(board)
            if make_move(new_board, row, col, player):
                # Llamar recursivamente a la función min_value con el nuevo estado del tablero
                weight, _, _ = self.min_value(level - 1, new_board, get_opponent(player), alpha, beta)

                if weight > best_weight:
                    best_weight = weight
                    best_move = (row, col)

                if self.is_alpha_beta:
                    alpha = max(alpha, best_weight)
                    if alpha >= beta:
                        break  # Poda alfa-beta

        return best_weight, best_move[0], best_move[1]

    def min_value(self, level, board, player, alpha, beta):
        movements = find_valid_moves(board, player)
        time_remaining = time.time() - self.start_time
        if level == 0 or not movements or time_remaining > self.max_cutting_time:
            self.nodes += 1
            return self.calculate_weight_difference(board, player), None, None  # Devolver peso y None para row y col

        best_weight = float("inf")
        best_move = None

        for row, col in movements:
            new_board = copy.deepcopy(board)
            if make_move(new_board, row, col, player):
                # Llamar recursivamente a la función max_value con el nuevo estado del tablero
                weight, _, _ = self.max_value(level - 1, new_board, get_opponent(player), alpha, beta)

                if weight < best_weight:
                    best_weight = weight
                    best_move = (row, col)

                if self.is_alpha_beta:
                    beta = min(beta, best_weight)
                    if beta <= alpha:
                        break  # Poda alfa-beta

        return best_weight, best_move[0], best_move[1]

    def run(self, board, player):
        self.nodes = 0
        self.start_time = time.time()
        weight, row, col = self.max_value(self.cutting_level, board, player, float("-inf"), float("inf"))
        end_time = time.time()

        if row is None or col is None:
            return False, True, end_time - self.start_time, self.nodes, row, col
        else:
            return True, True, end_time - self.start_time, self.nodes, row, col


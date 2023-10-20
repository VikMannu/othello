import ast
import os
import time

import numpy as np
import random
from othello import *
from othello_utils import *

# Definición de constantes
NUM_EPISODES = 1000
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.9
EPSILON = 0.1
gan_black = 0
gan_white = 0
position_weight = [
    [100, -20, 10, 5, 5, 10, -20, 100],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [10, -2, 2, 1, 1, 2, -2, 10],
    [5, -2, 1, 1, 1, 1, -2, 5],
    [5, -2, 1, 1, 1, 1, -2, 5],
    [10, -2, 2, 1, 1, 2, -2, 10],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [100, -20, 10, 5, 5, 10, -20, 100]
]
# Inicialización de la tabla Q
Q = np.zeros((BOARD_SIZE, BOARD_SIZE, BOARD_SIZE, BOARD_SIZE, 3))


# Función para elegir una acción (movimiento) con base en la política epsilon-greedy
def choose_action(board, state, epsilon, player):
    if np.random.rand() < epsilon:
        return random_valid_move(board, player)
    else:
        numeric_matrix = [[1 if char == WHITE else 2 if char == BLACK else 0 for char in row] for row in state]
        candidate = np.unravel_index(np.argmax(Q[numeric_matrix], axis=None), Q[numeric_matrix].shape)
        if not is_valid_move(board, candidate[0], candidate[1], player):
            return random_valid_move(board, player)
        # print("USO CANDIDATO")
        return candidate


# Función para obtener una jugada válida aleatoria
def random_valid_move(board, player):
    valid_moves = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if is_valid_move(board, r, c, player)]
    return None if len(valid_moves) == 0 else random.choice(valid_moves)


# Función para evaluar el tablero
def evaluate_board(board, player):
    opponent = get_opponent(player)
    player_weight = 0
    opponent_weight = 0
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == player:
                player_weight += position_weight[row][col]
            if board[row][col] == opponent:
                opponent_weight += position_weight[row][col]
    return player_weight - opponent_weight


# Función para actualizar la tabla Q
def update_Q(Q, state, action, reward, next_state):
    numeric_matrix = np.array([[1 if char == WHITE else 2 if char == BLACK else 0 for char in row] for row in state])
    numeric_matrix_next = np.array(
        [[1 if char == WHITE else 2 if char == BLACK else 0 for char in row] for row in next_state])

    disc = np.multiply(DISCOUNT_FACTOR, np.max(Q[numeric_matrix_next]))
    subs = np.subtract(disc, Q[numeric_matrix][action])
    suma = np.add(reward, subs)
    lr = np.multiply(LEARNING_RATE, suma)
    jiji = np.add(Q[numeric_matrix][action], lr)
    Q[numeric_matrix][action] = np.add(Q[numeric_matrix][action], lr)
    # print(LEARNING_RATE," REWARD: ",  reward, "DISCOUNT:", DISCOUNT_FACTOR, "npMax: ", np.max(Q[numeric_matrix_next]))
    # print("Suma np:",jiji.shape)

    m = Q[numeric_matrix][action]
    # print(m.shape)


# Función para entrenar al agente
def train_agent():
    loadLearningTable()
    # division de epocas
    for episode in range(NUM_EPISODES):

        othello = Othello()
        board = othello.board
        state = np.copy(board)
        player = BLACK  # El jugador negro comienza
        done = False
        while not done:
            next_player = get_opponent(player)
            if can_play(board, player):
                action = choose_action(board, state, EPSILON, player)
                make_move(board, action[0], action[1], player)
                next_state = board

                reward = evaluate_board(next_state, player)

                update_Q(Q, state, action, reward, next_state)
                state = next_state
                # print("Juega ", player, "Pos ", action[0], "-", action[1])
            done = is_game_over(board)
            player = next_player
        saveLearningTable()
        print("Gana", check_winner(board))


def loadLearningTable():
    if not os.path.exists('tabla_Q.txt'):
        return
    f = open('tabla_Q.txt', 'r')
    if f.mode == 'r':
        contents = f.read()
    Q = contents


def saveLearningTable():
    file1 = open("tabla_Q.txt", "w")
    str1 = repr(Q)
    file1.write(str1)
    file1.close()


# Lógica para jugar una partida contra el agente
def train_min_max():
    global gan_white
    global gan_black
    loadLearningTable()
    for episode in range(NUM_EPISODES):
        othello = Othello()
        board = othello.board
        state = np.copy(board)
        player = BLACK
        min_max_white = MinMax(2, 50, True)
        while True:
            # print("Estado actual del tablero:")
            # print_board(board)
            if can_play(board, player):
                if player == BLACK:
                    coord = choose_action(board, state, EPSILON, player)
                    row = coord[0]
                    col = coord[1]
                    next_state = board
                    reward = evaluate_board(next_state, player)
                    update_Q(Q, state, coord, reward, next_state)
                    state = next_state
                    # print(f"El agente juega en ({row + 1}, {col + 1})")
                else:
                    # print("Turno del oponente (humano o simulado)", player)
                    _, _, _, _, row, col = min_max_white.run(board, player)

                make_move(board, row, col, player)
            player = get_opponent(player)

            if is_game_over(board):
                # print("El juego ha terminado.")
                break
        print("Gana", check_winner(board))
        if check_winner(board) == "Black":
            gan_black += 1
        elif check_winner(board) == "White":
            gan_white += 1
        saveLearningTable()

    print("Estadishticas: \nBlack", gan_black, "\nWhite", gan_white)


if __name__ == "__main__":
    print("Iniciando entrenamiento...")
    train_agent()
    print("El juego ha iniciado...")
    train_min_max()

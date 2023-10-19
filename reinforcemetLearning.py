import os
import time

import numpy as np
import random
from othello import *
from othello_utils import *

# Definición de constantes
NUM_EPISODES = 100
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.9
EPSILON = 0.1

# Inicialización de la tabla Q
Q = np.zeros((BOARD_SIZE, BOARD_SIZE, BOARD_SIZE, BOARD_SIZE, 3))


# Función para elegir una acción (movimiento) con base en la política epsilon-greedy
def choose_action(board, state, epsilon, player):
    if np.random.rand() < epsilon:
        return random_valid_move(board, player)
    else:
        numeric_matrix = [[1 if char == 'W' else 2 if char == 'B' else 0 for char in row] for row in state]
        candidate = np.unravel_index(np.argmax(Q[numeric_matrix], axis=None), Q[numeric_matrix].shape)
        if not is_valid_move(board, candidate[0], candidate[1], player):
            return random_valid_move(board, player)
        #print("USO CANDIDATO")
        return candidate


# Función para obtener una jugada válida aleatoria
def random_valid_move(board, player):
    valid_moves = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if is_valid_move(board, r, c, player)]
    return None if len(valid_moves) == 0 else random.choice(valid_moves)


# Función para evaluar el tablero
def evaluate_board(board, player):
    player_count = np.sum(board == player)
    opponent = get_opponent(player)
    opponent_count = np.sum(board == opponent)
    return player_count - opponent_count


# Función para actualizar la tabla Q
def update_Q(state, action, reward, next_state):
    numeric_matrix = [[1 if char == 'W' else 2 if char == 'B' else 0 for char in row] for row in state]
    numeric_matrix_next = [[1 if char == 'W' else 2 if char == 'B' else 0 for char in row] for row in next_state]

    Q[numeric_matrix][action] = Q[numeric_matrix][action] + LEARNING_RATE * (
            reward + DISCOUNT_FACTOR * np.max(Q[numeric_matrix_next]) - Q[numeric_matrix][action])


# Función para entrenar al agente
def train_agent():
    #division de epocas
    for episode in range(NUM_EPISODES):
        othello = Othello()
        board=othello.board
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
                update_Q(state, action, reward, next_state)
                state = next_state
                #print("Juega ", player, "Pos ", action[0], "-", action[1])
            done = is_game_over(board)
            player = next_player
        #print("Gana", check_winner(board))

# Lógica para jugar una partida contra el agente
def play_game():
    othello = Othello()
    board=othello.board
    state = np.copy(board)
    player = BLACK
    min_max_white = MinMax(2, 50, True)
    while True:
        print("Estado actual del tablero:")
        print_board(board)
        if can_play(board, player):
            if player == BLACK:
                coord = choose_action(board, state, EPSILON, player)
                row = coord[0]
                col = coord[1]
                next_state = board
                reward = evaluate_board(next_state, player)
                update_Q(state, coord, reward, next_state)
                state = next_state
                print(f"El agente juega en ({row + 1}, {col + 1})")
            else:
                print("Turno del oponente (humano o simulado)", player)
                _, _, _, _, row, col = min_max_white.run(board, player)
            make_move(board, row, col, player)
        player = get_opponent(player)

        if is_game_over(board):
            print("El juego ha terminado.")
            break
    print("Gana", check_winner(board))

if __name__ == "__main__":

    train_agent()
    print("El juego ha iniciado.")
    play_game()

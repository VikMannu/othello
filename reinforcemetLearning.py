import numpy as np
import random

# Tamaño del tablero
BOARD_SIZE = 8

# Definir los posibles valores en el tablero
EMPTY = 0
WHITE = 1
BLACK = 2

# Inicialización del tablero
board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
board[3][3] = 2
board[4][4] = 2
board[3][4] = 1
board[4][3] = 1
# Definición de constantes
NUM_EPISODES = 10
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.9
EPSILON = 0.1

# Inicialización de la tabla Q
Q = np.zeros((BOARD_SIZE, BOARD_SIZE, BOARD_SIZE, BOARD_SIZE, 3))


# Función para elegir una acción (movimiento) con base en la política epsilon-greedy
def choose_action(state, epsilon):
    if np.random.rand() < epsilon:
        return random_valid_move(state)
    else:
        candidate=np.unravel_index(np.argmax(Q[state], axis=None), Q[state].shape)
        if not is_valid_move(board, state, candidate[0], candidate[1]):
            return random_valid_move(state)
        return candidate


# Función para obtener una jugada válida aleatoria
def random_valid_move(state):
    valid_moves = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if is_valid_move(board, state, r, c)]
    return random.choice(valid_moves)


# Función para verificar si una jugada es válida
def is_valid_move(board, state, row, col):
    if state[row, col] != EMPTY:
        return False

    player = BLACK if np.sum(state == BLACK) == np.sum(state == WHITE) else WHITE
    opponent = WHITE if player == BLACK else BLACK

    # Comprobar en todas las direcciones si hay una ficha del oponente alrededor
    for dr in [-1, 0, 1]: # tuplas sumadoras de posiciones
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            r, c = row + dr, col + dc #obtenemos las direcciones a iterar
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and state[r, c] == opponent:
                r += dr #suma posiciones mientras encontremos oponentes en esa direccion
                c += dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and state[r, c] == player: #encontramos a su pareja en el
                    #otro extremo
                    return True
    return False


# Función para evaluar el tablero
def evaluate_board(board, player):
    player_count = np.sum(board == player)
    opponent = WHITE if player == BLACK else BLACK
    opponent_count = np.sum(board == opponent)
    return player_count - opponent_count


# Función para verificar si hay movimientos válidos para un jugador
def has_valid_moves(board, player):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if is_valid_move(board, board, row, col):
                return True
    return False


# Función para realizar una jugada
def make_move(board, state, row, col, player):
    if not is_valid_move(board, state, row, col):
        return state, player

    # Realizar la jugada
    board[row, col] = player
    opponent = BLACK if player == WHITE else WHITE
    # Voltear las fichas del oponente en todas las direcciones
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            r, c = row + dr, col + dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r, c] == opponent:
                r += dr
                c += dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r, c] == player:
                    r, c = row + dr, col + dc
                    while board[r, c] == opponent:
                        board[r, c] = player
                        r += dr
                        c += dc
    # Cambiar el turno al siguiente jugador
    next_player = WHITE if player == BLACK else BLACK
    return board, next_player

# Función para actualizar la tabla Q
def update_Q(state, action, reward, next_state):
    Q[state][action] = Q[state][action] + LEARNING_RATE * (
            reward + DISCOUNT_FACTOR * np.max(Q[next_state]) - Q[state][action])
    print("Q actualizado a ", LEARNING_RATE * (
            reward + DISCOUNT_FACTOR * np.max(Q[next_state]) - Q[state][action]))


# Función para entrenar al agente
def train_agent():
    for episode in range(NUM_EPISODES):
        state = np.copy(board)
        player = BLACK  # El jugador negro comienza
        done = False
        print(state)
        while not done:
            print(state)
            action = choose_action(state, EPSILON)
            next_state, next_player = make_move(np.copy(state), state, action[0], action[1], player)
            reward = evaluate_board(next_state, player)
            update_Q(state, action, reward, next_state)
            state = next_state
            player = next_player
            done = not has_valid_moves(state, player)

# Lógica para jugar una partida contra el agente
def play_game():
    state = np.copy(board)
    player = BLACK

    while True:
        print("Estado actual del tablero:")
        print(state)
        if player == BLACK:
            opponent = WHITE
            coord = choose_action(state, EPSILON)
            row= coord[0]
            col= coord[1]
            print(f"El agente juega en ({row+1}, {col+1})")
        else:
            print("Turno del oponente (humano o simulado). Ingresa tu jugada (fila columna): ", player)
            row, col = map(int, input().split())
            row-=1; col-=1
            opponent = BLACK
            while not is_valid_move(board, state, row, col):
                print("Posicion invalida. Ingresa tu jugada de nuevo (fila columna): ", player)
                row, col = map(int, input().split())

        state, player = make_move(state, state, row, col, player)

        if not has_valid_moves(state, player) and not has_valid_moves(state, opponent):
            print("El juego ha terminado.")
            break
        player = opponent

if __name__ == "__main__":
    train_agent()
    print("El juego ha iniciado.")
    print(board)
    play_game()

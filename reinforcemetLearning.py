import numpy as np

# Definición de constantes
BOARD_SIZE = 8
NUM_EPISODES = 1000
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.9
EPSILON = 0.1

# Inicialización de la tabla Q
Q = np.zeros((BOARD_SIZE, BOARD_SIZE, BOARD_SIZE, BOARD_SIZE, 3))

# Función para elegir una acción (movimiento) con base en la política epsilon-greedy
def choose_action(state, epsilon):
    if np.random.rand() < epsilon:
        return np.unravel_index(np.argmax(Q[state], axis=None), Q[state].shape)
    else:
        return np.random.randint(0, BOARD_SIZE, size=2)

# Función para actualizar la tabla Q
def update_Q(state, action, reward, next_state):
    Q[state][action] = Q[state][action] + LEARNING_RATE * (reward + DISCOUNT_FACTOR * np.max(Q[next_state]) - Q[state][action])

# Función para jugar un episodio
def play_episode():
    state = (np.zeros((BOARD_SIZE, BOARD_SIZE)), np.zeros((BOARD_SIZE, BOARD_SIZE)), 0)
    for _ in range(BOARD_SIZE ** 2 // 2):  # Se juega la mitad del tablero
        row, col = choose_action(state, EPSILON)
        # Simula el juego: actualiza el estado
        # Aquí deberías implementar la lógica del juego Othello y actualizar el estado adecuadamente
        next_state = state  # Cambia esto con la lógica real del juego
        reward = 0  # Define cómo se calcula la recompensa
        update_Q(state, (row, col), reward, next_state)
        state = next_state

# Entrenamiento del agente
for episode in range(NUM_EPISODES):
    play_episode()
    if (episode + 1) % 100 == 0:
        print(f"Episodio {episode + 1}/{NUM_EPISODES} completado.")


##################################################################################################################
#heuristicas
##################################################################################################################
# Función para evaluar una jugada utilizando una heurística simple
def evaluate_move(board, row, col, player):
    if board[row, col] != EMPTY:
        return -np.inf  # La casilla ya está ocupada

    opponent = BLACK if player == WHITE else WHITE

    # Valorar la jugada
    value = 0

    # Puntaje para el centro del tablero
    if row in [2, 3, 4, 5] and col in [2, 3, 4, 5]:
        value += 2

    # Puntaje por ocupar las esquinas
    if (row, col) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
        value += 5

    # Puntaje por ocupar bordes (sin esquinas)
    if row in [0, 7] and col in [1, 2, 3, 4, 5, 6]:
        value += 3
    if col in [0, 7] and row in [1, 2, 3, 4, 5, 6]:
        value += 3

    # Puntaje por capturar fichas del oponente
	for dr in [-1, 0, 1]:
			for dc in [-1, 0, 1]:
				if dr == 0 and dc == 0:
					continue
				r, c = row + dr, col + dc
				count = 0
				while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r, c] == opponent:
					r += dr
					c += dc
					count += 1
					if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r, c] == player:
						value += count

	return value

	# Ejemplo de uso de la heurística para evaluar jugadas válidas
	valid_moves = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if evaluate_move(board, r, c, BLACK) != -np.inf]

	for move in valid_moves:
		row, col = move
		evaluation = evaluate_move(board, row, col, BLACK)
		print(f"Jugada en ({row}, {col}) - Evaluación: {evaluation}")



##################################################################################################################
############################################OTHELLO################################################################
##################################################################################################################
# Tamaño del tablero
BOARD_SIZE = 8

# Definir los posibles valores en el tablero
EMPTY = 0
WHITE = 1
BLACK = 2

# Inicialización del tablero
board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
board[3:5, 3:5] = WHITE
board[3:5, 4:6] = BLACK
player_turn = WHITE  # Empieza el jugador blanco

# Función para imprimir el tablero
def print_board(board):
    for row in board:
        row_str = [str(cell) if cell != EMPTY else '.' for cell in row]
        print(" ".join(row_str))
    print()

# Función para verificar si una jugada es válida
def is_valid_move(board, row, col, player):
    if board[row, col] != EMPTY:
        return False

    opponent = BLACK if player == WHITE else WHITE

    # Comprobar en todas las direcciones si hay una ficha del oponente alrededor
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            r, c = row + dr, col + dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r, c] == opponent:
                r += dr
                c += dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r, c] == player:
                    return True
    return False

# Función para realizar una jugada
def make_move(board, row, col, player):
    if not is_valid_move(board, row, col, player):
        return False

    opponent = BLACK if player == WHITE else WHITE

    board[row, col] = player

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

    return True

# Función para verificar si hay movimientos válidos para un jugador
def has_valid_moves(board, player):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if is_valid_move(board, row, col, player):
                return True
    return False

# Juego principal
def juega_othello(player_turn):
    print_board(board)
    if not has_valid_moves(board, player_turn):
        print(f"El jugador {player_turn} no tiene movimientos válidos. Cambiando de turno.")
        player_turn = BLACK if player_turn == WHITE else WHITE
        if not has_valid_moves(board, player_turn):
            print("El juego ha terminado.")
            white_count = np.sum(board == WHITE)
            black_count = np.sum(board == BLACK)
            if white_count > black_count:
                print("¡Jugador blanco gana!")
            elif black_count > white_count:
                print("¡Jugador negro gana!")
            else:
                print("Empate.")


    try:
        row, col = map(int, input(f"Jugador {player_turn}, ingresa tu jugada (fila columna): ").split())
        if make_move(board, row, col, player_turn):
            player_turn = BLACK if player_turn == WHITE else WHITE
        else:
            print("Movimiento no válido. Inténtalo de nuevo.")
    except (ValueError, IndexError):
        print("Entrada inválida. Ingresa dos números separados por un espacio (fila columna).")



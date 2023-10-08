# Problema de Othello con Minimax, Minimax con Poda Alfa Beta, y un agente basado en Reinforcement Learning
## Integrantes del Grupo
- Romina Alfonso
- Victor Ayala
- Alejandro Notario
- Cristhian Ortellado

## Descripción del Proyecto
El juego de Othello, también conocido como Reversi, es un juego de estrategia de tablero para dos jugadores que se juega en un tablero cuadrado de 8x8. El objetivo principal del juego es capturar la mayoría de las fichas del oponente y convertirlas en tus propias fichas.

El tablero comienza con cuatro fichas colocadas en el centro de manera diagonal, dos fichas para cada jugador, con colores opuestos (generalmente negro y blanco). A partir de esta configuración inicial, los jugadores se turnan para colocar una ficha de su color en el tablero. Sin embargo, para que una jugada sea válida, la ficha que se coloca debe rodear una línea continua de fichas del oponente, de modo que todas las fichas del oponente atrapadas en esa línea queden "atrapadas" entre la ficha recién colocada y otra ficha del mismo color en la dirección opuesta. Cuando esto sucede, las fichas del oponente que quedaron atrapadas se voltean para ser del color del jugador que hizo la jugada.

El juego continúa alternando turnos entre los jugadores, y cada jugador debe realizar una jugada válida en su turno. El juego termina cuando no se pueden realizar más movimientos válidos, lo que suele ocurrir cuando el tablero está completamente lleno o cuando ninguno de los jugadores puede realizar movimientos legales. En ese momento, se cuentan las fichas de cada jugador en el tablero, y el jugador con más fichas de su color gana.

## Requerimientos
- Python 3.9.6

## Instalación y Ejecución
1. Clona el repositorio desde GitHub:
```bash
git clone https://github.com/VikMannu/othello.git
```

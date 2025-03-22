import pygame
import random
import sys
import tkinter as tk
from tkinter import messagebox

# Inicialización del motor gráfico
pygame.init()

# Constantes del juego
MAPA_ANCHO = 20
MAPA_ALTO = 9
ANCHO, ALTO = 1200, 800
TAMANO_CELDA = min(ANCHO // MAPA_ANCHO, ALTO // MAPA_ALTO)

pantalla = pygame.display.set_mode((MAPA_ANCHO * TAMANO_CELDA, MAPA_ALTO * TAMANO_CELDA))
pygame.display.set_caption("Comecocos")

# Colores
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# Mapa del juego (matriz de enteros)
mapa = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,2,2,0,1,0,2,2,2,2,2,2,2,0,1,0,2,2,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1],
    [1,2,2,2,2,0,2,2,2,2,2,2,2,2,2,0,2,2,2,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1],
    [1,0,2,2,0,1,0,2,2,2,2,2,2,2,0,1,0,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

# Variables de estado
pac_x, pac_y = 1, 1
fan_x, fan_y = 10, 5
puntos = 0
velocidad = 100

# Reinicia las variables del juego y repone puntos
def reiniciar_juego():
    """
    Restaura las posiciones de Pac-Man y el fantasma, reinicia el puntaje y repone los puntos en el mapa.
    """
    global pac_x, pac_y, fan_x, fan_y, puntos
    pac_x, pac_y = 1, 1
    fan_x, fan_y = 10, 5
    puntos = 0
    for fila in range(len(mapa)):
        for columna in range(len(mapa[fila])):
            if mapa[fila][columna] == 0:
                mapa[fila][columna] = 2

# Movimiento de Pac-Man
def mover_pacman(dx, dy):
    """
    Mueve al jugador Pac-Man dentro del mapa si la celda es válida.

    Parámetros:
        dx (int): Movimiento horizontal.
        dy (int): Movimiento vertical.

    Retorno:
        None

    Flujo de ejecución:
    1. Calcula nueva posición basada en el movimiento recibido.
    2. Verifica que la celda destino no sea una pared (valor 1).
    3. Si hay un punto (valor 2), lo elimina del mapa y suma 10 puntos.
    4. Actualiza la posición del jugador en el mapa.
    """
    global pac_x, pac_y, puntos
    nuevo_x = pac_x + dx
    nuevo_y = pac_y + dy
    if mapa[nuevo_y][nuevo_x] != 1:
        pac_x, pac_y = nuevo_x, nuevo_y
        if mapa[pac_y][pac_x] == 2:
            puntos += 10
            mapa[pac_y][pac_x] = 0

# Movimiento aleatorio del fantasma
def mover_fantasma():
    """
    Mueve al fantasma aleatoriamente en direcciones válidas (no pared).

    Flujo de ejecución:
    1. Baraja las direcciones posibles.
    2. Recorre cada dirección y verifica que no sea pared.
    3. Si es válida, actualiza la posición y termina.
    """
    global fan_x, fan_y
    direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    random.shuffle(direcciones)
    for dx, dy in direcciones:
        nuevo_x = fan_x + dx
        nuevo_y = fan_y + dy
        if mapa[nuevo_y][nuevo_x] != 1:
            fan_x, fan_y = nuevo_x, nuevo_y
            break

# Muestra mensaje final en pantalla
def mostrar_game_over(mensaje_final="Game Over"):
    """
    Muestra en pantalla un mensaje de fin de juego (Game Over o Ganador).

    Parámetros:
        mensaje_final (str): Texto a mostrar en pantalla.

    Flujo de ejecución:
    1. Limpia pantalla y muestra mensaje centrado.
    2. Espera 2 segundos.
    3. Llama a la función para preguntar si desea jugar otra vez.
    """
    pantalla.fill(NEGRO)
    fuente = pygame.font.Font(None, 72)
    texto = fuente.render(mensaje_final, True, ROJO)
    pantalla.blit(texto, (ANCHO // 3, ALTO // 3))
    pygame.display.flip()
    pygame.time.delay(2000)
    preguntar_volver_a_jugar(f"¡{mensaje_final}! ¿Quieres jugar otra vez?")

# Ventana emergente con opción de reinicio
def preguntar_volver_a_jugar(mensaje):
    """
    Muestra ventana emergente que permite reiniciar o cerrar el juego.

    Parámetros:
        mensaje (str): Mensaje que aparece en el cuadro emergente.
    """
    root = tk.Tk()
    root.withdraw()
    respuesta = messagebox.askyesno("Juego Terminado", mensaje)
    if respuesta:
        reiniciar_juego()
    else:
        pygame.quit()
        sys.exit()

# Bucle principal del juego
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]: mover_pacman(-1, 0)
    if teclas[pygame.K_RIGHT]: mover_pacman(1, 0)
    if teclas[pygame.K_UP]: mover_pacman(0, -1)
    if teclas[pygame.K_DOWN]: mover_pacman(0, 1)

    mover_fantasma()

    # Colisión con fantasma
    if pac_x == fan_x and pac_y == fan_y:
        mostrar_game_over()

    # Verificar si ya no quedan puntos
    puntos_restantes = any(2 in fila for fila in mapa)
    if not puntos_restantes:
        mostrar_game_over("Ganador")

    pantalla.fill(NEGRO)
    for fila in range(len(mapa)):
        for columna in range(len(mapa[fila])):
            x = columna * TAMANO_CELDA
            y = fila * TAMANO_CELDA
            if mapa[fila][columna] == 1:
                pygame.draw.rect(pantalla, AZUL, (x, y, TAMANO_CELDA, TAMANO_CELDA))
            elif mapa[fila][columna] == 2:
                pygame.draw.circle(pantalla, BLANCO, (x + TAMANO_CELDA // 2, y + TAMANO_CELDA // 2), 5)

    pygame.draw.rect(pantalla, AMARILLO, (pac_x * TAMANO_CELDA, pac_y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))
    pygame.draw.rect(pantalla, ROJO, (fan_x * TAMANO_CELDA, fan_y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))

    fuente = pygame.font.Font(None, 36)
    texto = fuente.render(f"Puntos: {puntos}", True, BLANCO)
    pantalla.blit(texto, (10, 10))

    pygame.display.flip()
    pygame.time.delay(velocidad)

pygame.quit()

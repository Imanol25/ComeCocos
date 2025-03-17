import pygame
import random
import sys
import tkinter as tk
from tkinter import messagebox

# Inicializar pygame
pygame.init()

# Definir constantes
MAPA_ANCHO = 20
MAPA_ALTO = 9
ANCHO, ALTO = 1200, 800
TAMANO_CELDA = min(ANCHO // MAPA_ANCHO, ALTO // MAPA_ALTO)

pantalla = pygame.display.set_mode((MAPA_ANCHO * TAMANO_CELDA, MAPA_ALTO * TAMANO_CELDA))
pygame.display.set_caption("Comecocos")

# Definir colores
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# Mapa del juego (1 = pared, 0 = espacio libre, 2 = punto)
mapa = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 2, 2, 0, 1, 0, 2, 2, 2, 2, 2, 2, 2, 0, 1, 0, 2, 2, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
    [1, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
    [1, 0, 2, 2, 0, 1, 0, 2, 2, 2, 2, 2, 2, 2, 0, 1, 0, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Posiciones iniciales
pac_x, pac_y = 1, 1
fan_x, fan_y = 10, 5
puntos = 0
velocidad = 100

# Función para reiniciar el juego
def reiniciar_juego():
    global pac_x, pac_y, fan_x, fan_y, puntos
    pac_x, pac_y = 1, 1
    fan_x, fan_y = 10, 5
    puntos = 0
    # Restaurar puntos en el mapa
    for fila in range(len(mapa)):
        for columna in range(len(mapa[fila])):
            if mapa[fila][columna] == 0:
                mapa[fila][columna] = 2

# Función para mover a Pac-Man
def mover_pacman(dx, dy):
    global pac_x, pac_y, puntos
    nuevo_x = pac_x + dx
    nuevo_y = pac_y + dy
    if mapa[nuevo_y][nuevo_x] != 1:  # No atraviesa paredes
        pac_x, pac_y = nuevo_x, nuevo_y
        if mapa[pac_y][pac_x] == 2:  # Comer punto
            puntos += 10
            mapa[pac_y][pac_x] = 0

# Función para mover al fantasma aleatoriamente
def mover_fantasma():
    global fan_x, fan_y
    direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    random.shuffle(direcciones)  # Elegir dirección aleatoria
    for dx, dy in direcciones:
        nuevo_x = fan_x + dx
        nuevo_y = fan_y + dy
        if mapa[nuevo_y][nuevo_x] != 1:  # No atraviesa paredes
            fan_x, fan_y = nuevo_x, nuevo_y
            break

# Función para mostrar Game Over
def mostrar_game_over():
    pantalla.fill(NEGRO)
    fuente = pygame.font.Font(None, 72)
    texto = fuente.render("GAME OVER", True, ROJO)
    pantalla.blit(texto, (ANCHO // 3, ALTO // 3))
    pygame.display.flip()
    pygame.time.delay(2000)  # Esperar 2 segundos
    preguntar_volver_a_jugar("¡Game Over! ¿Quieres jugar otra vez?")

# Función para preguntar si quiere volver a jugar
def preguntar_volver_a_jugar(mensaje):
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
    if teclas[pygame.K_LEFT]:
        mover_pacman(-1, 0)
    if teclas[pygame.K_RIGHT]:
        mover_pacman(1, 0)
    if teclas[pygame.K_UP]:
        mover_pacman(0, -1)
    if teclas[pygame.K_DOWN]:
        mover_pacman(0, 1)

    mover_fantasma()  # Mueve el fantasma en cada iteración

    # Verificar colisión con el fantasma
    if pac_x == fan_x and pac_y == fan_y:
        mostrar_game_over()

    # Dibujar el mapa
    pantalla.fill(NEGRO)
    for fila in range(len(mapa)):
        for columna in range(len(mapa[fila])):
            x = columna * TAMANO_CELDA
            y = fila * TAMANO_CELDA
            if mapa[fila][columna] == 1:
                pygame.draw.rect(pantalla, AZUL, (x, y, TAMANO_CELDA, TAMANO_CELDA))
            elif mapa[fila][columna] == 2:
                pygame.draw.circle(pantalla, BLANCO, (x + TAMANO_CELDA // 2, y + TAMANO_CELDA // 2), 5)

    # Dibujar a Pac-Man
    pygame.draw.rect(pantalla, AMARILLO, (pac_x * TAMANO_CELDA, pac_y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))
    # Dibujar al fantasma
    pygame.draw.rect(pantalla, ROJO, (fan_x * TAMANO_CELDA, fan_y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))

    # Mostrar puntuación
    fuente = pygame.font.Font(None, 36)
    texto = fuente.render(f"Puntos: {puntos}", True, BLANCO)
    pantalla.blit(texto, (10, 10))

    pygame.display.flip()
    pygame.time.delay(velocidad)

pygame.quit()

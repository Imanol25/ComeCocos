import pygame
import random
import sys
import tkinter as tk
from tkinter import messagebox

# Inicializar pygame
pygame.init()

# Definición de constantes y estructuras de datos
MAPA_ANCHO = 20
MAPA_ALTO = 9
ANCHO, ALTO = 1200, 800
TAMANO_CELDA = min(ANCHO // MAPA_ANCHO, ALTO // MAPA_ALTO)

pantalla = pygame.display.set_mode((MAPA_ANCHO * TAMANO_CELDA, MAPA_ALTO * TAMANO_CELDA))
pygame.display.set_caption("Comecocos")

# Colores (estructura tipo tupla)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# Mapa: Matriz (lista de listas)
mapa = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 2, 2, 0, 1, 0, 2, 2, 2, 2, 2, 2, 2, 0, 1, 0, 2, 2, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
    [1, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
    [1, 0, 2, 2, 0, 1, 0, 2, 2, 2, 2, 2, 2, 2, 0, 1, 0, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Variables del juego
pac_x, pac_y = 1, 1
fan_x, fan_y = 10, 5
puntos = 0
velocidad = 100

# === Funciones (modularización) ===

def reiniciar_juego():
    """
    Reinicia el estado del juego.
    - Control de flujo: Recorre la matriz para reiniciar puntos.
    """
    global pac_x, pac_y, fan_x, fan_y, puntos
    pac_x, pac_y = 1, 1
    fan_x, fan_y = 10, 5
    puntos = 0
    for fila in range(len(mapa)):
        for columna in range(len(mapa[fila])):
            if mapa[fila][columna] == 0:
                mapa[fila][columna] = 2

def mover_pacman(dx, dy):
    """
    Control de flujo con condicionales y matrices.
    Verifica que no se cruce una pared y suma puntos si es necesario.
    """
    global pac_x, pac_y, puntos
    nuevo_x = pac_x + dx
    nuevo_y = pac_y + dy
    if mapa[nuevo_y][nuevo_x] != 1:  # Si no es pared
        pac_x, pac_y = nuevo_x, nuevo_y
        if mapa[pac_y][pac_x] == 2:  # Si hay punto
            puntos += 10
            mapa[pac_y][pac_x] = 0

def mover_fantasma():
    """
    Usa listas, aleatoriedad y condicionales para moverse.
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

def mostrar_game_over():
    """
    Muestra mensaje de Game Over en pantalla.
    Control de flujo visual con pygame y ventana emergente con tkinter.
    """
    pantalla.fill(NEGRO)
    fuente = pygame.font.Font(None, 72)
    texto = fuente.render("GAME OVER", True, ROJO)
    pantalla.blit(texto, (ANCHO // 3, ALTO // 3))
    pygame.display.flip()
    pygame.time.delay(2000)
    preguntar_volver_a_jugar("¡Game Over! ¿Quieres jugar otra vez?")

def preguntar_volver_a_jugar(mensaje):
    """
    Muestra una ventana emergente usando tkinter.
    """
    root = tk.Tk()
    root.withdraw()
    respuesta = messagebox.askyesno("Juego Terminado", mensaje)
    if respuesta:
        reiniciar_juego()
    else:
        pygame.quit()
        sys.exit()

# === Bucle principal del juego ===
corriendo = True
while corriendo:
    # Manejo de eventos (teclado, cerrar ventana)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    # Teclas presionadas
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        mover_pacman(-1, 0)
    if teclas[pygame.K_RIGHT]:
        mover_pacman(1, 0)
    if teclas[pygame.K_UP]:
        mover_pacman(0, -1)
    if teclas[pygame.K_DOWN]:
        mover_pacman(0, 1)

    mover_fantasma()

    # Colisión con el fantasma (condicional)
    if pac_x == fan_x and pac_y == fan_y:
        mostrar_game_over()

    # Redibujar pantalla
    pantalla.fill(NEGRO)
    for fila in range(len(mapa)):
        for columna in range(len(mapa[fila])):
            x = columna * TAMANO_CELDA
            y = fila * TAMANO_CELDA
            if mapa[fila][columna] == 1:
                pygame.draw.rect(pantalla, AZUL, (x, y, TAMANO_CELDA, TAMANO_CELDA))
            elif mapa[fila][columna] == 2:
                pygame.draw.circle(pantalla, BLANCO, (x + TAMANO_CELDA // 2, y + TAMANO_CELDA // 2), 5)

    # Dibujar personajes
    pygame.draw.rect(pantalla, AMARILLO, (pac_x * TAMANO_CELDA, pac_y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))
    pygame.draw.rect(pantalla, ROJO, (fan_x * TAMANO_CELDA, fan_y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))

    # Mostrar puntaje
    fuente = pygame.font.Font(None, 36)
    texto = fuente.render(f"Puntos: {puntos}", True, BLANCO)
    pantalla.blit(texto, (10, 10))

    # Refrescar pantalla
    pygame.display.flip()
    pygame.time.delay(velocidad)

# Salida del juego
pygame.quit()


import pygame
import sys
from main import game

pygame.init()

# Configuración de la pantalla
screen_width = 1020
screen_height = int(screen_width * 0.7)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menú")

# Cargar la imagen de fondo
BG = pygame.image.load("img/background/BG.jpg")
BG = pygame.transform.scale(BG, (screen_width, screen_height))

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Fuente
font = pygame.font.Font(None, 56)

screen.fill(NEGRO)

# Opciones del menú
menu_options = ["Jugar", "Salir"]

# Función para mostrar el menú
def show_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i in range(len(menu_options)):
                    text = font.render(menu_options[i], True, NEGRO)
                    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - len(menu_options) * text.get_height() // 2 + i * 50))
                    if text_rect.collidepoint(mouse_pos):
                        if i == 0: # Juego 
                            game()
                        elif i == 1:
                            pygame.quit()
                            sys.exit()

        # Dibuja el fondo
        screen.blit(BG, (0, 0))

        # Dibuja las opciones del menú
        for i in range(len(menu_options)):
            text = font.render(menu_options[i], True, NEGRO)
            posicion_y = screen_height // 2 - len(menu_options) * text.get_height() // 2 + i * 50
            screen.blit(text, (screen_width // 2 - text.get_width() // 2, posicion_y))

        pygame.display.update()

# Mantener el Juego en Ejecucion
show_menu()
import pygame
import time


pygame.init()
screen = pygame.display.set_mode((200,200))
color = (255, 0, 0)

while True:
    screen.fill(color)
    pygame.display.update()
    color = (color[0] - 1, color[1] + 1, 0)
    time.sleep(0.05)


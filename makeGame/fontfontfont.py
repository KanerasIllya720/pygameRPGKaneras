import pygame
pygame.font.init()
l = pygame.font.get_fonts()
for i in range(len(l)):
    print(l[i])
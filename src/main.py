""" 
Programa que corre la simulación del CRT
"""

import math
import sys
import pygame
import Electron

K = 8.99e9 # Constante de coulomb
e = 1.602e-19 # Carga fundamental
FPS = 15
gameClock = pygame.time.Clock()

sprites = pygame.sprite.Group()

def createWindow():
    pygame.init()
    screen = pygame.display.set_mode((1600,900))
    pygame.display.set_caption("Simulador de CRT")
    screen.fill((255,255,255))
    gameLoop()

def gameLoop():
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        dt = gameClock.tick(FPS) / 1000
        
        sprites.update(dt)
        
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    createWindow()
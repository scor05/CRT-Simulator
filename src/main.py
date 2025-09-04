""" 
Programa que corre la simulación del CRT

Todas las fuentes utilizadas en este código fueron obtenidas de dafont.com, derechos de autor reservados.
"""

import math
import sys
import pygame
from Electron import Electron
import os

# Constantes físicas
K = 8.99e9 # Constante de coulomb
E = 1.602e-19 # Carga fundamental

# Constantes de pygame
FPS = 30
gameClock = pygame.time.Clock()
particulas = pygame.sprite.Group()
labelFontPath = os.path.join(os.path.dirname(__file__), "..", "fonts", "game_over.ttf")
titleFontPath = os.path.join(os.path.dirname(__file__), "..", "fonts", "PEPSI_pl.ttf")
COLOR_WHITE =(255,255,255)
COLOR_RED = (255,0,0)
COLOR_GREEN = (0,255,0)
COLOR_BLACK = (0,0,0)
COLOR_LIGHT_GRAY = (220, 220, 220)

# Imagenes
electronImgPath = os.path.join(os.path.dirname(__file__), "..", "res", "electronSmall.png")
electronImg = pygame.image.load(electronImgPath)
tubeTopImgPath = os.path.join(os.path.dirname(__file__), "..", "res", "tubo_vista_vertical.png")
tubeTopImg = pygame.image.load(tubeTopImgPath)
tubeBottomImgPath = os.path.join(os.path.dirname(__file__), "..", "res", "tubo_vista_horizontal.png")
tubeBottomImg = pygame.image.load(tubeBottomImgPath)
imageList = [electronImg, tubeTopImg, tubeBottomImg]

# Márgenes
topViewRect = pygame.Rect(100,100,350,250)
horizontalViewRect = pygame.Rect(100,400,350,250)
frontViewRect = pygame.Rect(650, 250, 500, 500)


def drawMargin(surface: pygame.Surface, rect: pygame.Rect, label: str, font: pygame.font.SysFont, borderColor, fillColor):
    pygame.draw.rect(surface, borderColor, rect, 4) # último parámetro es grosor de línea
    insideRect = pygame.Rect(rect.left + 4, rect.top + 4, rect.width - 8, rect.height - 8)
    pygame.draw.rect(surface, fillColor, insideRect)
    text = font.render(label, True, borderColor)
    text_rect = text.get_rect()
    text_rect.topleft = (rect.left, rect.top - text_rect.height - 4)
    surface.blit(text, text_rect)
    
def createWindow():
    pygame.init()
    screen = pygame.display.set_mode((1600,900))
    pygame.display.set_caption("Simulador de CRT")
    screen.fill((255,255,255))
    for i in imageList:
        i.convert_alpha
    
    # tipo de fuente personalizado
    global labelFont, titleFont
    labelFont = pygame.font.Font(labelFontPath, 75)
    titleFont = pygame.font.Font(titleFontPath, 75)
    
    for i in range(5):
        e = Electron(100+50*i,100,0,0,0,electronImg)
        particulas.add(e)
    for p in particulas:
        p.applyForce(K*E*E/30, K*E*E/30)
    gameLoop(screen)

def gameLoop(screen):
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        dt = gameClock.tick(FPS) / 1000
        
        # Márgenes de las vistas
        topViewRect = pygame.Rect(25,155,350,250)
        horizontalViewRect = pygame.Rect(25,540,350,250)
        frontViewRect = pygame.Rect(425,130,725,725)
        controlsRect = pygame.Rect(1175,75,400,750)
        drawMargin(screen, controlsRect, "Controles de Usuario", labelFont, COLOR_BLACK, COLOR_LIGHT_GRAY)
        drawMargin(screen, topViewRect, "Vista Superior", labelFont, COLOR_BLACK, COLOR_LIGHT_GRAY)
        drawMargin(screen,horizontalViewRect, "Vista Horizontal", labelFont, COLOR_BLACK, COLOR_LIGHT_GRAY)
        drawMargin(screen, frontViewRect, "Vista Frontal", labelFont, COLOR_BLACK, COLOR_LIGHT_GRAY)
        
        titleLabel = titleFont.render("!Simulador de CRT", True, COLOR_BLACK)
        titleLabelRect = titleLabel.get_rect(center = (435,50))
        screen.blit(titleLabel, titleLabelRect)
        
        
        # Imagenes de los tubos
        screen.blit(tubeTopImg, (50, 180))
        screen.blit(tubeBottomImg, (50, 560))
        
        particulas.update(dt)
        particulas.draw(screen)
        
        pygame.display.flip()
        screen.fill((255,255,255))
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    createWindow()
""" 
Programa que corre la simulación del CRT

Todas las fuentes utilizadas en este código fueron obtenidas de dafont.com, derechos de autor reservados.
"""

import math
import sys
import pygame
from ElectronClass import Electron, E
from PlacaClass import Placa, V_PLAQUE_MIN, V_CANNON_MAX, V_CANNON_MIN, V_PLAQUE_MAX, K
import os

TUBE_LENGTH = 0.50 # longitud del tubo de rayos, 0.5 m
SCREEN_DIMENSIONS = 0.1 # anchura de la pantalla de vista frontal (es también igual a la altura, 0.1 m)
PLAQUE_LENGTH = 0.1 # longitud de las placas cuadradas, para determinar por cuántos frames aplicarle fuerza al electrón
PLAQUE_SEPARATION = 0.005 # Distancia entre las placas 
HORIZONTAL_PLAQUES_Z = 0.15 # a 0.15 m del cañón, se estrecha hasta z = 25
VERTICAL_PLAQUES_Z = 0.30 # con 5cm de separación entre la horizontal, se estrecha a z = 40 (donde empieza la inclinación)


# Imagenes
electronImgPath = os.path.join(os.path.dirname(__file__), "..", "res", "electronSmall.png")
electronImg = pygame.image.load(electronImgPath)
tubeTopImgPath = os.path.join(os.path.dirname(__file__), "..", "res", "tubo_vista_vertical.png")
tubeTopImg = pygame.image.load(tubeTopImgPath)
tubeBottomImgPath = os.path.join(os.path.dirname(__file__), "..", "res", "tubo_vista_horizontal.png")
tubeBottomImg = pygame.image.load(tubeBottomImgPath)
imageList = [electronImg, tubeTopImg, tubeBottomImg]

# Constantes de pygame
FPS = 30
gameClock = pygame.time.Clock()
particulas = pygame.sprite.Group()
front_electron_lifetime = {} # guarda cuántas frames le queda a cada electrón para que se borre
labelFontPath = os.path.join(os.path.dirname(__file__), "..", "fonts", "game_over.ttf")
titleFontPath = os.path.join(os.path.dirname(__file__), "..", "fonts", "PEPSI_pl.ttf")
COLOR_WHITE =(255,255,255)
COLOR_RED = (255,0,0)
COLOR_GREEN = (0,255,0)
COLOR_BLACK = (0,0,0)
COLOR_LIGHT_GRAY = (220, 220, 220)
SCALE_FRONT = 725 / SCREEN_DIMENSIONS   # 7250 px/m, la pantalla mide 725 px x 725 px (ver frontViewRect en gameloop)
SCALE_SIDES = 300 / TUBE_LENGTH          # 600 px/m (la imagen de tubo mide 300x200, el ancho se usa aquí para la escala)
ORIGIN_FRONT = (425 + 725//2, 130 + 725//2)  # centro del rect frontal
electron_sprite_half = electronImg.get_width() // 2 # Ajustar offset por la sprite del electrón
ORIGIN_SIDE = (50 - electron_sprite_half, 560 + 200//2)             # entrada del tubo en vista lateral
ORIGIN_TOP = (50 - electron_sprite_half, 180 + 200//2)              # entrada del tubo en vista superior


# prueba
e = Electron(0,0,0,0,0,0.05,electronImg) # electron de prueba
particulas.add(e)
for p in particulas:
    front_electron_lifetime[p] = 10 # 1/3 de segundo por cada electrón (30fps / 10 frames)

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
    
    gameLoop(screen)

def gameLoop(screen):
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        dt = gameClock.tick(FPS) / 1000
        
        # Márgenes de las vistas
        
        screen.fill((255,255,255))
        
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
        
        for p in particulas:
            if (p.pos[2] < TUBE_LENGTH):
                p.image.set_alpha(255)
                p.draw_in_view(screen, 'top', ORIGIN_TOP, SCALE_SIDES)
                p.draw_in_view(screen, 'side', ORIGIN_SIDE, SCALE_SIDES)
            elif (front_electron_lifetime[p] != 0):
                front_electron_lifetime[p] -= 1
                alphaVal = p.calculateOpacity()
                p.image.set_alpha(alphaVal)
                p.draw_in_view(screen, 'front', ORIGIN_FRONT, SCALE_FRONT)
            elif (front_electron_lifetime[p] == 0):
                front_electron_lifetime.pop(p)
                particulas.remove(p)
            
        particulas.update(dt)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    createWindow()
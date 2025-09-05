""" 
Programa que corre la simulación del CRT

Todas las fuentes utilizadas en este código fueron obtenidas de dafont.com, derechos de autor reservados.
"""

import math
import sys
import pygame
from ElectronClass import Electron
from PlacaClass import Placa, V_PLAQUE_MIN, V_PLAQUE_MAX
from constants import V_CANNON_MAX, V_CANNON_MIN
import os

TUBE_LENGTH = 1 # longitud del tubo de rayos, 
SCREEN_DIMENSIONS = 0.4 # anchura de la pantalla de vista frontal (es también igual a la altura)
PLAQUE_LENGTH = 0.2 # longitud de las placas cuadradas, para determinar por cuántos frames aplicarle fuerza al electrón
PLAQUE_SEPARATION = 0.01 # Distancia entre las placas 
HORIZONTAL_PLAQUES_Z = 0.3 # punto inicial de las placas horizontales
VERTICAL_PLAQUES_Z = 0.6 # punto inicial de las placas verticales


# Imagenes
electronImgPath = os.path.join(os.path.dirname(__file__), "..", "res", "electronSmall.png")
electronImg = pygame.image.load(electronImgPath)
tubeTopImgPath = os.path.join(os.path.dirname(__file__), "..", "res", "tubo_vista_vertical.png")
tubeTopImg = pygame.image.load(tubeTopImgPath)
tubeBottomImgPath = os.path.join(os.path.dirname(__file__), "..", "res", "tubo_vista_horizontal.png")
tubeBottomImg = pygame.image.load(tubeBottomImgPath)
imageList = [electronImg, tubeTopImg, tubeBottomImg]

# Constantes de pygame
FPS = 120
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
SCALE_FRONT = 725 / SCREEN_DIMENSIONS
SCALE_SIDES = 350 / TUBE_LENGTH
ORIGIN_FRONT = (425, 130)
electron_sprite_half = electronImg.get_width() // 2 # Ajustar offset por la sprite del electrón
ORIGIN_SIDE = (50 - electron_sprite_half, 560 + 200//2)             # entrada del tubo en vista lateral
ORIGIN_TOP = (50 - electron_sprite_half, 180 + 200//2)              # entrada del tubo en vista superior

# Contador global
global_time = 0.0
electron_spawn_interval = 0.1
last_electron_spawn = 0.0

# Generación de placas
horizontal_P1 = Placa(HORIZONTAL_PLAQUES_Z, 0.05)
horizontal_P2 = Placa(HORIZONTAL_PLAQUES_Z, -0.05)
vertical_P1 = Placa(VERTICAL_PLAQUES_Z, 0)
vertical_P2 = Placa(VERTICAL_PLAQUES_Z, -0)

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
    global global_time, last_electron_spawn
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        dt = gameClock.tick(FPS) / 1000.0  # Asegurar que sea float
        global_time += dt
        
        screen.fill((255, 255, 255))
        
        # Márgenes de las vistas
        topViewRect = pygame.Rect(25, 155, 350, 250)
        horizontalViewRect = pygame.Rect(25, 540, 350, 250)
        frontViewRect = pygame.Rect(425, 130, 725, 725)
        controlsRect = pygame.Rect(1175, 75, 400, 750)
        
        drawMargin(screen, controlsRect, "Controles de Usuario", labelFont, COLOR_BLACK, COLOR_LIGHT_GRAY)
        drawMargin(screen, topViewRect, "Vista Superior", labelFont, COLOR_BLACK, COLOR_LIGHT_GRAY)
        drawMargin(screen, horizontalViewRect, "Vista Horizontal", labelFont, COLOR_BLACK, COLOR_LIGHT_GRAY)
        drawMargin(screen, frontViewRect, "Vista Frontal", labelFont, COLOR_BLACK, COLOR_LIGHT_GRAY)
        
        titleLabel = titleFont.render("Simulador de CRT", True, COLOR_BLACK)
        titleLabelRect = titleLabel.get_rect(center=(435, 50))
        screen.blit(titleLabel, titleLabelRect)
        
        # Imágenes de los tubos
        screen.blit(tubeTopImg, (50, 180))
        screen.blit(tubeBottomImg, (50, 560))
        
        # Spawnar un electrón únicamente si ha pasado el intervalo de tiempo dado
        if global_time - last_electron_spawn >= electron_spawn_interval:
            # Usar valores exactos para evitar acumulación de errores
            e = Electron(0.0, 0.0, 0.0, 0.0, 0.0, 4, electronImg)
            particulas.add(e)
            e.fixed = False
            front_electron_lifetime[e] = 10
            last_electron_spawn = global_time
        
        # Lista temporal para evitar modificar el grupo durante iteración
        electrons_to_remove = []
        
        # Debug: contar electrones en diferentes estados
        in_tube = 0
        in_front = 0
        to_remove = 0
        
        for p in particulas:
            if p.pos[2] < TUBE_LENGTH:
                in_tube += 1
                # El electrón está viajando por el tubo
                p.image.set_alpha(255)
                
                # Aplicar fuerzas de las placas horizontales
                if (HORIZONTAL_PLAQUES_Z <= p.pos[2] <= HORIZONTAL_PLAQUES_Z + PLAQUE_LENGTH):
                    force_x = horizontal_P1.exertForce(horizontal_P2, PLAQUE_SEPARATION)
                    p.applyForce(force_x, 0)
                
                # Aplicar fuerzas de las placas verticales
                if (VERTICAL_PLAQUES_Z <= p.pos[2] <= VERTICAL_PLAQUES_Z + PLAQUE_LENGTH):
                    force_y = vertical_P1.exertForce(vertical_P2, PLAQUE_SEPARATION)
                    p.applyForce(0, force_y)
                
                # Dibujar en vistas laterales
                p.draw_in_view(screen, 'top', ORIGIN_TOP, SCALE_SIDES, SCREEN_DIMENSIONS)
                p.draw_in_view(screen, 'side', ORIGIN_SIDE, SCALE_SIDES, SCREEN_DIMENSIONS)
                
            elif p.pos[2] >= TUBE_LENGTH and front_electron_lifetime[p] > 0:
                in_front += 1
                # El electrón ha llegado a la pantalla frontal
                front_electron_lifetime[p] -= 1
                alphaVal = p.calculateOpacity()
                p.image.set_alpha(255)  # TODO: cambiar a alphaVal cuando funcione
                
                # Fijar SOLO UNA VEZ
                if not p.fixed:
                    # Corrigir overshoot en Z
                    overshoot = p.pos[2] - TUBE_LENGTH
                    if p.velocity[2] != 0:
                        t_correction = overshoot / p.velocity[2]
                    else:
                        t_correction = 0

                    # Retroceder X e Y proporcionalmente
                    p.pos[0] -= p.velocity[0] * t_correction
                    p.pos[1] -= p.velocity[1] * t_correction
                    # Colocar Z exactamente en la pantalla
                    p.pos[2] = TUBE_LENGTH

                    # Clamp opcional para evitar salirse de la pantalla física
                    half_dim = SCREEN_DIMENSIONS / 2
                    if p.pos[0] < -half_dim: p.pos[0] = -half_dim
                    elif p.pos[0] > half_dim: p.pos[0] = half_dim
                    if p.pos[1] < -half_dim: p.pos[1] = -half_dim
                    elif p.pos[1] > half_dim: p.pos[1] = half_dim

                    # Congelar electrón
                    p.velocity = [0, 0, 0]
                    p.fixed = True
                
                # Dibujar en vista frontal usando la escala consistente
                p.draw_in_view(screen, 'front', ORIGIN_FRONT, SCALE_FRONT, SCREEN_DIMENSIONS)
                
            else:
                to_remove += 1
                # El electrón ha terminado su vida útil en la pantalla
                electrons_to_remove.append(p)
        
        # Remover electrones que han terminado su ciclo de vida
        for electron in electrons_to_remove:
            if electron in front_electron_lifetime:
                front_electron_lifetime.pop(electron)
            particulas.remove(electron)
        
        # Actualizar todas las partículas
        particulas.update(dt)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    createWindow()
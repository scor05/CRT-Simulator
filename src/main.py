""" 
Programa que corre la simulación del CRT

Todas las fuentes utilizadas en este código fueron obtenidas de dafont.com, derechos de autor reservados.
"""

import math
import sys
import pygame
from ElectronClass import Electron
from PlacaClass import Placa
import os

TUBE_LENGTH = 1 # longitud del tubo de rayos 
SCREEN_DIMENSIONS = 0.5 # anchura de la pantalla de vista frontal (es también igual a la altura)
PLAQUE_LENGTH = 0.2 # longitud de las placas cuadradas, para determinar por cuántos frames aplicarle fuerza al electrón
PLAQUE_SEPARATION = 0.05 # Distancia entre las placas 
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
FPS = 60
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
electron_spawn_interval = 0.05
last_electron_spawn = 0.0

# Generación de placas
horizontal_P1 = Placa(HORIZONTAL_PLAQUES_Z, 0.05)
horizontal_P2 = Placa(HORIZONTAL_PLAQUES_Z, -0.05)
vertical_P1 = Placa(VERTICAL_PLAQUES_Z, 0)
vertical_P2 = Placa(VERTICAL_PLAQUES_Z, -0)

# Variables de control del usuario:
user_voltage_accel = 1.0 # voltaje de aceleración inicial (es igual a la velocidad porque Vz constante)
user_voltage_vert  = 0.0 # voltaje vertical
user_voltage_horiz = 0.0 # voltaje horizontal
user_mode_sinusoidal = False
user_freq_x = 1.0 # Hz, para las placas horizontales
user_freq_y = 1.0 # Hz, para las placas verticales
user_phase = 0.0 # rad
SINE_AMPLITUDE = 0.06 # constante arbitraria para reducir el efecto del seno.


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
    labelFont = pygame.font.Font(labelFontPath, 65)
    titleFont = pygame.font.Font(titleFontPath, 65)
    
    gameLoop(screen)

def gameLoop(screen):
    global global_time, last_electron_spawn
    global user_voltage_accel, user_voltage_vert, user_voltage_horiz
    global user_mode_sinusoidal, user_phase, user_freq_x, user_freq_y
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    user_voltage_accel = max(1, user_voltage_accel - 0.1)
                elif event.key == pygame.K_e:
                    user_voltage_accel += 0.1
                elif event.key == pygame.K_w:
                    user_voltage_vert += 0.1
                elif event.key == pygame.K_s:
                    user_voltage_vert -= 0.1
                elif event.key == pygame.K_a:
                    user_voltage_horiz -= 0.1
                elif event.key == pygame.K_d:
                    user_voltage_horiz += 0.1
                elif event.key == pygame.K_m:
                    user_mode_sinusoidal = not user_mode_sinusoidal
                elif event.key == pygame.K_f:
                    user_freq_x += 0.1
                elif event.key == pygame.K_g:
                    user_freq_x = max(0.1, user_freq_x - 0.1)
                elif event.key == pygame.K_v:
                    user_freq_y += 0.1
                elif event.key == pygame.K_b:
                    user_freq_y = max(0.1, user_freq_y - 0.1)
                elif event.key == pygame.K_r:
                    user_phase += 0.1
                elif event.key == pygame.K_t:
                    user_phase -= 0.1
                
        dt = gameClock.tick(FPS) / 1000.0
        global_time += dt
        
        screen.fill((255, 255, 255))
        
        # Márgenes de las vistas
        topViewRect = pygame.Rect(25, 155, 350, 250)
        horizontalViewRect = pygame.Rect(25, 540, 350, 250)
        frontViewRect = pygame.Rect(425, 130, 725, 725)
        controlsRect = pygame.Rect(1175, 105, 412, 750)
        
        drawMargin(screen, controlsRect, "Controles de Usuario", labelFont, COLOR_BLACK, COLOR_LIGHT_GRAY)
        drawMargin(screen, topViewRect, "Vista Superior", labelFont, COLOR_BLACK, COLOR_LIGHT_GRAY)
        drawMargin(screen, horizontalViewRect, "Vista Horizontal", labelFont, COLOR_BLACK, COLOR_LIGHT_GRAY)
        drawMargin(screen, frontViewRect, "Vista Frontal", labelFont, COLOR_BLACK, COLOR_LIGHT_GRAY)
        
        titleLabel = titleFont.render("Simulador de TRC", True, COLOR_BLACK)
        titleLabelRect = titleLabel.get_rect(center=(435, 50))
        screen.blit(titleLabel, titleLabelRect)
        
        # Renderizar controles dentro del rectángulo de usuario
        controls_text = [
            f"Q/E: Voltaje aceleración = {user_voltage_accel:.1f}",
            f"W/S: Voltaje vertical = {user_voltage_vert:.1f}",
            f"A/D: Voltaje horizontal = {user_voltage_horiz:.1f}",
            f"M: Modo = {'Sinusoidal' if user_mode_sinusoidal else 'Manual'}",
            f"F/G: Frecuencia X = {user_freq_x:.1f} Hz",
            f"V/B: Frecuencia Y = {user_freq_y:.1f} Hz",
            f"R/T: Fase = {user_phase:.2f} rad"
        ]

        y_offset = controlsRect.top + 30
        for line in controls_text:
            text_surface = labelFont.render(line, True, COLOR_BLACK)
            screen.blit(text_surface, (controlsRect.left + 10, y_offset))
            y_offset += 50
        
        # Imágenes de los tubos
        screen.blit(tubeTopImg, (50, 180))
        screen.blit(tubeBottomImg, (50, 560))
        
        # Spawnar un electrón únicamente si ha pasado el intervalo de tiempo dado
        if global_time - last_electron_spawn >= electron_spawn_interval:
            # Usar valores exactos para evitar acumulación de errores
            e = Electron(0.0, 0.0, 0.0, 0.0, 0.0, user_voltage_accel, electronImg)
            particulas.add(e)
            e.fixed = False
            front_electron_lifetime[e] = 5
            last_electron_spawn = global_time
        
        # Lista temporal para evitar modificar el grupo durante iteración
        electrons_to_remove = []
        
        
        for p in particulas:
            if p.pos[2] < TUBE_LENGTH:
                # El electrón está viajando por el tubo
                p.image.set_alpha(255)
                
                # Definir fuerzas de usuario (manual o sinusoidal)
                if user_mode_sinusoidal:
                    horizontal_P1.voltage = SINE_AMPLITUDE * math.sin(2*math.pi*user_freq_x*global_time + user_phase)
                    horizontal_P2.voltage = -1* horizontal_P1.voltage
                    vertical_P1.voltage = SINE_AMPLITUDE * math.sin(2*math.pi*user_freq_y*global_time + user_phase)
                    vertical_P2.voltage = -1* vertical_P2.voltage
                else:
                    horizontal_P1.voltage = user_voltage_horiz
                    horizontal_P2.voltage = - horizontal_P1.voltage
                    vertical_P1.voltage = user_voltage_vert
                    vertical_P2.voltage = - vertical_P1.voltage

                force_x = 0.0
                force_y = 0.0
                # Aplicar fuerzas si el electrón está dentro de las placas
                if HORIZONTAL_PLAQUES_Z <= p.pos[2] <= HORIZONTAL_PLAQUES_Z + PLAQUE_LENGTH:
                    force_x = horizontal_P1.exertForce(horizontal_P2, PLAQUE_SEPARATION)
                if VERTICAL_PLAQUES_Z <= p.pos[2] <= VERTICAL_PLAQUES_Z + PLAQUE_LENGTH:
                    force_y = vertical_P1.exertForce(vertical_P2, PLAQUE_SEPARATION)
                
                p.applyForce(force_x, force_y)
                
                # Dibujar en vistas laterales
                p.draw_in_view(screen, 'top', ORIGIN_TOP, SCALE_SIDES, SCREEN_DIMENSIONS)
                p.draw_in_view(screen, 'side', ORIGIN_SIDE, SCALE_SIDES, SCREEN_DIMENSIONS)
                rect = p.image.get_rect(center=(int(ORIGIN_SIDE[0] + p.pos[2]*SCALE_SIDES),
                                        int(ORIGIN_SIDE[1] - p.pos[1]*SCALE_SIDES)))
                if rect.centerx >= 335:
                    p.pos[2] = TUBE_LENGTH  # forzamos impacto
                
            elif p.pos[2] >= TUBE_LENGTH and front_electron_lifetime[p] > 0:
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

                    # Clamp para evitar salirse de la pantalla física
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
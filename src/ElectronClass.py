"""
Archivo de la clase de electron para guardar momentum y fuerzas

Teoría:
El eje Z para el electrón representa el eje de profundidad del tubo de rayos
catódicos, por ende, entre mayor velocidad en Z tenga el electrón, mayor brillo
tendrá. Sabiendo que el voltaje máximo (Vmax) y mínimo (Vmin) son fijos, la velocidad
mínimia y máxima se puede determinar con métodos de energía:

Para todo el proceso de lanzarse en el cañón:
delta(E) = 0
(Kf - Ki) + (Uf - Ui) = 0 -> delta(V) = delta(U) / q
Kf - Ki + q*delta(V) = 0 -> Kf = 0 porque choca contra la pantalla
q*deltaV = Ki
1/2m(Vz)^2 = e*V
Vz = sqrt(2eV/m) -> Velocidad en Z para cualquier voltaje del cañón
Por ende -> Vmin = sqrt(2eVmin_cañon/m)
Vmax = sqrt(2eVmax_cañon/m)

Cada instancia del electrón se inicializa con esa mangitud de velocidad y esa
se mantiene constante durante toda su trayectoria porque el campo eléctrico de
las placas se cancela en Z por simetría.

* SE USARON CONSTANTES ARBITRARIAS PARA FINES SIMULATIVOS, M = 1, K = 1.
"""

import os
import math
import pygame
from constants import *
from PlacaClass import Placa

# Por la utilización de unidades arbitrarias, el cálculo anterior de las velocidades límite no funciona.
# VZ_max = math.sqrt(2*(1)*VOLTAGE_ACCEL_MAX/1)
# VZ_min = math.sqrt(2*(1)*VOLTAGE_ACCEL_MIN/1)

def m_to_px(meters, scale):
    return meters*scale

class Electron(pygame.sprite.Sprite):
    # mass = M_E
    
    def __init__(self, Xo, Yo, Zo, VoX, VoY, VoZ, img):
        super().__init__()
        # Velocidad y posición en Z solo para simular frecuencia de golpeo de electrones (brillo).
        self.pos = [float(Xo), float(Yo), float(Zo)]
        self.velocity = [float(VoX), float(VoY), float(VoZ)]
        self.fixed = False
        self.image = img
        self.force = [0,0] # Empezar con Fnet = 0
        
        self.rect = self.image.get_rect()
    
    def calculateOpacity(self, voltage: float) -> int:
        
        # Normalizar para que con la velocidad mínima sea un cuarto de opacidad, con la máxima el 100%
        # con base a los voltajes de las placas
        calc = abs(voltage - VOLTAGE_ACCEL_MIN) / (VOLTAGE_ACCEL_MAX - VOLTAGE_ACCEL_MIN)
        calc = max(0.0, min(1.0, calc)) # estandarizar a [0,1] por si da error de negativos
        opacity = 0.25 + (0.75*calc)
        return int(255*opacity)
        
    def applyForce(self, Fx: float, Fy: float):
        self.force[0] += Fx
        self.force[1] += Fy
    
    def update(self, dt: float):
        """
        dt -> intervalo de tiempo entre frames en seg.
        """
        dt = float(dt)
        
        self.velocity[0] += self.force[0]*dt
        self.velocity[1] += self.force[1]*dt
        # velocidad en Z es constante, no se actualiza
        
        self.pos[0] += self.velocity[0]*dt
        self.pos[1] += self.velocity[1]*dt
        self.pos[2] += self.velocity[2]*dt
        
        # print("x=",self.pos[0], "vx=", self.velocity[0], "y=",self.pos[1], "vy",self.velocity[1])
        
        # Resetea la fuerza en cada frame
        self.force = [0,0]
        
    def draw_in_view(self, surface, view, origin_px, scale, screenDimensions):
        """
        Para dibujar en las vistas horizontales, verticales y frontales porque cambia la escala por cada una.
        view  String = 'front', 'side', 'top'
        origin_px: (x0, y0) en píxeles de donde empieza a dibujar la vista
        scale: px/m correspondiente a esa vista
        """
        if view == 'front':  
            # vista frontal: pantalla en plano x-y
            # sumar la mitad de las dimensiones de la pantalla a x, restar a y para que quede
            # en el centro
            x_px = origin_px[0] + (self.pos[0] + 0.5 * screenDimensions) * scale
            y_px = origin_px[1] + (0.5 * screenDimensions - self.pos[1]) * scale
        elif view == 'side':
            # vista horizontal: z -> eje x, y -> eje y
            x_px = origin_px[0] + m_to_px(self.pos[2], scale)
            y_px = origin_px[1] - m_to_px(self.pos[1], scale)
        elif view == 'top':
            # vista superior: z -> eje x, x -> eje y
            x_px = origin_px[0] + m_to_px(self.pos[2], scale)
            y_px = origin_px[1] - m_to_px(self.pos[0], scale)
        else:
            return
                
        # Debugger de coordenadas inválidas
        if not (math.isfinite(x_px) and math.isfinite(y_px)):
            print(f"Coordenadas inválidas en vista {view}: x_px={x_px}, y_px={y_px}")
            print(f"Posición del electrón: {self.pos}")
            return
            
        rect = self.image.get_rect(center=(int(x_px), int(y_px)))

        # Límites específicos para cada vista (para no dibujar afuera de ellas:
        if view == 'front':
            left = origin_px[0]
            top = origin_px[1]
            right = origin_px[0] + screenDimensions * scale
            bottom = origin_px[1] + screenDimensions * scale
            if left <= rect.centerx <= right and top <= rect.centery <= bottom:
                surface.blit(self.image, rect)
        else:
            if -100 < rect.centerx < 340 and -100 < rect.centery < 1000:
                surface.blit(self.image, rect)
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

Cada instancia del electrón se inicializa con esa mangitud de velocidad y esa
se mantiene constante durante toda su trayectoria porque el campo eléctrico de
las placas se cancela en Z por simetría.

Cuando se instancia el electrón, no se dibujará en la placa frontal hasta que
el tiempo elapsado desde su instanciamiento sea el correcto dada la velocidad
en Z -> t = x/v_z

Para el brillo, se usará la siguiente ecuación para determinar la fracción
de opacidad que tendrá la imagen del electrón en la placa frontal:
b = (Vz - Vz_min) / (Vz_max - Vz_min)
"""

import os
import math
import pygame

def m_to_px(meters, scale):
    return meters*scale

class Electron(pygame.sprite.Sprite):
    mass = 9.11e-31
    
    def __init__(self, Xo, Yo, Zo, VoX, VoY, VoZ, img):
        super().__init__()
        self.pos = [Xo, Yo, Zo]
        # Velocidad en Z solo para simular frecuencia de golpeo de electrones (brillo).
        self.velocity = [VoX, VoY, VoZ]
        self.accel = [0,0]
        self.image = img
        self.force = [0,0] # Empezar con Fnet = 0
        
        self.rect = self.image.get_rect()
        
    def applyForce(self, Fx: float, Fy: float):
        self.force = [Fx, Fy]
    
    def update(self, dt: float):
        """ 
        dt -> intervalo de tiempo entre frames en seg.
        """
        self.accel[0] = self.force[0] / self.mass
        self.accel[1] = self.force[1] / self.mass
        
        self.velocity[0] += self.accel[0]*dt
        self.velocity[1] += self.accel[1]*dt
        # velocidad en Z es constante, no se actualiza
        
        self.pos[0] += self.velocity[0]*dt
        self.pos[1] += self.velocity[1]*dt
        self.pos[2] += self.velocity[2]*dt 
        
        # Resetea la fuerza en cada frame
        self.force = [0,0]
        
    def draw_in_view(self, surface, view, origin_px, scale):
        """
        Para dibujar en las vistas horizontales, verticales y frontales porque cambia la escala por cada una.
        view  String = 'front', 'side', 'top'
        origin_px: (x0, y0) en píxeles de donde empieza a dibujar la vista
        scale: px/m correspondiente a esa vista
        """
        if view == 'front':  
            # vista frontal: pantalla en plano x-y
            x_px = origin_px[0] + m_to_px(self.pos[0], scale)
            y_px = origin_px[1] - m_to_px(self.pos[1], scale) # - porque en pygame +y es hacia abajo
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

        rect = self.image.get_rect(center=(x_px, y_px))
        surface.blit(self.image, rect)
"""
Archivo de la clase de electron para guardar momentum
"""

import os
import math
import pygame

class Electron(pygame.sprite.Sprite):
    mass = 9.11e-31
    
    def __init__(self, Xo, Yo, VoX, VoY, VoZ, img):
        super().__init__()
        self.pos = [Xo, Yo]
        # Velocidad en Z solo para simular frecuencia de golpeo de electrones.
        self.velocity = [VoX, VoY, VoZ]
        self.accel = [0,0]
        self.image = img
        self.force = [0,0] # Empezar con Fnet = 0
        
        self.rect = self.image.get_rect()
        self.rect.center = (Xo, Yo)
        
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
        
        self.pos[0] += self.velocity[0]*dt
        self.pos[1] += self.velocity[1]*dt
        
        self.rect.center = (self.pos[0], self.pos[1])
        
        # Resetea la fuerza en cada frame
        self.force = [0,0]
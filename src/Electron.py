"""
Archivo de la clase de electron para guardar momentum
"""

import os
import math
import pygame

class Electron(pygame.sprite.Sprite):
    mass = 9.11e-31
    
    def __init__(self, Xo, Yo, VoX, VoY):
        super().__init__()
        self.pos = [Xo, Yo]
        self.velocity = [VoX, VoY]
        self.accel = [0,0]
        
        imagePath = os.path.join(os.path.dirname(__file__), "..", "res", "electron.png")
        self.img = pygame.image.load(imagePath).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (Xo, Yo)
        
        
    def applyForce(self, Fx: float, Fy: float) -> float:
        self.accel = [Fx/self.mass, Fy/self.mass]
    
    def update(self, dt: float): # deltaTime
        """ 
        dt -> intervalo de tiempo entre frames en seg.
        """
        
        self.velocity[0] += self.accel[0]*dt
        self.velocity[1] += self.accel[1]*dt
        
        self.pos[0] += self.velocity[0]*dt
        self.pos[1] += self.velocity[1]*dt
        
        self.rect.center = (self.pos[0], self.pos[1])
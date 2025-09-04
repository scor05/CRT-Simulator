""" 
Clase de placa que guarda el campo eléctrico y el voltaje para aplicarle fuerzas al electron
"""

import os
import math
import pygame

class Placa(pygame.sprite.Sprites):
    def __init__(self, X, Y, img):
        self.x = X
        self.y = Y
        self.image = img
    
    def setVoltage(self, V):
        self.voltage = V
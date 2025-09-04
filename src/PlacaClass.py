""" 
Clase de placa que guarda el campo eléctrico y el voltaje para aplicarle fuerzas al electrón

Teoría:
Dado V = -integral_línea(E dot dr), para una placa con un electrón que pasa en el eje de simetría,
el cos del ángulo entre E y dr es 180, por lo que E dot dr = Edrcos(theta) = Edr(-1):
V = -integral_linea(-Edr) = Eintegral(dr) = E * r
Por ende -> E = V/r (donde r es la distancia del electrón a la placa)
De eso, F/q = V/r
F = qV/r
F = eV/r -> fuerza aplicada a los electrones (con el voltaje dado por el usuario)

Las placas aplicarán dicha fuerza a los electrones por toda la duración en lo que los electrones
estén en el rango de coordenadas [L, 2L], donde L es la longitud de la placa (declarada en main)

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
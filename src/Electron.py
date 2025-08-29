"""
Archivo de la clase de electron para guardar momentum
"""

import math

class Electron:
    velocity = [] # componentes x,y
    accel = [] # componentes x,y
    pos = [] # componentes x,y
    mass = 9.11e-31
    
    def __init__(self, Vox, Voy):
        velocity = [Vox, Voy]
        
    def applyForce(self, Fx: float, Fy: float) -> float:
        accel = [Fx/self.mass, Fy/self.mass]
        
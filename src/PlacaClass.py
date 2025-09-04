""" 
Clase de placa que guarda el campo eléctrico y el voltaje para aplicarle fuerzas al electrón

Teoría:

El voltaje del par de placas paralelas que se ve en los CRT se define como la integral de 
la intensidad de campo eléctrico a lo largo de una distancia (integral de línea):
V = - ∫ (E dot dr)

Si el campo eléctrico es constante y paralelo a la trayectoria se cumple lo
siguiente debido a que E dot dr = Edrcos(theta) = Edrcos(180) = -Edr:
V = E * d
donde:
V = diferencia de potencial aplicada entre placas
d = separación entre placas

Por ende -> E = V / d
Y también -> F = qE = e * (V/d)

Las placas aplicarán dicha fuerza a los electrones por toda la duración en lo que los electrones
estén en el rango de coordenadas [L, 2L], donde L es la longitud de la placa (declarada en main)
"""

from constants import E

# Voltajes de las placas las definimos como [-1000, 1000] V
V_PLAQUE_MIN = -1000
V_PLAQUE_MAX = 1000

# Se ignora el valor de la carga fundamental en el cálculo de exertForce por
# la misma razón explicada en ElectronClass.py, estaba retornando valores
# muy altos, por lo que se consideraron unidades arbitrarias.
class Placa():
    def __init__(self, Z, volt): # en metros
        self.Z = Z
        self.y = 0
        self.voltage = volt
    
    def exertForce(self, twin, distance) -> float:
        return (self.voltage - twin.voltage)/distance
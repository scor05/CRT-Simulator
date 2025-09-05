""" 
Archivo que guarda las constantes físicas usadas en el simulador
"""

E = 1.602e-19 # Carga fundamental (reemplazada por 1, unidades arbitrarias)
M_E = 9.11e-31 # Masa del electrón (se reemplaza por 1 igualmente)
TUBE_LENGTH = 1 # longitud del tubo de rayos 
SCREEN_DIMENSIONS = 0.5 # anchura de la pantalla de vista frontal (es también igual a la altura)
PLAQUE_LENGTH = 0.2 # longitud de las placas cuadradas, para determinar por cuántos frames aplicarle fuerza al electrón
PLAQUE_SEPARATION = 0.05 # Distancia entre las placas 
HORIZONTAL_PLAQUES_Z = 0.3 # punto inicial de las placas horizontales
VERTICAL_PLAQUES_Z = 0.3 # punto inicial de las placas verticales
VOLTAGE_ACCEL_MAX = 3 # voltaje máximo del cañón
VOLTAGE_ACCEL_MIN = 1 # voltaje mínimo del cañón
VOLTAGE_SIDES_LIMIT = 1.1 # límite Vm para las placas
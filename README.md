<h1 align="center">📺 CRT-Simulator</h1>

<p align="center">
Simulador interactivo de un <b>Tubo de Rayos Catódicos (CRT en inglés, TRC en español)</b> en Python usando Pygame.<br>
Permite visualizar la trayectoria de electrones dentro del tubo, su interacción con placas deflectoras y su impacto en la pantalla.
</p>

<hr>

<h2>Funcionalidades</h2>
<ul>
  <li>Vistas simultáneas del TRC:
    <ul>
      <li>Vista Superior</li>
      <li>Vista Lateral</li>
      <li>Vista Frontal</li>
    </ul>
  </li>
  <li>Generación y actualización de electrones en tiempo real con física simplificada.</li>
  <li>Placas deflectoras horizontales y verticales que aplican campos eléctricos según el voltaje.</li>
  <li>Interfaz de control por teclado para modificar variables físicas en tiempo real.</li>
  <li>Persistencia visual de los electrones al impactar en la pantalla (brillo controlado por voltaje).</li>
  <li>Soporte para modos Manual y Sinusoidal.</li>
</ul>

<h2>Variables físicas controlables</h2>
<p>El usuario, mediante su teclado, puede controlar:</p>
<ul>
  <li><b>Voltaje de aceleración</b> (<code>Q/E</code>)</li>
  <li><b>Voltaje de deflexión horizontal</b> (<code>A/D</code>)</li>
  <li><b>Voltaje de deflexión vertical</b> (<code>W/S</code>)</li>
  <li><b>Modo Manual/Sinusoidal para el voltaje</b> (<code>M</code>)</li>
  <li><b>Frecuencia en eje X</b> (<code>F/G</code>)</li>
  <li><b>Frecuencia en eje Y</b> (<code>V/B</code>)</li>
  <li><b>Desfase</b> (<code>R/T</code>)</li>
  <li><b>Latencia de electrones en pantalla</b> (<code>Y/H</code>)</li>
</ul>

<h2>Controles de Usuario</h2>
Como se mencionó anteriormente, el usuario utiliza el teclado para manejar las propiedades de la simulación, por lo que a continuación se enlistan las disponibles:
(NOTA: La primera tecla aumenta el valor en cuestión, la segunda lo decrementa)
<pre>
Q/E: Voltaje aceleración
W/S: Voltaje vertical
A/D: Voltaje horizontal
M: Cambiar modo Manual/Sinusoidal
F/G: Frecuencia X
V/B: Frecuencia Y
R/T: Desfase
Z/X: Latencia en pantalla de cada electrón
</pre>

<h2>Requisitos</h2>
<ul>
  <li>Python 3.10+</li>
  <li><a href="https://www.pygame.org/">Pygame</a></li>
</ul>
<pre>
pip install pygame
</pre>

<h2>Ejecución</h2>
<pre>
git clone https://github.com/scor05/CRT-Simulator.git
cd CRT-Simulator
cd src
python src/main.py
</pre>

<h2>Estructura del proyecto</h2>
<pre>
CRT-Simulator/
│
├── main.py              # Loop principal y lógica de simulación
├── ElectronClass.py     # Clase Electron (posición, velocidad, dibujo)
├── PlacaClass.py        # Clase Placa (voltajes, cálculo de fuerza)
├── res/                 # Recursos gráficos (sprites, imágenes)
├── fonts/               # Tipografías usadas en interfaz
└── README.md            # Este archivo
</pre>

<h2>Créditos</h2>
<ul>
  <li>Desarrollado como proyecto para la clase de Física 3 en el segundo ciclo del 2025.</li>
  <li>Autor: Santiago <i>scor05</i> Cordero</li>
</ul>

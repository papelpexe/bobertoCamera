from vl53 import VL53L0X
from portas import Portas
from time import sleep
from defs import teclado

import threading

# distanciaGarra = VL53L0X(Portas.I2C3)
# distanciaLateral = VL53L0X(Portas.I2C4)
# distanciaFrente = VL53L0X(Portas.I2C1)
# distanciaLateral2 = VL53L0X(Portas.I2C7)
# # distanciaFrente = "pedrinho"
# # distanciaLateral = "pedrinho"

valorDistanciaFrente = 8000
valorDistanciaGarra = 8000
valorDistanciaLateral = 8000
valorDistanciaLateral2 = 8000

# def leDistanciaFrente(): 
#     """retorna o valor de distancia em mm"""

#     return distanciaFrente.read_range_single_millimeters()
#     # return "pedrinho"

#     # return "pedrinho"

# def leDistanciaGarra(): 
#     """retorna o valor de distancia em mm"""

#     return distanciaGarra.read_range_single_millimeters()

# def leDistanciaLateral(): 
#     """retorna o valor de distancia em mm"""

#     return distanciaLateral.read_range_single_millimeters()

# def leDistanciaLateral2(): 
#     """retorna o valor de distancia em mm"""

#     return distanciaLateral2.read_range_single_millimeters()


def thread_distancia():
    global valorDistanciaFrente, valorDistanciaGarra, valorDistanciaLateral, valorDistanciaLateral2
    sleep(1)
    
    while True:

        # valorDistanciaFrente = leDistanciaFrente()
        # valorDistanciaGarra = leDistanciaGarra()
        # valorDistanciaLateral = leDistanciaLateral()
        # valorDistanciaLateral2 = leDistanciaLateral2()

        ##atualiza nessa thread para evitar conflitos no barramento
        teclado.atualizaEstadoBotoes()
        teclado._atualizar_estado()
        
        sleep(0.02)

threadDistancia = None
def iniciarThreadDistancia():
        global threadDistancia
        """Inicia a thread para chamar `atualiza` periodicamente."""
        threadDistancia = threading.Thread(target=thread_distancia)
        threadDistancia.daemon = True  # Permite que o programa principal encerre mesmo com a thread ativa
        threadDistancia.start()

# Imports necessários para a comunicação serial
from motores import Motores
from time import time, sleep
from cronometro import Cronometro
from sensorCorReflexao import CorReflexao
from giroscopio import Giroscopio
from placaMuxVl53l0x import PlacaMuxVl53l0x
from placaMuxTCS34725 import PlacaMuxTCS34725
from portas import Portas
from teclado import Teclado
from tela import Tela
from tcs import TCS34725
from vl53 import VL53L0X
from botoes import Botoes

import threading
import ctypes

motores = Motores(True)
motores.direcao_motor(2, motores.NORMAL)
motores.direcao_motor(1, motores.INVERTIDO)
# motores.modoFreio(motores.HOLD)

motores.pid_motor(3,10,0)

sensorCor = CorReflexao(Portas.SERIAL1)
# #placaMuxLaser = PlacaMuxVl53l0x(Portas.SERIAL3)
giroscopio = Giroscopio(Portas.SERIAL4)
# #placaMuxCor = PlacaMuxTCS34725(Portas.SERIAL4)

velocidadeMotor1 = 80
velocidadeMotor2 = 80
posicaoServo1 = 0
tela = Tela()
teclado = Teclado()
teclado.botao_para_encerrar_programa(Teclado.ESC)

# botoes = Botoes()

#giroscopio: X e o eixo q usa na rampa, Z e o eixo q usa nos giros

# ========== SISTEMA DE PARADA ELEGANTE ==========
class ThreadStopSignal(Exception):
    """Exceção para parada elegante da thread"""
    pass

class ThreadAsyncController:
    def __init__(self):
        self.thread_id = None
        self.stop_requested = False
    
    def register_thread(self):
        """Registra a thread para poder pará-la via exceção assíncrona"""
        self.thread_id = threading.get_ident()
        self.stop_requested = False
    
    def stop_thread(self):
        """Para a thread levantando exceção nela de forma assíncrona"""
        if self.thread_id and not self.stop_requested:
            self.stop_requested = True
            print(f"🎯 Enviando exceção assíncrona para thread {self.thread_id}")
            
            # Método 1: Usando ctypes (mais direto)
            try:
                result = ctypes.pythonapi.PyThreadState_SetAsyncExc(
                    ctypes.c_long(self.thread_id), 
                    ctypes.py_object(ThreadStopSignal)
                )
                if result == 0:
                    print("❌ Thread não encontrada ou já terminou")
                elif result > 1:
                    print("⚠️  Múltiplas exceções, restaurando...")
                    ctypes.pythonapi.PyThreadState_SetAsyncExc(self.thread_id, None)
            except Exception as e:
                print(f"❌ Erro no método ctypes: {e}")
                # Método 2: Fallback usando flag
                self.stop_requested = True

# Instância global do controlador
thread_controller = ThreadAsyncController()
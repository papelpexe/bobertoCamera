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


motores = Motores(True)
motores.direcao_motor(2, motores.INVERTIDO)
motores.direcao_motor(1, motores.NORMAL)
# motores.modoFreio(motores.HOLD)

# motores.PIDMotor(3,3,3)

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

def pausa():
    #pausa o codigo apertando um botao
    pass
    # if (teclado.botaoPressionado(Teclado.CIMA)):
    #     motores.paraMotores()
    #     tela.escreve("codigo pausado", 1)
    #     sleep(0.2) 
    #     while True:
    #         if (teclado.botaoPressionado(Teclado.CIMA)): 
    #             sleep(0.2) 
    #             break
    #         pass
            
    #     tela.apaga(1)


# tela.escreve("esperando apertar botao", 0)
    
        # while not (teclado.botaoPressionado(Teclado.ENTER)) and not iniciaDireto:
        #     sleep(0.1)
        # sleep(0.3)
        

        # if (teclado.botaoPressionado(Teclado.ENTER)) or iniciaDireto:
        #     iniciarThreadMain()
        #     iniciaDireto = False

        # else: continue
        # sleep(1.5)
        
        # while not (teclado.botaoPressionado(Teclado.ENTER)):
        #     sleep(0.1)


        # sleep(0.5)
        # if (teclado.botaoPressionado(Teclado.ENTER)):
        #     tela.escreve("", 0)
        #     matarThreadMain()
        #     sleep(0.3)
        #     while flagThreadMorreu == False:
        #         continue
        #     flagThreadMorreu = False
        #     mov.motores.paraMotores()
        #     sleep(0.3)
            

        #     print("\nInterrupção detectada! Parando os motores e entrando em modo de espera")
        #     # debug.apagarTodosLeds()
        #     # # Parar os motores
        #     # motores.desligaMotores()
        #     # #desativo todos os servos
        #     # motores.desativaServo(1)
        #     # motores.desativaServo(2)
        #     # motores.desativaServo(3)
        #     # motores.desativaServo(4)
        #     # motores.desativaServo(5)
        #     # motores.desativaServo(6)
        #     # print("Programa encerrado com segurança.")
        #     #    subprocess.run(["killall python3", None], check=True)

        # else: continue
        # sleep(1.5)
        
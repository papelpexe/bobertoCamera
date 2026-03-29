from defs import sleep
sleep(2)
#sudo dmesg

#pra logar: ssh banana@192.168.1.113
#pra entrar no ambiente especifico do pyhton: source meu_venv/bin/activate
#source meu_venv/bin/activate
#sudo shutdown now

#ordem dos botoes 
#ESC ENTER UP DOWN

import threading
from defs import tela
from defs import teclado
from defs import Teclado
from defs import motores
import movimentos as mov
import constantes as const
from defs import giroscopio, thread_controller
import defs
import funcs
import crono as cr
import sensor as se
import dist
import conds
import debug
import random
import servos as ser
import conds as con
import sys
import ctypes

import camera

import codigo


## thread principal que contem o funcionamento do robo
def thread_main():
    codigo.main()

threadMain = None
def iniciarThreadMain():
    global threadMain, threadRunning
    print("iniciou thread main")
    threadMain = threading.Thread(target=thread_main)
    threadMain.daemon = True
    threadRunning = True
    thread_controller.stop_requested = False  # Reseta flag
    threadMain.start()

def matarThreadMain():
    global threadMain, threadRunning
    print("Solicitando parada da thread main...")
    threadRunning = False
    
    # Para a thread de forma assíncrona
    thread_controller.stop_thread()
    
    if threadMain and threadMain.is_alive():
        threadMain.join(timeout=2)  # Timeout de segurança
        if threadMain.is_alive():
            print("Thread não respondeu - forçando parada")
            # Força parada se necessário
        else:
            print("Thread main parada com sucesso!")

iniciaDireto = False   
if len(sys.argv) >= 2:
    iniciaDireto = True

## loop onde podemos reinicar o codigo matando todas as threads, e reiniciar, apenas aoertando o botao enter
try:   
    flagThreadMorreu = False

    print("Exemplo processamento de IA encontrando posição dos objetos detectados na camera")
    # o código do flask deve ser iniciado em uma thread separada para poder rodar junto com o código principal
    flask_thread = threading.Thread(target=camera.iniciar_flask)
    flask_thread.daemon = True
    flask_thread.start()

    camera.iniciarThreadCamera()
    sleep(1)
    # cr.iniciarThreadParachoque()
    # cr.iniciarThreadCronometros()
    # dist.iniciarThreadDistancia()
    # mov.iniciarThreadAnguloMotores()
    coiso = True
    while True:
        tela.escreve('esperando')

        while True:
            if (teclado.botao_pressionado(Teclado.ENTER)) or coiso :
                coiso = False
                break
            sleep(0.1)  # Pequeno sleep para não sobrecarregar

        sleep(0.5)
        iniciarThreadMain()
        tela.escreve('rodando codigo')

        while True:
            if (teclado.botao_pressionado(Teclado.ENTER)):
                break
            sleep(0.1)  # Pequeno sleep para não sobrecarregar

        sleep(0.5)
        matarThreadMain()

except KeyboardInterrupt as e:
    mov.motores.para_motores()
    print("\nInterrupção detectada! Parando os motores e encerrando...")
    debug.apagarTodosLeds()
    # Parar os motores

    #desativo todos os servos
    motores.desativa_servo(1)
    motores.desativa_servo(2)
    motores.desativa_servo(3)
    motores.desativa_servo(4)
    motores.desativa_servo(5)
    motores.desativa_servo(6)
    print("Programa encerrado com segurança.")
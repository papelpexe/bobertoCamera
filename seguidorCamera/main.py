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
from defs import giroscopio
import defs
import funcs
import crono as cr
import sensor as se
import dist
import conds
import area
import camera
import processOpenCv
import debug
import random
import servos as ser
import conds as con
import sys

def seguidorDeLinha():

    """funcao contendo todas as outras funcoes que checam e realizam os movimentos necessarios de acordo com os perigos da pista"""

    funcs.verdes()
    funcs.intercessao()

    ## segue linha continua
    mov.pid() 
    # funcs.motoresTravados()

threadRunning = False
def main():
    global flagThreadMorreu

    """funcao que contem todo o funcionamento do robo em um loop"""
    

    # inicia thread do flask
    print("Exemplo processamento de IA encontrando posição dos objetos detectados na camera")
    # o código do flask deve ser iniciado em uma thread separada para poder rodar junto com o código principal
    flask_thread = threading.Thread(target=camera.iniciar_flask)
    flask_thread.daemon = True
    flask_thread.start()
    # # input()
    
    ## RESETA AS VARIAVEIS NECESSARIAS E POSICIONA OS SERVOS EM SUAS RESPECTIVAS POSICOES
    debug.piscarLed(1)
    giroscopio.reseta_z()
    debug.apagarTodosLeds()
    ser.subirGarra()
    ser.abrirGarra()
    ser.fecharPorta()
    mov.m.para_motores()
    motores.set_modo_freio(0)
    count = 0
    const.contadorGap = 0
    # area.vitimasCapturadas = []
    # area.vitimasEntregues = False
    # area.fugiuDaArea = False
    run = 1

    sleep(1)
  
    tela.escreve("MAIN", 0)
    count = 1

    while run == 1 and threadRunning:
        pass
        ser.m.atualiza_servos() ## joga o servos na posicao correta, para remediar os espasmos

        seguidorDeLinha()

    # debug.piscarLed(1)
    mov.m.para_motores()
    flagThreadMorreu = True

## thread principal que contem o funcionamento do robo
def thread_main():
    main()

threadMain = None
def iniciarThreadMain():
    global threadMain, threadRunning
    print("iniciou thread main")
    threadMain = threading.Thread(target=thread_main)
    threadMain.daemon = True
    threadRunning = True
    threadMain.start()

def matarThreadMain():


    global threadMain, threadRunning
    threadRunning = False

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


    while True:
        seguidorDeLinha()
        # motores.atualiza_motores()
        # print(motores.estado_motor(1))
        
        

except KeyboardInterrupt as e:
    mov.motores.para_motores()
    print("\nInterrupção detectada! Parando os motores e encerrando...")
    debug.apagarTodosLeds()
    # Parar os motores
    motores.desligaMotores()
    #desativo todos os servos
    motores.desativaServo(1)
    motores.desativaServo(2)
    motores.desativaServo(3)
    motores.desativaServo(4)
    motores.desativaServo(5)
    motores.desativaServo(6)
    print("Programa encerrado com segurança.")
#    subprocess.run(["killall python3", None], check=True)
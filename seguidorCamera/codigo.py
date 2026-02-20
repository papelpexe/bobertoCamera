import threading
from defs import tela
from defs import teclado
from defs import Teclado
from defs import motores
import movimentos as mov
import constantes as const
from defs import giroscopio
from time import sleep
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

import area
import camera as cam
import processOpenCv as pcv2


def seguidorDeLinha():
    """funcao contendo todas as outras funcoes que checam e realizam os movimentos necessarios de acordo com os perigos da pista"""

    # #python3 ~/seguidorCamera/main.py
    funcs.verdes()
    funcs.intercessao()
    # funcs.pararNoVermelhoCamera()
    # #processOpenCv.detectaPrata(camera.getFrameAtual())
    # if processOpenCv.verificaLinhaPreta(camera.getFrameAtual()):
    #     print("LINHA PRETA DETECTADA")
    # sleep(1)
    # if processOpenCv.contains_silver(camera.getFrameAtual()):
    #     print("PRATA DETECTADA")
    #segue linha continua
    mov.pid()
    # for i in range(5):
    #     processOpenCv.salvaImagem(f"frame_teste_{random.randint(0,1000)}.png", "Imagens")
    


threadRunning = False
def main():
    global flagThreadMorreu

    """funcao que contem todo o funcionamento do robo em um loop"""

    
    # Registra a thread para poder pará-la
    defs.thread_controller.register_thread()
    
    ## RESETA AS VARIAVEIS NECESSARIAS E POSICIONA OS SERVOS EM SUAS RESPECTIVAS POSICOES
    debug.piscarLed(1)
    giroscopio.reseta_z()
    mov.m.para_motores()
    const.contadorGap = 0

    sleep(1)

    tela.escreve("MAIN", 0)

    try:
        # giroscopio.calibra()
        r=g=b=0
        while True:
            #VERIFICAÇÃO NO LOOP PRINCIPAL (obrigatória)
            if defs.thread_controller.stop_requested:
                raise defs.ThreadStopSignal("Parada solicitada no loop principal")
            
            # ser.m.atualiza_servos() ## joga o servos na posicao correta, para remediar os espasmos
            seguidorDeLinha()
            val = 255
            motores.set_led_rgb_all(val,val,val)
            # vdetectados = pcv2.checarVerdes(cam.getFrameAtual())

            # print(giroscopio.le_angulo_z())
            # mov.m.velocidade_motores_4x4(100,100)
            # sleep(4)
            # mov.m.velocidade_motores_4x4(50,50)
            # sleep(4)    
            # mov.m.velocidade_motores_4x4(-50,-50)
            # sleep(4)
            # mov.m.velocidade_motores_4x4(-100,-100)
            # sleep(4)

            # mov.reto(10)
            # sleep(1)
            # mov.reto(10,const.TRAS)
            # sleep(1)

            # cam.frameProcessado = cam.frame

            # r=b=g=g+10
            # if g>255:
            #     g=0
            #     r=0
            #     b=0
            
            # sleep(0.1)

           
    except defs.ThreadStopSignal:
        print("Thread main parada elegantemente!")
    except KeyboardInterrupt:
        print("Interrupção via Ctrl+C")
    finally:
        # Limpeza garantida
        debug.piscarLed(1)
        mov.m.set_modo_freio(1)
        mov.m.para_motores()
        mov.m.set_modo_freio(0)
        flagThreadMorreu = True
        print("Thread main finalizada com segurança!")
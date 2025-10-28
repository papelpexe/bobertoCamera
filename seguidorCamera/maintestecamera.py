import camera
import processOpenCv
import threading
import cv2
import time
import numpy as np
import cronometro
from giroscopio import Giroscopio
from portas import Portas

import motores

m = motores.Motores(True)
m.direcao_motor(1, m.NORMAL)
m.direcao_motor(2, m.INVERTIDO)

giro = Giroscopio(Portas.SERIAL4)

# python3 ~/seguidorCamera/maintestecamera.py

print("Exemplo processamento de IA encontrando posição dos objetos detectados na camera")

# Start Flask in a separate thread
flask_thread = threading.Thread(target=camera.iniciar_flask)
flask_thread.daemon = True
flask_thread.start()

# Start camera thread
camera.iniciarThreadCamera()

# Wait a moment for camera to initialize
time.sleep(2)

print("Starting main processing loop...")
erro = 0
erroAnterior = erro

contaciclos = cronometro.Cronometro()
contaciclos.inicia()

def girar_angulo(vel, angulo, dir = 'esq'):

    if dir == 'dir':
        vel = -vel

    m.set_modo_freio(1)
    m.para_motores()
    giro.reseta_z()

    while abs(giro.le_angulo_z()) < angulo:
        print(giro.le_angulo_z())
        m.potencia_motores_4x4(vel,-vel)

    m.para_motores()
    m.set_modo_freio(0)

def girarGraus(direc, graus, vb = 50 + 25, cond = None, cond2 = None, conds = [], cronos = [], delta = 0, hold = True):
    if hold == True: 
        m.set_modo_freio(1)
    m.para_motores()
    # print("potencia dos motores:",  vb)

    # print("girando")
    # print(giroscopio.leAnguloZ())

    giro.reseta_z()
    giro.reseta_z()
    para = False

    while graus > abs(giro.le_angulo_z()):
        # cr.reset()
        # print(angFinal, giroscopio.leAnguloZ())
        if direc == 'esq':
            if graus*0.8 < abs(giro.le_angulo_z()):
                m.velocidade_motores_4x4(2*vb/3, -2*vb/3 - delta)

            else: m.velocidade_motores_4x4(vb, -vb - delta)

        elif direc == 'dir':
            if graus*0.8 < abs(giro.le_angulo_z()):
                m.velocidade_motores_4x4(-2*vb/3, 2*vb/3 - delta)

            else: m.velocidade_motores_4x4(-vb, vb + delta)

        if cond and cond():  
            print("pegou cond do giro")
            break
        if cond2 and cond2():  
            print("pegou cond 2 do giro")
            break

        for c in conds:
            if c and c():  
                print("pegou uma das conds do reto")
                para = True

        for c in cronos:
            if c.tempo() < 100:  
                print("pegou um dos cronos do reto")
                para = True

        if para:
            break

    m.para_motores()
    if hold: time.sleep(0.1)
    m.set_modo_freio(0)
    # print(giroscopio.leAnguloZ())

def vendoPreto():
    dec = processOpenCv.verificaIntercessao2(camera.getFrameAtual())
    print(dec)
    if dec == 'nada':
        return True
    else: return False

def reto(cm, vel = 30, dir = 'frente'):
    ang = cm * 15

    if dir == 'frente':

        m.reseta_angulo_motor(1)
        m.reseta_angulo_motor(2)
        while m.angulo_motor(1) < ang and m.angulo_motor(2) < ang:
            m.velocidade_motores_4x4(vel, vel)

    elif dir == 'tras':

        m.reseta_angulo_motor(1)
        m.reseta_angulo_motor(2)
        while m.angulo_motor(1) > -ang and m.angulo_motor(2) > -ang:
            m.velocidade_motores_4x4(-vel, -vel)

    m.para_motores()
    m.set_modo_freio(0)

giro.calibra()

while True:
    try:
        # Get the current frame from the camera module
        frame = camera.getFrameAtual()
        
        if frame is not None:
            pass
            
            # Update the processed frame that will be streamed
            # with camera.lock:
            #     camera.frameProcessado = binaria
            
            erro = int(processOpenCv.seguidor_centro(frame))
            # erro = 0

            #lado direito e negativo
            
           
 
        time.sleep(0.033/2)  # ~30 (60) FPS processing

        kp = 0.45
        kd = 1.9
        p = erro * kp
        d = (erro - erroAnterior) * kd

        valor = p + d #variacao da potencia do motor
       
        # print(se.leReflexaoTodos())
        # print(erro, p, d, valor, kp, kd)
        vb = 40
        # if erro < 0:
        #     valorMotorEsq = vb - valor
        #     valorMotorDir = vb
        # elif erro > 0:
        #     valorMotorEsq = vb 
        #     valorMotorDir = vb + valor
        # else: 
        #     valorMotorEsq = vb
        #     valorMotorDir = 

        valorMotorEsq = vb - valor  
        valorMotorDir = vb + valor

        # minVel = 15
        # if valorMotorDir < minVel:
        #     valorMotorDir = minVel
        # if valorMotorEsq < minVel:
        #     valorMotorEsq = minVel


        m.potencia_motores_4x4(valorMotorEsq, valorMotorDir)
        erroAnterior = erro

        # print(erro, valor)
        decisao = processOpenCv.verificaIntercessao2(frame)

        if decisao == 'esq':
            print(decisao)
            # reto(1)
            girarGraus('esq', 90, cond = vendoPreto)

        if decisao == 'dir':
            print(decisao)
            # reto(1)
            girarGraus('dir', 90, cond = vendoPreto)

        # print(decisao)

        # print(giro.le_angulo_z())
        


        
    except KeyboardInterrupt:
        print("Stopping...")
        break
    except Exception as e:
        print(f"Error in main loop: {e}")
        time.sleep(1)
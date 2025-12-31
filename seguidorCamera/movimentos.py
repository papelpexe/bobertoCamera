import threading
import time
from defs import motores
from defs import giroscopio
from defs import sleep
import sensor as se
from constantes import ESQ, DIR, FRENTE, TRAS, DELTA, VERDE, VERMELHO, PRATA
import crono as cr

from defs import teclado as tcl

import camera as cam
import processOpenCv as pcv2

m = motores
motorEsquerdoTravado = False
motorDireitoTravado = False
#motor esquerdo vai ser o 1 e o direito o 2

kp = 0.6
ki = 0
kd = 1.9

vb_pid = 65

erroAnterior = 0
integral = []
def pid():
    global erroAnterior, integral

    erro = pcv2.seguidor_centro(cam.getFrameAtual())

    p = erro * kp

    integral.append(erro)
    if len(integral) > 20: integral.pop(-1)

    somaInt = sum(integral)
    
    if somaInt > 100: somaInt = 50
    if somaInt < -100: somaInt = -50

    i = somaInt * ki

    d = (erro - erroAnterior) * kd
    
    valor = p + i + d #variacao da potencia do motor
    # print(se.leReflexaoTodos())

    valorMotorEsq = vb_pid + valor  
    valorMotorDir = vb_pid - valor


    m.potencia_motores_4x4(valorMotorEsq, valorMotorDir)
    erroAnterior = erro

def pidPorDistancia(cm, direc = FRENTE, vb = vb_pid, cond = None, cond2 = None, cronos = [], conds = []):
    m.para_motores()
    
    anguloEsq = m.angulo_motor(1)
    anguloDir = m.angulo_motor(2)

    quant = indiceDoReto * cm
    para = False

    while True: 
        global erroAnterior

        erro = pcv2.seguidor_centro(cam.getFrameAtual())

        if direc ==FRENTE: 
            kpDist = kp - 0.15
            kdDist = kd + 3
        else:
            kpDist = kp - 0.45
            kdDist = kd + 5
        
    
        p = erro * (kpDist - 0.15)
        d = (erro - erroAnterior) * (kdDist + 3)
        
        vb_pid = vb
        valor = p + d #variacao da potencia do motor
        # print(se.leReflexaoTodos())

        if direc == FRENTE: m.velocidade_motores_4x4(vb_pid - valor, vb_pid + valor)
        else: 
            valor = -valor
            m.potencia_motores_4x4(-vb_pid + valor, -vb_pid - valor)

        if cond and cond():

            print("pegou cond do reto")
            break
        if cond2  and cond2():  
            print("pegou cond2 do reto")
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

        if direc == FRENTE:
            if (anguloEsq + quant <= m.angulo_motor(1)) and (anguloDir + quant <= m.angulo_motor(2)):
                break
        else:
            if (anguloEsq - quant >= m.angulo_motor(1)) and (anguloDir - quant >= m.angulo_motor(2)):
                break

        erroAnterior = erro

    m.para_motores()

def andaMotor(motor, cm, direc = FRENTE, vb = 50, conds = [], cronos = []):

    anguloEsq = m.angulo_motor(1)
    anguloDir = m.angulo_motor(2)

    quant = indiceDoReto * cm

    para = False

    if motor == ESQ:
        while True:

            if direc == FRENTE:
                m.velocidade_motores_4x4(1, vb)
                if (anguloEsq + quant <= m.angulo_motor(1)):
                    break
            else:
                m.velocidade_motores_4x4(1, -vb)
                if (anguloEsq - quant >= m.angulo_motor(1)):
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

    if motor == DIR:
        while True:
            
            if direc == FRENTE:
                m.velocidade_motores_4x4(2, vb)
                if (anguloDir + quant <= m.angulo_motor(2)):
                    break
            else:
                m.velocidade_motores_4x4(2, -vb)
                if (anguloDir - quant >= m.angulo_motor(2)):
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
    

indiceDoReto = 7
def retoAntigo(cm, direc = FRENTE, vb = vb_pid + 15, hold = True, cond = None, cond2 = None, conds = [], cronos = [], delta = 1.1):
    if hold: m.set_modo_freio(1)
    m.para_motores()

    anguloEsq = m.angulo_motor(1)
    anguloDir = m.angulo_motor(2)
    
    vel = vb

    print("anda reto")
    quant = int(cm * indiceDoReto) #valor encontrado por meio de testes


    para = False
    counter = 0
    cr.espera.reseta()
    while True:
        if cond and cond():  
            print("pegou cond do reto")
            break
        if cond2 and cond2():  
            print("pegou cond2 do reto")
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

        if direc == FRENTE: m.velocidade_motores_4x4(vel, vel * delta)
        else: 
            m.velocidade_motores_4x4(-vel, -(vel) * delta)


        if direc == FRENTE:
            if (anguloEsq + quant <= m.angulo_motor(1)) and (anguloDir + quant <= m.angulo_motor(2)):
                break
        else:
            if (anguloEsq - quant >= m.angulo_motor(1)) and (anguloDir - quant >= m.angulo_motor(2)):
                break
        counter += 1
        if cr.espera.tempo() > 10000: 
            print("tempo demais no loop do reto")
            break
            # raise Exception("tempo demais no loop do reto")
 
    # print("numero de loops do reto: ", counter)
        
    m.para_motores()
    m.set_modo_freio(0)

#função de andar reto com graus kp kd

def reto(cm, direc = FRENTE, vb = 100, hold = False, cond = None, cond2 = None, conds = [], cronos = []):
    if hold: m.set_modo_freio(1)
    m.para_motores()

    giroscopio.reseta_z()#resetar o angulo (não lembro se é o z))
    erroAnterior=0

    anguloEsq = m.angulo_motor(1)
    anguloDir = m.angulo_motor(2)

    vel = vb

    print("anda reto")
    quant = int(cm * indiceDoReto) #valor encontrado por meio de testes


    para = False
    counter = 0
    cr.espera.reseta()
    while True:
        
        if cond and cond():  
            print("pegou cond do reto")
            break
        if cond2 and cond2():  
            print("pegou cond2 do reto")
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

        
        if direc == FRENTE:
            erro=giroscopio.le_angulo_z()
            kp= 1
            kd= 1
            p = erro * kp
            d = (erro - erroAnterior) * kd
            valor = p + d
            valorMotorEsq=vb_pid - valor  
            valorMotorDir=vb_pid + valor
            
            m.velocidade_motores_4x4(valorMotorEsq, valorMotorDir)
            erroAnterior = erro

        else: 
            erro=0-(giroscopio.le_angulo_z())
            kp= 1
            kd= 1
            p = erro * kp
            d = (erro - erroAnterior) * kd
            valor = p + d
            valorMotorEsq=vb_pid + valor  
            valorMotorDir=vb_pid - valor
            
            m.velocidade_motores_4x4(-valorMotorEsq, -valorMotorDir)
            erroAnterior = erro

        if direc == FRENTE:
            if (anguloEsq + quant <= m.angulo_motor(1)) and (anguloDir + quant <= m.angulo_motor(2)):
                break
        else:
            if (anguloEsq - quant >= m.angulo_motor(1)) and (anguloDir - quant >= m.angulo_motor(2)):
                break
        counter += 1
        print(m.angulo_motor(1), m.angulo_motor(2))
        if cr.espera.tempo() > 10000: 
            print("tempo demais no loop do reto")
            break
            # raise Exception("tempo demais no loop do reto")
 
    # print("numero de loops do reto: ", counter)
        
    m.para_motores()
    # m.set_modo_freio(0)

def girarGraus(direc, graus, vb = 100, cond = None, cond2 = None, conds = [], cronos = [], delta = 0, hold = False):
    if hold == True: 
        m.set_modo_freio(1)
    m.para_motores()
    # print("potencia dos motores:",  vb)

    # print("girando")
    # print(giroscopio.leAnguloZ())

    giroscopio.reseta_z()
    giroscopio.reseta_z()
    para = False

    while graus > abs(giroscopio.le_angulo_z()):
        # cr.reset()
        # print(angFinal, giroscopio.leAnguloZ())
        if direc == DIR:
            if graus*0.8 < abs(giroscopio.le_angulo_z()):
                m.velocidade_motores_4x4(2*vb/3, -2*vb/3 - delta)

            else: m.velocidade_motores_4x4(vb, -vb - delta)

        elif direc == ESQ:
            if graus*0.8 < abs(giroscopio.le_angulo_z()):
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
    if hold: sleep(0.1)
    m.set_modo_freio(0)
    # print(giroscopio.leAnguloZ())

def curvarGraus(direc, graus, vb = 100, cond = None, cond2 = None, conds = [], cronos = [], delta = 0, hold = False):
    if hold == True: 
        m.set_modo_freio(1)
    m.para_motores()
    # print("potencia dos motores:",  vb)

    # print("girando")
    # print(giroscopio.leAnguloZ())

    giroscopio.reseta_z()
    giroscopio.reseta_z()
    para = False


    print('iniciou curva')

    while graus > abs(giroscopio.le_angulo_z()):
        # cr.reset()
        # print(angFinal, giroscopio.leAnguloZ())
        if direc == ESQ:
            if graus*0.8 < abs(giroscopio.le_angulo_z()):
                m.velocidade_motores_4x4(vb, int(vb/5))

            else: m.velocidade_motores_4x4(vb, int(vb/5))

        elif direc == DIR:
            if graus*0.8 < abs(giroscopio.le_angulo_z()):
                m.velocidade_motores_4x4(int(vb/5), vb)

            else: m.velocidade_motores_4x4(int(vb/5), vb)

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
    
    print('acabou curva')

    m.para_motores()
    if hold: 
        sleep(0.1)
        m.set_modo_freio(0)
    # print(giroscopio.leAnguloZ())

esperaFreio = cr.Cronometro()
esperaFreio.inicia()
def freiar(velInicial = 50, velFinal = 0, desaceleracao = 15, tempo = 200, delta = 1):

    vel = velInicial
    while True:
        esperaFreio.reseta()
        m.velocidade_motores_4x4(vel,vel * delta)
        while esperaFreio.tempo() < tempo:
            pass
        vel -= desaceleracao

        if velFinal >= vel: break

angulo_motorEsquerdo = 0
angulo_motorDireito = 0
def checarAnguloDosMotores():
    global angulo_motorEsquerdo
    global angulo_motorDireito

    # m.estado()
    if abs(m.angulo_motor(1) - angulo_motorEsquerdo) < 5:tcl.alteraLed(3, 1)
    else: cr.motorEsquerdoTravado.reseta(); tcl.alteraLed(3, 0)

    if abs(m.angulo_motor(2) - angulo_motorDireito) < 5: tcl.alteraLed(3, 1)
    else: cr.motorDireitoTravado.reseta(); tcl.alteraLed(3, 0)
    # print(m.angulo_motor(1), m.angulo_motor(2))

    angulo_motorEsquerdo = m.angulo_motor(1)
    angulo_motorDireito = m.angulo_motor(2)
    
def thread_angulo_motores():
    while True:
        checarAnguloDosMotores()
        time.sleep(0.01)

def iniciarThreadangulo_motores():
    print("iniciou thread angulo_motores")
    threadAngulos = threading.Thread(target=thread_angulo_motores)
    threadAngulos.daemon = True
    threadAngulos.start()
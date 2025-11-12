import movimentos as mov
import sensor
import dist
import crono as cr
import constantes as const
from constantes import ESQ, DIR, FRENTE, TRAS
from time import sleep

import conds as con

from defs import teclado as tcl
from defs import Teclado
from defs import tela

from defs import giroscopio as giro
import camera as cam
import processOpenCv as pcv2

andada = 2.6
andadaVerde = 3.5
volta = 1


def intercessao():
    decisao = pcv2.verificaIntercessao(cam.getFrameAtual())

    if decisao == ESQ:
        print('esq')
        # reto(1)
        mov.girarGraus(ESQ, 90, cond = con.vendoPreto)

    if decisao == DIR:
        print('dir')
        # reto(1)
        mov.girarGraus(DIR, 90, cond = con.vendoPreto)


def verdes():
    vdetectados = pcv2.checarVerdes(cam.getFrameAtual())

    vEsq = False
    vDir = False

    if len(vdetectados) > 0:
        for v in vdetectados:
            if v == 'verde dir':
                vDir = True
            elif v == 'verde esq':
                vEsq = True

    if vEsq and not vDir: ##verde na esquerda
        mov.reto(5)
        mov.girarGraus(ESQ, 50)
        mov.girarGraus(ESQ, 40, cond = con.vendoPreto)

    elif vDir and not vEsq: ##verde na direita
        mov.reto(5)
        mov.girarGraus(DIR, 50)
        mov.girarGraus(DIR, 40, cond = con.vendoPreto)

    elif vDir and vEsq: ##180
        mov.girarGraus(ESQ, 180)
        mov.girarGraus(ESQ, 20, cond = con.vendoPreto)


def gap(): ## TEM QUE FAZER A VARREDURA DPS

    if cr.fezGap.tempo() > 3000:
        const.contadorGap = 0

    if con.tudoBranco():
        # mov.reto(3, conds = [con.viuMeioPreto])

        if cr.VerdeEs.tempo() < cr.VerdeDir.tempo():
            mov.girarGraus(ESQ, 90, conds = [con.viuPreto, con.viuVermelho])
            if con.tudoBranco():
                mov.girarGraus(DIR, 180, conds = [con.viuPreto, con.viuVermelho])
                if con.tudoBranco(): mov.girarGraus(ESQ, 90, conds = [con.viuPreto, con.viuVermelho])
        elif cr.VerdeEs.tempo() > cr.VerdeDir.tempo():
            mov.girarGraus(DIR, 90, conds = [con.viuPreto, con.viuVermelho])
            if con.tudoBranco(): 
                mov.girarGraus(ESQ, 180, conds = [con.viuPreto, con.viuVermelho])
                if con.tudoBranco(): mov.girarGraus(DIR, 90, conds = [con.viuPreto, con.viuVermelho])
        

        if con.viuPreto() == False:

            print("confere gap")
            mov.reto(13, conds = [con.meioBrancoFalso, con.viuVermelho])

            if con.meioBranco():
                print("gap falso, se perdeu")
                const.contadorGap += 1
                cr.fezGap.reseta()
                mov.reto(15, TRAS, vb = 70, conds = [con.meioBrancoFalso, con.parachoqueApertadoTras, con.viuVermelho])
                mov.pidPorDistancia(3, TRAS, conds = [con.parachoqueApertadoTras, con.viuVermelho])
                # if con.meioBrancoFalso() == False:
                #     mov.reto(4, TRAS)
                # if 
                #     mov.girarGraus(DIR, 5)
                # elif sensor.erro_pid() < -20:
                #     mov.girarGraus(ESQ, 5)
        
            else: 
                print("gap verdadeiro")
                const.contadorGap = 0

    
def pararNoVermelho():
    if con.viuVermelho():
        print(sensor.leHSVtodos())
        mov.m.modoFreio_(1)
        mov.m.paraMotores()
        sleep(0.3)
        mov.m.modoFreio_(0)

        validarVermelho = True

        if not(con.viuVermelho()):
            mov.reto(1, FRENTE, 10, cond = con.viuVermelho)
            mov.reto(3, TRAS, 10, cond = con.viuVermelho)
            mov.motores.paraMotores()
        print("viu vermelho")
        
        esperaVermelho = cr.Cronometro()
        esperaVermelho.reseta()
        while esperaVermelho.tempo() < 1500:
            if not(con.viuVermelho()):
                validarVermelho = False
                print("falso vermelho")
                break

        if validarVermelho == True:
            mov.motores.paraMotores()
            print("finalizou a pista")
            while True:
                if (tcl.botaoPressionado(Teclado.CIMA)): 
                    sleep(0.2) 
                    break
                pass


esperaRampa = cr.Cronometro()
esperaRampa.inicia()
def rampa():
    # print(giro.leAnguloX())

    #rampa subida
    if giro.leAnguloX() > 15:
        # tcl.alteraLed(1, 1)
        # mov.m.modoFreio_(0)
        
        cr.RampaSubiu.reseta()

        erroAnterior = 0
        print("subida da rampa")
        while True:
            esperaRampa.reseta()

            ##PID DA RAMPA
            kp = 0.65
            kd = 2
            erro = sensor.erro_pid()

            p = erro * kp 
            d = (erro - erroAnterior) * kd
            
            valor = p + d #variacao da potencia do motor
            valor = int(valor)

            vb_pid = 60

            valMotorEsq = vb_pid - valor
            valMotorDir = vb_pid + valor

            maxvb = 80
            minvb = 20

            if valMotorEsq <  minvb: valMotorEsq = minvb
            if valMotorDir <  minvb: valMotorDir = minvb

            if valMotorEsq >  maxvb: valMotorEsq = maxvb
            if valMotorDir >  maxvb: valMotorDir = maxvb

            mov.motores.velocidadeMotores(valMotorEsq, valMotorDir)

            erroAnterior = erro

            if giro.leAnguloX() > 15:
                cr.RampaSubiu.reseta()
                
            if cr.RampaSubiu.tempo() > 100:
                print("saiu da subida da rampa")
                # mov.reto(4, TRAS)
                # tcl.alteraLed(1, 0)
                # mov.reto(3, TRAS)
                break

            tcl.alteraLed(1, 1)

            # while esperaRampa.tempo() < 100:
            #     pass

            # print(cr.RampaSubiu.tempo())

    #rampa descida
    if giro.leAnguloX() < -15:
        # mov.m.modoFreio_(0)
        # tcl.alteraLed(1, 1)

        cr.RampaDesceu.reseta()

        
        # mov.freiar(35, -15, 10, 150)
        mov.reto(3, TRAS, 35, hold = False)

        erroAnterior = 0
        print("descida da rampa")

        while True:

            esperaRampa.reseta()

            ##PID DA RAMPA
            kp = 0.7
            kd = 2
            erro = sensor.erro_pid()
        
            p = erro * kp 
            d = (erro - erroAnterior) * kd
            
            valor = p + d #variacao da potencia do motor
            valor = int(valor)

            vb_pid = 15

            valMotorEsq = vb_pid - valor
            valMotorDir = vb_pid + valor

            maxvb = 60
            minvb = 10

            if valMotorEsq <  minvb: valMotorEsq = minvb
            if valMotorDir <  minvb: valMotorDir = minvb

            if valMotorEsq >  maxvb: valMotorEsq = maxvb
            if valMotorDir >  maxvb: valMotorDir = maxvb

            mov.motores.velocidadeMotores(valMotorEsq, valMotorDir)


            erroAnterior = erro

            if giro.leAnguloX() < -15:
                cr.RampaDesceu.reseta()
                
            if cr.RampaDesceu.tempo() > 100:
                print("saiu da descida da rampa")
                tcl.alteraLed(1, 0)
                break

            # tcl.alteraLed(1, 1)

            # while esperaRampa.tempo() < 100:
            #     pass

def obstaculo(): ### TEM QUE SER REPENSADO
    # pass
    if dist.valorDistanciaFrente < 200:
        print(dist.valorDistanciaFrente)
        print("obstaculo")

        tcl.alteraLed(1, 0)

        mov.reto(8, const.TRAS)
        mov.reto(8)
        mov.reto(8, const.TRAS)
        mov.reto(8)

        # mov.m.paraMotores()
        # mov.reto(20, FRENTE, 30, cond = con.parachoqueApertadoFrente, cond2 = con.viuVerde, cronos = [cr.VerdeEs, cr.VerdeMeio, cr.VerdeDir], conds = [con.tudoBranco, con.inclinadoCima])
        mov.pidPorDistancia(20, FRENTE, 30, cond = con.parachoqueApertadoFrente, cond2 = con.viuVerde, cronos = [cr.VerdeEs, cr.VerdeMeio, cr.VerdeDir], conds = [con.tudoBranco, con.inclinadoCima])
        if con.parachoqueApertadoFrente():
            
            mov.reto(3, TRAS)
            mov.girarGraus(DIR, 76)

            while con.viuMeioPreto() == False:
                mov.m.velocidadeMotores(45,19)

            mov.reto(3)
            mov.girarGraus(DIR, 55)
            mov.girarGraus(DIR, 35, cronos = [cr.PretoEs], hold = False)
            # while True:
            #     mov.m.velocidadeMotores(-35,25)
            #     if cr.PretoEs.tempo() < 100:
            #         break
            mov.reto(10, TRAS, 20, cond = con.parachoqueApertadoTras)
            print("finalizou obst")


esperaRedutor = False
def motoresTravados():
    global esperaRedutor

    if cr.motorEsquerdoTravado.tempo() > 600:
        print("motorEsquerdo travado")
        # mov.m.velocidadeMotor(1, 30)
        # mov.reto(4)
        esperaRedutor = True

    if cr.motorDireitoTravado.tempo() > 600:
        print("motorDireito travado")
        # mov.m.velocidadeMotor(2, 30)
        # mov.reto(4)
        esperaRedutor = True
    # sleep(1)

    if esperaRedutor:
        print("passando redutor")
        while cr.motorEsquerdoTravado.tempo() > 600 or cr.motorDireitoTravado.tempo() > 600:
            mov.m.velocidadeMotores(60, 60)
            pass
        print("passou do redutor")

    esperaRedutor = False

#função de ver vermelho 
#temporário para tratar a imagem do vermelho
import numpy as np
import cv2



#função de tratar a imagem do vermelho
def verVermelhoii(frame):
    # Carregar imagem e tratar a imagem ----------------------------------------------------------
    #ssh banana@192.168.1.121
    #python3 ~/seguidorCamera/main.py
    img = frame

    #Aplicar o kenel para ajustar as bordas
    kernel = np.ones((5, 5), np.uint8)
    freme_kernel = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    freme_kernel = cv2.morphologyEx(freme_kernel, cv2.MORPH_CLOSE, kernel)

    # Definir número de cores desejado
    data = freme_kernel.reshape((-1, 3))
    data = np.float32(data)
    K = 8  # quanto menor, mais simplificada a imagem
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    # Aplicar K-means 
    _, labels, centers = cv2.kmeans(data, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    simplified = centers[labels.flatten()].reshape(freme_kernel.shape)


    #cortar a imagem -------------------------------------------------------------------------------
    altura, largura = simplified.shape[:2]

    y_start = altura // 4
    x_start = largura // 4

    y_end = altura * 3 // 4
    x_end = largura * 3 // 4

    frame_cortado = simplified[y_start:y_end, x_start:x_end]
    

    # desenhar e contar os contornos -------------------------------------------------------------------
    min_area_threshold=50 #só conta os contornos se ele for mair que isso
    hsv = cv2.cvtColor(frame_cortado, cv2.COLOR_BGR2HSV)

    # 2. Definir os limites (ranges) para a cor vermelha em HSV

    # O vermelho é uma cor especial no HSV, pois "envolve" o 0 (vai de 0 a 10 e de 170 a 180).
    
    # Faixa 1: 0 a 10 (H)
    lower_red_1 = np.array([0, 50, 50])
    upper_red_1 = np.array([10, 255, 255])
    
    # Faixa 2: 170 a 180 (H)
    lower_red_2 = np.array([170, 50, 50])
    upper_red_2 = np.array([180, 255, 255])

    # 3. Criar as máscaras e combiná-las
    mask1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
    mask2 = cv2.inRange(hsv, lower_red_2, upper_red_2)
    mask_vermelho = mask1 + mask2    

    # 5. Encontrar os contornos
    contornos, _ = cv2.findContours(mask_vermelho, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    area = cv2.contourArea(contornos)
   

    #Desenhar o contornos
    imagem_com_contotno=cv2.drawContours(img, contornos, 1, (255,255,255), 3)
    cam.frameProcessado = imagem_com_contotno


    #lógica de vermelho
    '''
    if area>200:
        return True
    else: return False
    '''


def verVermelho(freme, min_area_threshold=50, decision_area_threshold=1000):
    """
    Detecta vermelho considerando apenas um contorno (o maior).
    Retorno: (resultado_bool, area_do_maior_contorno, frame_com_contorno)
    - min_area_threshold: ignora contornos menores que esse valor
    - decision_area_threshold: limiar de área para considerar "vermelho"
    """
    print("Analisando vermelho")
    img = freme.copy()

    # Tratamento morfológico
    kernel = np.ones((5, 5), np.uint8)
    freme_kernel = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    freme_kernel = cv2.morphologyEx(freme_kernel, cv2.MORPH_CLOSE, kernel)

    # K-means para simplificar cores
    data = freme_kernel.reshape((-1, 3)).astype(np.float32)
    K = 8
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(data, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    simplified = centers[labels.flatten()].reshape(freme_kernel.shape)

    # Cortar a imagem (centro)
    altura, largura = simplified.shape[:2]
    y_start, x_start = altura // 4, largura // 4
    y_end, x_end = altura * 3 // 4, largura * 3 // 4
    frame_cortado = simplified[y_start:y_end, x_start:x_end]

    # Máscara para vermelho em HSV
    hsv = cv2.cvtColor(frame_cortado, cv2.COLOR_BGR2HSV)
    lower_red_1 = np.array([0, 50, 50])
    upper_red_1 = np.array([10, 255, 255])
    lower_red_2 = np.array([170, 50, 50])
    upper_red_2 = np.array([180, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
    mask2 = cv2.inRange(hsv, lower_red_2, upper_red_2)
    mask_vermelho = cv2.bitwise_or(mask1, mask2)

    # Encontrar contornos no frame cortado
    contornos, _ = cv2.findContours(mask_vermelho, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Selecionar o maior contorno válido (acima do min_area_threshold)
    maior_contorno = None
    maior_area = 0
    for c in contornos:
        area = cv2.contourArea(c)
        if area > min_area_threshold and area > maior_area:
            maior_area = area
            maior_contorno = c

    # Preparar frame de saída desenhando o contorno no frame original
    frame_com_contornos = img.copy()
    if maior_contorno is not None:
        # Transladar contorno do frame_cortado para o frame original
        offset = np.array([[[x_start, y_start]]])
        cont_transladado = maior_contorno + offset
        cv2.drawContours(frame_com_contornos, [cont_transladado], -1, (0, 255, 0), 2)
        x, y, w, h = cv2.boundingRect(cont_transladado)
        cv2.putText(frame_com_contornos, f"Area:{int(maior_area)}", (x, y-6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    # Decisão: True se a maior área exceder o limiar de decisão
    resultado = maior_area > decision_area_threshold

    cam.frameProcessado = frame_com_contornos
    

    return resultado#, int(maior_area), frame_com_contornos


def pararNoVermelhoCamera():
    if verVermelho(cam.getFrameAtual()):
        print('Vermelho parar')
        mov.m.paraMotores()
        sleep(0.3)
        while True:
            continue



    


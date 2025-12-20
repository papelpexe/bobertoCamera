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

    #to colocando aqui para aproveitar a decisão da verificaIntercessao()
    if decisao == 'gap':
        print("Estou em um gap")
        gapCamera()

def gapCamera():
    mov.retoGraus(cm = 30, cond = pcv2.verificaLinhaPreta(cam.getFrameAtual()))
    if pcv2.verificaIntercessao(cam.getFrameAtual()) == 'gap':
        print("Gap errado, voltando")
        mov.retoGraus(cm = 40, direc = TRAS, cond = pcv2.verificaLinhaPreta(cam.getFrameAtual()))
        
      

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

def pararNoVermelhoCamera():
    if pcv2.verVermelho(cam.getFrameAtual()):
        print('Vermelho parar')
        mov.m.para_motores()
        sleep(0.3)
        while True:
            continue



    


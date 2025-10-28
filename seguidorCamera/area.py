import crono as cr
import sensor as se
import movimentos as mov
import constantes as const
import conds as con
import dist
from defs import sleep
from defs import giroscopio

from defs import tela, pausa
from defs import teclado as tcl

import debug

import camera

import random
from defs import teclado, Teclado

import servos as ser

import math

vitimasCapturadas = []

timeOutTempo = 60000

garraAberta = False
deltaBola = 120
deltaTriangulo = 70

def acharMaiorObjeto():
    """procura o maior objeto detectado por meio da camera"""

    bolinhaAtual = []
    if len(camera.objetos_detectados) > 0:
        for i in camera.objetos_detectados:
            if bolinhaAtual == []:
                bolinhaAtual = i
            elif bolinhaAtual[2] < i[2]:
                bolinhaAtual = i

    return bolinhaAtual

def vendoObjeto(obj = acharMaiorObjeto()):
    """checa se a camera detectou algum objeto"""

    if len(obj) > 0: return True
    else: return False

def proximoVitima(vitima):
    """checa se a vitima esta proxima do robo"""

    if vendoObjeto(vitima):

        if vitima[2] > 70000: 
            print("proximo vitima")
            return True #achar um valor melhor pras distancias
        elif calcularDistanciaVitima(vitima) < 6: 
            print("proximo vitima")
            return True
        else: return False

    else: return False

def alinharComVitima(vitima):
    global deltaBola
    """checa se o robo esta alinhado com a vitima e tenta se alinahr com ela"""

    if vitima[0] > 320 + deltaBola:
        mov.girarGraus(const.DIR, 2, vb = 50)
    elif vitima[0] < 320 - deltaBola:
        mov.girarGraus(const.ESQ, 2, vb = 50)

    return abs(vitima[0] - 320) <= deltaBola

def calcularDistanciaVitima(vitima):
    """calcula a distancia entre o robo e a vitima"""
    
    k = 1060

    if vendoObjeto(vitima):

        area = vitima[2]
        distancia = k * math.sqrt(4.3/area)

        return int(distancia)
    else:
        return None


def prepararGarra():
    ser.abaixarGarra()
    ser.abrirGarra()
    global garraAberta
    garraAberta = True

def pegarBolinha(vitima):
    global garraAberta
    
    ## REALISA O MOVIMENTO DE CAPTURA
    timeOutPegarBolinha = cr.Cronometro()
    timeOutPegarBolinha.inicia()
    while dist.valorDistanciaGarra > 120:
        print(dist.valorDistanciaGarra)
        mov.m.velocidadeMotores(35,35)

        if timeOutPegarBolinha.tempo() > 1000:
            print("timeout pegar bolinha")
            break

    mov.m.velocidadeMotores(35,35)
    ser.fecharGarra()
    sleep(0.3)
    # mov.m.paraMotores()
    mov.reto(5, const.TRAS)
    ser.subirGarra()
    garraAberta = False
    sleep(0.4)

    ## REGISTRA QUE PEGOU A BOLINHA E DEPOSITA NO LADO CERTO SE O SENSOR VER Q EXISTE UMA BOLINHA NA GARRA

    if dist.valorDistanciaGarra < 78:
        print("detectou bolinha com sucesso")
        if vitima[3] == "Silver Ball": 
            ser.jogarBolaProLado(const.ESQ)
        else: 
            ser.jogarBolaProLado(const.DIR)

        sleep(0.3)
        ser.abrirGarra()
        vitimasCapturadas.append(vitima[3])

vitimaAtual = []
alinhadoBola = False
def irAteVitimaECapturar():

    giros = 0
    """procura vitimas, e quando detectar uma, se alinha com ela para capturar logo depois"""

    global garraAberta
    global vitimaAtual
    global alinhadoBola, deltaBola

    ser.fecharPorta()
    ser.fecharPorta()
    ser.fecharPorta()

    if vendoObjeto(camera.objetos_detectados):
        ##CHECA SE ESTA VENDO A VITIMA E SE ESTA A UMA ALTURA ABAIXO DO LIMITE

        vitimaAtual = acharMaiorObjeto()

        if vitimaAtual[1] >= 60:

                ##ROBO SE ALINHA COM A VITIMA
            print(alinharComVitima(vitimaAtual))
            if alinharComVitima(vitimaAtual):

                ## SE ELE ESTIVER ALINHADO, ELE CHECA SE A VITIMA ESTA PROXIMA
                if proximoVitima(vitimaAtual) or dist.valorDistanciaGarra < 180: 
                    if garraAberta == False: 
                        #SE ELE ESTIVER COM A GARRA FECHADA, ELE VOLTA PARA SE AJEITAR
                        mov.reto(6, const.TRAS)
                        prepararGarra()

                    else:
                        pegarBolinha(vitimaAtual)

                else: 
                    ## SE ESTIVER LONGE, ELE CALCULA A DISTANCIA PARA A VITIMA E VAI ATE ELA, COM A GARRA ABERTA
                    if garraAberta == False:
                        ser.abaixarGarra()
                        ser.abrirGarra()
                        garraAberta = True
                    
                    distanciaAteVitima = calcularDistanciaVitima(vitimaAtual)
                    mov.reto(distanciaAteVitima -2.3, vb = 60)

            elif dist.valorDistanciaGarra < 180 and garraAberta == True:

                pegarBolinha(vitimaAtual)

    else: 
        mov.girarGraus(const.ESQ, 35)
        giros += 1

        if giros > 10:
            mov.reto(40)
            giros = 0
            
    
    sleep(0.2)

foiAteOVerde = False
foiAteOVermelho = False
vitimasEntregues = False
contadorGiro = 0

def alinharComTriangulo(objeto):
    deltaTriangulo = 90
    if objeto[0] > 320 + deltaTriangulo:
        mov.girarGraus(const.DIR, 6, vb = 50)
    elif objeto[0] < 320 - deltaTriangulo:
        mov.girarGraus(const.ESQ, 6, vb = 50)
    return abs(objeto[0] - 320) <= deltaTriangulo

def entregarVitima(cor, abrirPortaFunc):
    global foiAteOVerde
    global foiAteOVermelho

    mov.reto(30, const.TRAS, cond=con.parachoqueApertadoTras)

    if con.parachoqueApertadoTrasDir() and not con.parachoqueApertadoTrasEsq():
        mov.reto(1)
        while not con.parachoqueApertadoTrasEsq():
            mov.m.velocidadeMotores(-80, -10)
    elif not con.parachoqueApertadoTrasDir() and con.parachoqueApertadoTrasEsq():
        mov.reto(1)
        while not con.parachoqueApertadoTrasDir():
            mov.m.velocidadeMotores(-10, -80)

    # if foiAteOVerde or foiAteOVermelho:
    #     pass
    # else:
    # mov.reto(30, const.TRAS, cond=con.parachoqueApertadoTras)
    
    abrirPortaFunc()
    # sleep(0.5)

    for i in range(6):
        mov.reto(1,  vb = 100)
        mov.reto(10, const.TRAS,  vb = 100, cond=con.parachoqueApertadoTras)
        mov.reto(1, const.TRAS,  vb = 100, hold = False)
        sleep(0.1)
    ser.fecharPorta()
    if cor == const.VERDE:
        foiAteOVerde = True
    else:
        foiAteOVermelho = True


#TEM QUE TROCAR O ALGORITMO DE RECONHECER OBJETOS NO ARQUIVO DA CAMERA
def seAlinharEIrAteTriangulo():
    global foiAteOVerde, foiAteOVermelho, vitimasEntregues, contadorGiro

    if foiAteOVerde and foiAteOVermelho: vitimasEntregues = True

    ser.fecharPorta()
    ser.fecharPorta()
    ser.fecharPorta()

    objeto = None
    if vendoObjeto(camera.objetos_detectados): 
        objeto = acharMaiorObjeto()
        objCor = objeto[4]
        print(objeto)

        if objeto[2] > 8000 and objeto[1] > 70:


            if (objCor == const.VERDE and foiAteOVerde) or (objCor == const.VERMELHO and foiAteOVermelho):
                print("ja viu esse triangulo")
                mov.girarGraus(const.ESQ, 80)

            else:

                if alinharComTriangulo(objeto):

                    print("alinhado com objeto")
                    # mov.girarGraus(const.ESQ, 180)
                    mov.reto(120, vb = 100, cond = con.pertoFrontal)
                    # mov.reto(5, const.TRAS)
                    mov.reto(20, vb = 40, cond = con.parachoqueApertadoFrente)
                    # mov.reto(2)

                
                    mov.m.paraMotores()
                    mov.reto(10, const.TRAS)
                    mov.girarGraus(const.ESQ, 180)
                    
                    
                    if foiAteOVerde or foiAteOVermelho: andarDepois = False
                    else: andarDepois = True


                    if objCor == const.VERDE: 

                        entregarVitima(objCor, ser.abrirPortaEsq)

                    elif objCor == const.VERMELHO: 

                        entregarVitima(objCor, ser.abrirPortaDir)

                    if andarDepois: mov.reto(40)

                    contadorGiro = 0

        else:
            if contadorGiro >= 10:
                print("")
                mov.reto(30, vb = 70, cond = con.parachoqueApertadoFrente)
                contadorGiro = 0

            else:
                print("tentou girar")
                mov.girarGraus(const.ESQ, 25)
                contadorGiro += 1

            if con.parachoqueApertadoFrente():
                mov.reto(30, const.TRAS)

    else:     
        if contadorGiro >= 10:
            print("")
            mov.reto(30, vb = 70, cond = con.parachoqueApertadoFrente)
            contadorGiro = 0

        else:
            print("tentou girar")
            mov.girarGraus(const.ESQ, 25)
            contadorGiro += 1

        if con.parachoqueApertadoFrente():
            mov.reto(30, const.TRAS)

    sleep(0.7)

def seAlinharNaLinhaDaEntrada():
    while not(73 > se.leRGBCdir()[3] or 73 > se.leRGBCesq()[3]):
        mov.m.velocidadeMotores(8,8)

        mov.m.paraMotores()
        print(se.leRGBCdir()[3], se.leRGBCesq()[3])
        # sleep(10)
        tcl.alteraLed(3, 1)
        while not(73 > se.leRGBCdir()[3] > 67) or not(73 > se.leRGBCesq()[3] > 67): 
            print(se.leRGBCdir()[3], se.leRGBCesq()[3])

            if 67 > se.leRGBCdir()[3]: mov.m.velocidadeMotor(2, 180)
            else: mov.m.velocidadeMotor(2, 0)

            if 67 > se.leRGBCesq()[3]: mov.m.velocidadeMotor(1, 180)
            else: mov.m.velocidadeMotor(1, 0)
            
            if 73 < se.leRGBCdir()[3]: mov.m.velocidadeMotor(2, 180)
            else: mov.m.velocidadeMotor(2, 0)
            
            if 73 < se.leRGBCesq()[3]: mov.m.velocidadeMotor(1, 180)
            else: mov.m.velocidadeMotor(1, 0)

def checarEntradaDaSala():
    if con.viuPrata():
        print("confere area")
        mov.m.modoFreio_(1)
        mov.m.paraMotores()
        sleep(0.5)
        mov.m.modoFreio_(0)
        validarPrata = True

        mov.reto(5, const.TRAS, cond = con.viuPrata, vb = 20)
        
        esperaPrata = cr.Cronometro()
        esperaPrata.reseta()

        while esperaPrata.tempo() < 1000:
            # print(se.leRGBCesq(), se.leRGBCmeio(), se.leRGBCdir())
            if not(con.viuPrata()):
                print(se.leRGBCesq(), se.leRGBCmeio(), se.leRGBCdir())
                validarPrata = False
                print("falso prata")
                break

        if validarPrata == True:
            tcl.alteraLed(4, 1)
            mov.m.paraMotores()
            print("entrou na area de resgate") 
            return True
        else: return False

    # TEM QUE FAZER ELE RECONHECER CINZA DIREITO
    elif con.viuCinza():
        print("confere area")
        mov.m.modoFreio_(1)
        mov.m.paraMotores()
        # sleep(6000)
        sleep(0.5)
        mov.m.modoFreio_(0)
        validarCinza = True

        mov.reto(5, const.TRAS, cond = con.viuCinza, vb = 20)
        
        esperaCinza = cr.Cronometro()
        esperaCinza.reseta()
        # sleep(20)
        while esperaCinza.tempo() < 1000:
            print(se.leRGBCesq(), se.leRGBCmeio(), se.leRGBCdir())
            if not(con.viuCinza()):
                print(se.leRGBCesq(), se.leRGBCmeio(), se.leRGBCdir())
                validarCinza = False
                print("falso cinza")
                break

        if validarCinza == True:
            tcl.alteraLed(4, 1)
            mov.m.paraMotores()
            print("entrou na area de resgate") 
            return True
        else: return False

    else: return False

#TEM QUE REFAZER A FUNCAO INTEIRA
fugiuDaArea = False
def fugirDaArea():
    global fugiuDaArea

    d = 200
    dLateral = 50

    kp = 1
    kd = 5

    kpLateral = 1
    kdLateral = 1

    indFrente = 3000
    indLateral = 700

    vbFuga = 50
    erroFugaAnterior = 0
    erroFugaAnteriorLateral = 0

    contadorDirErrada = 0
    while True:
        D = dist.valorDistanciaFrente
        D2 = dist.valorDistanciaLateral
        D3 = dist.valorDistanciaLateral2

        dif = D - d
        if dif <= 0: dif = 1

        difLateral = D2 - dLateral
        if difLateral == 0: difLateral = 1
    
        erroFugafrente = int(indFrente/dif)
        erroFugaLateral = int(indLateral/difLateral)

        valorPID = (erroFugafrente * kp) - (erroFugafrente - erroFugaAnterior) * kd
        valPIDLateralEsq = (erroFugaLateral * kpLateral) - (erroFugaLateral - erroFugaAnteriorLateral) * kdLateral

        if D > 400: valorPID = 0
        # if D2 > 250: 
        #     valPIDLateralEsq = - valPIDLateralEsq - 10
        #     valPIDLateralDir = valPIDLateralEsq * 2



        print(D2, erroFugaLateral, valPIDLateralEsq)

        mov.m.potenciaMotores(vbFuga + valorPID + valPIDLateralEsq, vbFuga - (0.3*valorPID))
        erroFugaAnterior = erroFugafrente
        erroFugaAnteriorLateral = erroFugaLateral


        if con.parachoqueApertadoFrente():
            mov.reto(6, const.TRAS)
            mov.girarGraus(const.DIR, 30)

        if D2 > 250 and D3 > 250:
            mov.reto(23)
            mov.girarGraus(const.ESQ, 90, cond = con.viuPreto)
            mov.reto(60, cond = con.viuPreto, cond2 = con.parachoqueApertadoFrente)

            if con.parachoqueApertadoFrente():
                mov.reto(6, const.TRAS)
                mov.girarGraus(const.DIR, 50)

            elif con.viuPreto():
                if con.viuPrata(1000) or con.viuCinza(1000):
                    mov.reto(15, const.TRAS)
                    mov.girarGraus(const.DIR, 80)
                else:
                    print("fugiu da area")
                    fugiuDaArea = True
                    teclado.alteraLed(1,0)
                    # mov.girarGraus(const.ESQ, 90)
                    mov.reto(10, cond = con.viuMeioPreto)
                    mov.reto(5)

                    mov.girarGraus(const.ESQ, 90)
                    mov.reto(15, cond = con.parachoqueApertadoFrente)
                    mov.reto(10, const.TRAS)
                    mov.girarGraus(const.DIR, 55)
                    mov.girarGraus(const.DIR, 35, cond = con.viuMeioPreto)
                    # mov.girarGraus(const.ESQ, 90, cond = con.viuMeioPreto)
                    break

            else:
                mov.reto(60, const.TRAS, cond = con.parachoqueApertadoTras)

                if con.parachoqueApertadoTras():
                    mov.reto(6, const.FRENTE)
                    mov.girarGraus(const.DIR, 80)
                else:
                    mov.girarGraus(const.DIR, 80)

                contadorDirErrada += 1

                if contadorDirErrada > 2:
                    mov.girarGraus(const.DIR, 180)
                    contadorDirErrada = 0

        if con.viuPrata() or con.viuCinza():
            mov.reto(15, const.TRAS)
            mov.girarGraus(const.DIR, 90)
            mov.reto(25)

        if con.viuPreto():
                if con.viuPrata(1000) or con.viuCinza(1000):
                    mov.reto(15, const.TRAS)
                    mov.girarGraus(const.DIR, 80)
                else:
                    print("fugiu da area")
                    fugiuDaArea = True
                    teclado.alteraLed(1,0)
                    # mov.girarGraus(const.ESQ, 90)
                    mov.reto(10, cond = con.viuMeioPreto)
                    mov.reto(5)

                    mov.girarGraus(90, const.ESQ)
                    mov.reto(15, cond = con.parachoqueApertadoFrente)
                    mov.reto(10, const.TRAS)
                    mov.girarGraus(90, const.DIR, cond = con.viuMeioPreto)
                    # mov.girarGraus(const.ESQ, 90, cond = con.viuMeioPreto)
                    break

def fugirDaArea2():
    global fugiuDaArea
    # pass

    while True:
        if con.longeLateral(): 
            pass
            ## gira graus pra esquerda
            mov.girarGraus(const.ESQ, 90)
            ## anda ate achar preto ou prata
            mov.reto(10, conds = [con.viuPreto, con.viuPrata, con.parachoqueApertadoFrente])

            if con.viuPreto():
                ## tenta se alinhar no preto e conferir
                fugiuDaArea = True
                while True:
                    
                    print("saiu da area")

            elif con.viuPrata():
                ## desvia do prata
                mov.reto(8, const.TRAS)
                mov.girarGraus(90, const.DIR)

            elif con.parachoqueApertadoFrente():
                mov.reto(7, const.TRAS)
                mov.girarGraus(const.DIR, 90)

        else:
            condsFuga = [
                con.parachoqueApertadoFrente,
                con.viuPreto, 
                con.viuPrata,
                con.longeLateral
            ]

            mov.reto(100, conds = condsFuga)

            if con.parachoqueApertadoFrente():
                mov.reto(7, const.TRAS)
                mov.girarGraus(const.DIR, 90)

            elif con.viuPrata(): 
                pass
                ## desvia do prata
                mov.reto(8, const.TRAS)
                mov.girarGraus(90, const.DIR)              

            elif con.viuPreto(): 
                pass
                fugiuDaArea = True
                while True:
                    
                    print("saiu da area")

                ## se alinha e foge da area
                break
    
            elif con.longeLateral(): 
                pass
                ## se movimenta para tentar achar a saida
                ## gira graus pra esquerda
                mov.girarGraus(const.ESQ, 90)
                ## anda ate achar preto ou prata
                mov.reto(10, conds = [con.viuPreto, con.viuPrata, con.parachoqueApertadoFrente])

                if con.parachoqueApertadoFrente():
                    mov.reto(7, const.TRAS)
                    mov.girarGraus(const.DIR, 92)

                elif con.viuPrata(): 
                    pass
                    ## desvia do prata
                    mov.reto(8, const.TRAS)
                    mov.girarGraus(90, const.DIR)      

                elif con.viuPreto(): 
                    pass
                    ## se alinha e foge da area
                    fugiuDaArea = True
                    while True:
                    
                        print("saiu da area")
                    break
            
def fugirDaArea1_5():
    global fugiuDaArea

    d = 200

    kp = 0.8
    kd = 5

    indFrente = 5000

    vbFuga = 60
    erroFugaAnterior = 0

    while True:
        D = dist.valorDistanciaFrente

        dif = D - d
        if dif <= 0: dif = 1

        erroFugafrente = int(indFrente/dif)

        valorPID = (erroFugafrente * kp) - (erroFugafrente - erroFugaAnterior) * kd
        if D > 300: valorPID = 0
        # if D2 > 250: 
        #     valPIDLateralEsq = - valPIDLateralEsq - 10
        #     valPIDLateralDir = valPIDLateralEsq * 2



        print(D, erroFugafrente)

        mov.m.potenciaMotores(vbFuga - (0.3*valorPID), vbFuga + valorPID)
        erroFugaAnterior = erroFugafrente
        # vbFuga = 100
        
        condsFuga = [
            con.parachoqueApertadoFrente,
            con.viuPreto, 
            con.viuPrata,
            con.longeLateral
        ]

        # # mov.reto(200, vb = vbFuga, conds = condsFuga)
        if any(condsFuga): 
            mov.m.paraMotores()

        if con.parachoqueApertadoFrente():
            mov.reto(6, const.TRAS, vb = vbFuga)
            
            while True:
                mov.m.velocidadeMotores(-25,25)
                val = dist.valorDistanciaLateral - dist.valorDistanciaLateral2
                print(val)
                if 20 < abs(val) < 30:
                    break
                

        elif con.viuPrata(): 
            print("viu prata")
            pass
            ## desvia do prata
            mov.reto(8, const.TRAS, vb = vbFuga)
            mov.girarGraus(const.DIR, 90)     
            mov.reto(20, vb = vbFuga)          

        elif con.viuPreto(): 
            pass
            fugiuDaArea = True
            ## se alinha e foge da area
            break

        elif con.longeLateral(): 
            print("longe lateral")
            pass
            ## se movimenta para tentar achar a saida
            ## gira graus pra esquerda
            mov.reto(10, vb = vbFuga)
            mov.girarGraus(const.ESQ, 90, vb = vbFuga)
            ## anda ate achar preto ou prata
            mov.reto(30, vb = vbFuga, conds = [con.viuPreto, con.viuPrata, con.parachoqueApertadoFrente])

            if con.parachoqueApertadoFrente():
                mov.reto(6, const.TRAS, vb = vbFuga)

                while True:
                    mov.m.velocidadeMotores(-25,25)
                    val = dist.valorDistanciaLateral - dist.valorDistanciaLateral2
                    print(val)
                    if 20 < abs(val) < 30:
                        break

            elif con.viuPrata(): 
                print("viu prata")
                pass
                ## desvia do prata
                mov.reto(8, const.TRAS, vb = vbFuga)
                mov.girarGraus(const.DIR, 90)    
                mov.reto(20, vb = vbFuga) 

            elif con.viuPreto(): 
                pass
                ## se alinha e foge da area
                fugiuDaArea = True
                break

        elif dist.valorDistanciaLateral < 80 or dist.valorDistanciaLateral2 < 80:
            mov.girarGraus(const.DIR, 90)   
            mov.reto(10)
            mov.girarGraus(const.ESQ, 180) 
            mov.reto(10, conds = [con.parachoqueApertadoFrente])

            while True:
                mov.m.velocidadeMotores(-25,25)
                val = dist.valorDistanciaLateral - dist.valorDistanciaLateral2
                print(val)
                if 20 < abs(val) < 30:
                    break

def fugirDaArea3():
    mov.reto(4)
    mov.girarGraus(const.ESQ, 90)

    global fugiuDaArea

    d = 200
    dLat = 130

    kp = 4
    kd = 4

    kpLat = 4
    kdLat = 2

    indFrente = 5000

    vbFuga = 80
    erroFugaAnterior = 0
    erroFugaAnteriorLateral = 0

    difMediaLat = 25
    deltaLat = 25

    while True:
        D = dist.valorDistanciaFrente
        DLateral = dist.valorDistanciaLateral

        dif = D - d
        if dif <= 0: dif = 1

        difLateral = DLateral - dLat
        # if dif <= 0: dif = 0

        erroFugafrente = int(indFrente/dif)
        erroFugaLateral = int(difLateral)

        valorPID = (erroFugafrente * kp) - (erroFugafrente - erroFugaAnterior) * kd
        valorPIDLateral = (erroFugaLateral * kpLat) - (erroFugaLateral - erroFugaAnteriorLateral) * kdLat
        if D > 300: valorPID = 0
        # if D2 > 250: 
        #     valPIDLateralEsq = - valPIDLateralEsq - 10
        #     valPIDLateralDir = valPIDLateralEsq * 2



        # print(DLateral, valorPIDLateral)

        mov.m.potenciaMotores(vbFuga - (0.3*valorPID) + valorPIDLateral, vbFuga - (0.6*valorPIDLateral)  + valorPID)
        erroFugaAnterior = erroFugafrente
        erroFugaAnteriorLateral = erroFugaLateral
        # vbFuga = 100
        
        condsFuga = [
            con.parachoqueApertadoFrente,
            con.viuPreto, 
            con.viuPrata
        ]

        # # mov.reto(200, vb = vbFuga, conds = condsFuga)
        
        if any(condsFuga): 
            mov.m.paraMotores()

        if con.parachoqueApertadoFrente():
            print("parachoqueApertado")
            mov.reto(6, const.TRAS, vb = vbFuga)

            mov.girarGraus(const.DIR, 30)
            
            # while True:
            #     mov.m.velocidadeMotores(-25,25)
            #     val = dist.valorDistanciaLateral - dist.valorDistanciaLateral2
            #     print(val)
            #     if 20 < abs(val) < 30:
            #         break

        elif con.viuPreto(): 
            print("viu preto")

            # if checarEntradaDaSala():
            #         mov.reto(8, const.TRAS)
            # else:
            #     fugiuDaArea = True
            #     ## se alinha e foge da area
            #     break
            fugiuDaArea = True
                    ## se alinha e foge da area
            break

        elif con.viuPrata(): 
            print("viu prata")
     
            ## desvia do prata
            mov.reto(8, const.TRAS, vb = vbFuga)
            mov.girarGraus(const.DIR, 90)     
            mov.reto(20, vb = vbFuga)          

        elif dist.valorDistanciaLateral > 200:
            print("distancia grande")
            mov.reto(23)
            # while True:
            #     mov.m.velocidadeMotores(15,45)

            #     if any(condsFuga): 
            #         break
            mov.girarGraus(const.ESQ, 90, conds = condsFuga)
            mov.reto(100, conds = condsFuga)


            if any(condsFuga): 
                mov.m.paraMotores()

            if con.parachoqueApertadoFrente():
                print("parachoqueApertado")
                mov.reto(6, const.TRAS, vb = vbFuga)

                mov.girarGraus(const.DIR, 60)
                
                # while True:
                #     mov.m.velocidadeMotores(-25,25)
                #     val = dist.valorDistanciaLateral - dist.valorDistanciaLateral2
                #     print(val)
                #     if 20 < abs(val) < 30:
                #         break

            elif con.viuPrata(): 
                print("viu prata")
    
                ## desvia do prata
                mov.reto(8, const.TRAS, vb = vbFuga)
                mov.girarGraus(const.DIR, 90)     
                mov.reto(20, vb = vbFuga)          

            elif con.viuPreto(): 
                print("viu preto")

                # if checarEntradaDaSala():
                #     mov.reto(8, const.TRAS)
                # else:
                #     fugiuDaArea = True
                #     ## se alinha e foge da area
                #     break

                fugiuDaArea = True
                    ## se alinha e foge da area
                break


            
    
    print("fugiu da area")

    # while True:
    #     motores.paraMotores()

def seAlinharNaSaida():
    mov.reto(1, const.TRAS, vb = 35)
    if con.tudoBranco():
        mov.reto(6, vb = 17, cond = con.viuPreto)
    
    if cr.PretoEsEX.tempo() < 100:
        while se.leReflexaoDirEX() > const.PRETO:
            mov.m.velocidadeMotores(25,-4)

    if cr.PretoDirEX.tempo() < 100:
        while se.leReflexaoEsqEX() > const.PRETO:
            mov.m.velocidadeMotores(-4,25)
    mov.m.paraMotores()

    mov.reto(10)


    if con.viuMeioPreto() == False:
        mov.girarGraus(const.DIR, 60, cond = con.viuPreto)
        mov.girarGraus(const.ESQ, 150, cond = con.viuPreto)

    # mov.reto(7)
    # mov.pidPorDistancia(9, const.TRAS)

    # if con.viuMeioPreto(): pass

    # if cr.PretoDirEX.tempo() < 100 and (cr.BrancoEsEX.tempo() < 100 and cr.PretoEsEX.tempo() > 600):
    #     # mov.girarGraus(const.DIR, 90)
    #     # mov.reto(5)
    #     mov.girarGraus(const.DIR, 90, cond = con.meioPreto)
        
    # elif (cr.BrancoDirEX.tempo() < 100 and cr.PretoDirEX.tempo() > 600) and cr.PretoEsEX.tempo() < 100:
    #     # mov.girarGraus(const.ESQ, 90)
    #     # mov.reto(5)
    #     mov.girarGraus(const.ESQ, 90, cond = con.meioPreto)

    print("se alinhou")

def areaDeResgate():

    # print(const.contadorGap)
    global vitimasCapturadas, vitimasEntregues, fugiuDaArea, timeOutTempo
    
    if checarEntradaDaSala() or const.contadorGap >= 4:
        const.contadorGap = 0

    #     print("\n\n\n\n\n\nENTROU NA AREA\n\n\n\n\n")
    # if True:
        # # seAlinharNaLinhaDaEntrada()

        mov.reto(40)  

        camera.encontraObjetos()

        timeOutBola = cr.Cronometro()
        timeOutBola.inicia()
        timeOutBola.reseta()

        while len(vitimasCapturadas) < 3 and timeOutBola.tempo() < timeOutTempo:
            # break
            # pausa()
            camera.processamentoVitima()
            # print(camera.objetos_detectados)
            # proximoVitima(acharMaiorObjeto())
            # print(calcularDistanciaVitima(acharMaiorObjeto()))
            irAteVitimaECapturar()
        print("capiturou todas as vitimas")

        ser.subirGarra()
        ser.abrirGarra()

        if timeOutBola.tempo() < timeOutTempo:
            mov.reto(100, conds = [con.parachoqueApertadoFrente, con.viuPreto, con.viuPrata])
            mov.reto(35, const.TRAS)
        
        while vitimasEntregues == False:
            # break
            # pausa()
            camera.encontraObjetos()
            seAlinharEIrAteTriangulo()
        print("entregou todas as vitimas")

        while fugiuDaArea == False:
            # pausa()
            # if dist.valorDistanciaLateral > 300:
            #     mov.reto(60, cond = con.parachoqueApertadoFrente)
            #     if con.parachoqueApertadoFrente():
            #         mov.girarGraus(const.DIR, 90)

            # else:
            fugirDaArea3()

        # if fugiuDaArea: 
        tcl.alteraLed(4, 0)
        print("fugiu da area de resgate")

        seAlinharNaSaida()

        # mov.reto(6, cond = con.viuPreto)
        # mov.reto(6, const.TRAS, cond = con.viuPreto)
        # mov.girarGraus(const.ESQ, 90, cond = con.viuPreto)
        # mov.girarGraus(const.DIR, 180, cond = con.viuPreto)

        # while True:
        #     pass
        #     # break

        # mov.reto(10, const.TRAS)
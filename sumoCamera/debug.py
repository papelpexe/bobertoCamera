import threading
from defs import tela
from defs import teclado
from defs import Teclado
from defs import motores
from defs import sleep
import movimentos as mov
import constantes as const
from defs import giroscopio
import defs
import funcs
import crono as cr
import sensor as se
import dist

def testaReto(cm = 10,vb = 65):
    mov.reto(cm, const.FRENTE, vb)
    sleep(1)
    mov.reto(cm, const.TRAS, vb)
    sleep(1)

def testaGiro(graus, vel = 80):
    mov.girarGraus(const.ESQ, graus, vel)
    mov.girarGraus(const.DIR, graus, vel)

def testaVelocidade(vel = 60):
    motores.ve(vel, vel)
    sleep(3)
    motores.paraMotores()
    motores.velocidadeMotores(-vel, -vel)
    sleep(3)
    motores.paraMotores()

def testaPotencia(vel = 60):
    motores.potenciaMotores(vel, vel)
    sleep(3)
    motores.paraMotores()
    motores.potenciaMotores(-vel, -vel)
    sleep(3)
    motores.paraMotores()

coiso = 0
def testaTelinha():
    if (teclado.botaoPressionado(Teclado.CIMA)): 
        coiso +=1 
        print("apertou cima")
        sleep(0.4) 
    elif (teclado.botaoPressionado(Teclado.BAIXO)): 
        coiso -=1 
        print("apertou baixo")
        sleep(0.4)
    else: print("apertou nada")

    if coiso > 3: coiso = 3
    if coiso < 0: coiso = 0
        
    match coiso:
        case 0: tela.escreve("aaaaa", 1)
        case 1: tela.escreve("bbbbb", 1)
        case 2: tela.escreve("ccccc", 1)
        case 3: tela.escreve("ddddd", 1)

def apagarTodosLeds():
    teclado.altera_led(1,0)
    teclado.altera_led(2,0)
    teclado.altera_led(3,0)
    teclado.altera_led(4,0)

def piscarLed(led):
    teclado.altera_led(led, 1)
    sleep(0.3)
    teclado.altera_led(led, 0)

  # for i in range(4):
        # if count > 4:
        #     count = 1
        # num = count
        # teclado.alteraLed(num, 1)
        # sleep(0.3)
        # teclado.alteraLed(num, 0)
        # count += 1

        # if (teclado.botaoPressionado(Teclado.CIMA)):
        #     print("apertou teclado cima")
        # if (teclado.botaoPressionado(Teclado.BAIXO)):
        #     print("apertou teclado BAIXO")
   
        # print(motores.atualizaMotores())

        # print(motores.anguloMotor(1), motores.anguloMotor(2))
        # print(const.contadorGap)

        # print(se.sensorCor.lista)

        
        # mov.m.potenciaMotores(40,40)

        # mov.girarGraus(const.ESQ, 90)
        # mov.girarGraus(const.DIR, 90)

        # print(se.leReflexaoTodos())

        # mov.m.potenciaMotores(100,100)


        # print(dist.valorDistanciaGarra, dist.valorDistanciaLateral, dist.valorDistanciaLateral2)
    
        # led = int(input())


        # defs.teclado.alteraLed(1, 1)
        # # # ang2 = int(input())
        # # # mov.m.moveServos(1, 2, ang, 170-ang2)
        # mov.m.moveServo(3,ang)
        # mov.m.moveServo(4,ang)

        # mov.pidPorDistancia(30, const.TRAS)
        # mov.pidPorDistancia(30)

        # mov.reto(100, vb = 10, conds = [conds.parachoqueApertadoFrente, conds.parachoqueApertadoTras])
        # sleep(1)

        # print(se.leHSVtodos())
        # mov.reto(10, const.TRAS, vb = 10)

        # print(cr.VerdeEs.tempo(), cr.VerdeMeio.tempo(), cr.VerdeDir.tempo())
        # print("\n\n\n\n")

        # print(se.leHSVtodos(), se.leRGBCtodos())
        # sleep(1)

        # print(cr.PrataEs.tempo(), cr.PrataMeio.tempo(), cr.PrataDir.tempo())
        # mov.reto(10)
        # sleep(2)
        
        # print(giroscopio.leAnguloX())

        # print(dist.valorDistanciaFrente)
        # print(cr.PretoEsEX.tempo(),cr.PretoEs.tempo(),cr.PretoDir.tempo(),cr.PretoDirEX.tempo())

# print(cr.PretoEsEX.tempo(), cr.PretoDirEX.tempo())
# print(cr.Fez90.tempo())
# print(se.sensorCor.leReflexao())

# print(mov.calculoErro())

# print(cr.VerdeEs.tempo(), cr.VerdeMeio.tempo(), cr.VerdeDir.tempo())
# print(cr.VermEs.tempo(), cr.VermMeio.tempo(), cr.VermDir.tempo())

# print(cr.PretoEsEX.tempo(), cr.PretoEs.tempo(), cr.PretoDir.tempo(), cr.PretoDirEX.tempo())
# print(se.leReflexaoTodos())

# print(se.leHSVesq(), se.checarCorHSV(se.leHSVesq()) == const.verde)
# print(se.leHSVesq(), se.leHSVmeio(), se.leHSVdir())

# print(giroscopio.leAnguloX())
# print(cr.PrataDir.tempo(), cr.PrataMeio.tempo(), cr.PrataEs.tempo())
# print(dist.leDistanciaFrente())

# print(cr.PrataDir.tempo(), cr.PrataMeio.tempo(), cr.PrataEs.tempo())

# print(se.leRGBCesq(), se.leRGBCmeio(), se.leRGBCdir())

# print(se.leRGBCesq(), se.leRGBCmeio(), se.leRGBCdir())

# print(cr.CinzaEs.tempo(), cr.CinzaMeio.tempo(), cr.CinzaDir.tempo())
# print(area.calcularDistanciaVitima(area.acharVitimasProximas()))

# print(se.leReflexaoTodos())

# debug.testaReto(30)
# debug.testaReto(20)
# debug.testaReto(10)
# debug.testaReto(5)
# sleep(1)
# print(dist.valorDistanciaLateral, dist.valorDistanciaFrente) 

# print(cr.PretoEsEX.tempo(), cr.PretoEs.tempo(), cr.PretoDir.tempo(), cr.PretoDirEX.tempo())
# print(cr.BrancoEsEX.tempo(), cr.BrancoEs.tempo(), cr.BrancoDir.tempo(), cr.BrancoDirEX.tempo())

# if exec.tempo() > 1000:
#     print(counter)
#     counter = 0
#     exec.reseta()

# print(se.leReflexaoTodos())
# print(cr.VerdeEs.tempo(), cr.VerdeMeio.tempo(), cr.VerdeDir.tempo())
# print(cr.VermEs.tempo(), cr.VermMeio.tempo(), cr.VermDir.tempo())
# debug.testaGiro(180, 65)
# counter += 1

# debug.testaGiro(180) #testa giro

# mov.reto(10, const.TRAS, hold = False) #testa andar pra tras
# mov.girarGraus(const.ESQ, 50)
# mov.reto(23)
# mov.girarGraus(const.DIR, 90)
# mov.reto(23)

# print(se.sensorCor.lista)

# ang = int(input())
# ang2 = int(input())
# mov.m.moveServos(1, 2, ang, 170-ang2)
# mov.m.moveServo(3,ang)

# ser.abaixarGarra()
# sleep(0.2)
# ser.abrirGarra()
# sleep(1)
# ser.fecharGarra()
# sleep(0.2)
# ser.subirGarra()
# sleep(1)
# ser.jogarBolaProLado(const.ESQ)
# ser.abrirPortaEsq()
# sleep(1)



# # ser.abaixarGarra()
# # sleep(0.2)
# # ser.abrirGarra()
# # sleep(1)
# # ser.fecharGarra()
# # sleep(0.2)
# # ser.subirGarra()
# # sleep(1)
# ser.jogarBolaProLado(const.DIR)
# ser.abrirPortaDir()
# sleep(1)

# print(giroscopio.leAnguloX())

# print(mov.anguloMotorEsquerdo, mov.anguloMotorDireito)
# mov.m.estado()

# mov.reto(30, vb = 10, cond = conds.parachoqueApertado)
# sleep(1)


            



        
        # if (teclado.botaoPressionado(Teclado.ENTER)):
        #     break

        # #pausa o codigo apertando um botao
        # if (teclado.botaoPressionado(Teclado.CIMA)):
        #     mov.m.paraMotores()
        #     tela.escreve("codigo pausado", 1)
        #     sleep(0.2) 
        #     while True:
        #         if (teclado.botaoPressionado(Teclado.CIMA)): 
        #             sleep(0.2) 
        #             break
        #         pass
                
        #     tela.apaga(1)
        # count+=1
        # if cr.relogio.tempo() >= 1000:
        #     cr.relogio.reseta()
        #     print(count)
        #     count = 0

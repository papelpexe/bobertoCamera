from defs import motores as m
from time import sleep
import constantes as const

#primeiro e o esquerdo e o segundo valor e o direito

deltaAngulo = 170

def subirGarra(angulo = 180):
    print("subiu garra")
    m.move_servo(3, angulo)

def abaixarGarra(angulo = 4):
    m.move_servo(3, angulo)

def fecharGarra(angulo = 150):
    ang = 0
    while ang < angulo:
        ang += 10
        if ang > angulo: ang = angulo
        m.moc(1, 2, ang, deltaAngulo-ang)
        sleep(0.03)

def abrirGarra(angulo = 95):
    m.move_servos(1, 2, angulo, deltaAngulo-angulo)

def jogarBolaProLado(lado):
    if lado == const.DIR : 
        m.move_servos(1, 2, 170, 80)
        sleep(0.2)
        m.move_servos(2, 130)

    if lado == const.ESQ : 
        m.move_servos(1, 2, 100, 10)
        sleep(0.2)
        m.move_servo(1, 50)

def fecharPorta():
    m.move_servo(4, 90)

def abrirPortaDir():
    m.move_servo(4, 135)

def abrirPortaEsq():
    m.move_servo(4, 25)
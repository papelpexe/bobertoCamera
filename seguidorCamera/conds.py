import sensor as se
import crono as cr
import dist
import constantes as const
from defs import giroscopio as giro
import processOpenCv
import camera

def tudoBranco(max = 100, min = 0):
    if min < cr.BrancoDirEX.tempo() < max and min < cr.BrancoDir.tempo() < max and\
        min < cr.BrancoEs.tempo() < max and min < cr.BrancoEsEX.tempo() < max and viuPreto() == False:
        return True
    else: return False

def meioBranco(max = 100):
    if cr.BrancoDir.tempo() < max and cr.BrancoEs.tempo() < max:
        return True
    else: return False

def meioBrancoEsq():
    if cr.BrancoEs.tempo() < 100:
        return True
    else: return False

def meioBrancoDir():
    if cr.BrancoDir.tempo() < 100:
        return True
    else: return False

def meioBrancoEsqFalso():
    if cr.BrancoEs.tempo() < 100:
        return False
    else: return True

def meioBrancoDirFalso():
    if cr.BrancoDir.tempo() < 100:
        return False
    else: return True

def brancoEsqEX():
    if cr.BrancoEsEX.tempo() < 100:
        return True
    else: return False

def brancoDirEX():
    if cr.BrancoDirEX.tempo() < 100:
        return True
    else: return False

def brancoEsqFalsoEX():
    if cr.BrancoEsEX.tempo() < 100:
        return False
    else: return True

def brancoDirFalsoEX():
    if cr.BrancoDirEX.tempo() < 100:
        return False
    else: return True

def meioBrancoFalso(): return not meioBranco()
    
def tudoPreto():
    if cr.PretoDirEX.tempo() < 100 and cr.PretoDir.tempo() < 100 and cr.PretoEs.tempo() < 100 and cr.PretoEsEX.tempo() < 100:
        return True
    else: return False

def meioPreto():
    if cr.PretoDir.tempo() < 100 and cr.PretoEs.tempo() < 100:
        return True
    else: return False

def viuMeioPreto(max = 100):
    if cr.PretoDir.tempo() < max or cr.PretoEs.tempo() < max:
        return True
    else: return False

def viuMeioPretoEsq():
    if cr.PretoEs.tempo() < 100:
        return True
    else: return False

def viuMeioPretoDir():
    if cr.PretoDir.tempo() < 100:
        return True
    else: return False

def tudoVermelho():
    if cr.VermEs.tempo() < 100 and cr.VermMeio.tempo() < 100 and cr.VermDir.tempo() < 100: return True
    else: return False

def tudoPrata():
    if cr.PrataEs.tempo() < 100 and cr.PrataDir.tempo() < 100: return True; print("tudo prata")
    else: return False

def tudoCinza():
    if cr.CinzaEs.tempo() < 100 and cr.CinzaDir.tempo() < 100: return True
    else: return False

def viuVerde():
    if cr.VerdeEs.tempo() < 100 or cr.VerdeMeio.tempo() < 100 or cr.VerdeDir.tempo() < 100: return True
    else: return False

def viuVerdeEsq():
    if cr.VerdeEs.tempo() < 100: return True
    else: return False

def viuVerdeDir():
    if cr.VerdeDir.tempo() < 100: return True
    else: return False

def viuVermelho():
    if cr.VermEs.tempo() < 100 or cr.VermMeio.tempo() < 100 or cr.VermDir.tempo() < 100: return True
    else: return False

def viuPrata(time = 100):
    if cr.PrataEs.tempo() < time or cr.PrataMeio.tempo() < time or cr.PrataDir.tempo() < time: return True
    else: return False

def viuCinza(time = 100):
    if cr.CinzaEs.tempo() < 100 or cr.CinzaMeio.tempo() < 100 or cr.CinzaDir.tempo() < 100: return True
    else: return False

def viuPreto():
    if cr.PretoDirEX.tempo() < 100 or cr.PretoDir.tempo() < 100 or cr.PretoEs.tempo() < 100 or cr.PretoEsEX.tempo() < 100:
        return True
    else: return False

def alinhado():
    if cr.BrancoDirEX.tempo() < 50 and cr.BrancoEsEX.tempo() < 50 and(cr.PretoDir.tempo() < 100 or cr.PretoEs.tempo() < 100):
        return True
    else: return False

def distanciaMenorQue(mm): 
    if dist.leDistanciaFrente() <= mm: return True 
    else: return False

def distanciaMaiorQue(mm): 
    if dist.leDistanciaFrente() >= mm: return True 
    else: return False

def parachoqueApertado(dir = const.FRENTE):
    if dir == const.FRENTE:
        if cr.parachoqueFrente.tempo() < 100: return True
        else: return False
 
    if dir == const.TRAS:
        if cr.parachoqueTras.tempo() < 100: return True
        else: return False

def parachoqueApertadoTras():
    if cr.parachoqueTras.tempo() < 100: return True
    else: return False

def parachoqueApertadoFrente():
    if cr.parachoqueFrente.tempo() < 100: return True
    else: return False

def parachoqueApertadoFrenteEsq():
    if cr.parachoqueFrenteEsquerdo.tempo() < 100: return True
    else: return False

def parachoqueApertadoFrenteDir():
    if cr.parachoqueFrenteDireito.tempo() < 100: return True
    else: return False

def parachoqueApertadoTrasEsq():
    if cr.parachoqueTrasEsquerdo.tempo() < 100: return True
    else: return False

def parachoqueApertadoTrasDir():
    if cr.parachoqueTrasDireito.tempo() < 100: return True
    else: return False
 
def longeLateral():
    if dist.valorDistanciaLateral > 230: return True 
    else: return False
 
def pertoLateral():
    if dist.valorDistanciaLateral < 200: return True 
    else: return False

def longeFrontal():
    if dist.valorDistanciaFrente > 200: return True 
    else: return False
 
def pertoFrontal():
    if dist.valorDistanciaFrente < 200: return True 
    else: return False

def inclinadoCima():
    if giro.leAnguloX() > 15: return True
    else: return False

def vendoPreto():
    dec = processOpenCv.verificaIntercessao2(camera.getFrameAtual())
    print(dec)
    if dec == 'nada':
        return True
    else: return False
from cronometro import Cronometro
import sensor
import constantes as const
import threading
from time import sleep
from defs import teclado as tcl


relogio = Cronometro("tempo") ## MEDE O TEMPO DE EXECUCAO DO ROBO
espera = Cronometro()

## CRONOMETRO QUE MEDE O TEMPO DES DE A ULTIMA VEZ QUE VIU ALGO NO SENSOR ESPECIFICADO
VerdeDir = Cronometro() 
VerdeMeio = Cronometro()
VerdeEs = Cronometro()

VermDir = Cronometro() 
VermMeio = Cronometro()
VermEs = Cronometro()

PrataDir = Cronometro() 
PrataMeio = Cronometro()
PrataEs = Cronometro()

CinzaDir = Cronometro() 
CinzaMeio = Cronometro()
CinzaEs = Cronometro()

PretoDirEX = Cronometro()
PretoDir = Cronometro()
PretoEs = Cronometro()
PretoEsEX = Cronometro()

BrancoDirEX = Cronometro()
BrancoDir = Cronometro()
BrancoEs = Cronometro()
BrancoEsEX = Cronometro()

FezVerde = Cronometro()
Fez90 = Cronometro()

RampaSubiu = Cronometro()
RampaDesceu = Cronometro()

fezGap = Cronometro()

parachoqueFrente = Cronometro()
parachoqueTras = Cronometro()

parachoqueFrenteEsquerdo = Cronometro()
parachoqueFrenteDireito = Cronometro()
parachoqueTrasEsquerdo = Cronometro()
parachoqueTrasDireito = Cronometro()

motorEsquerdoTravado = Cronometro()
motorDireitoTravado = Cronometro()

FezFuncao = Cronometro()

#INICIA OS CRONOMETROS
relogio.carrega()
espera.inicia()

FezVerde.inicia()
Fez90.inicia()

VerdeDir.inicia()
VerdeMeio.inicia()
VerdeEs.inicia()

VermDir.inicia()
VermMeio.inicia()
VermEs.inicia()

PrataDir.inicia()
PrataMeio.inicia()
PrataEs.inicia()

CinzaDir.inicia()
CinzaMeio.inicia()
CinzaEs.inicia()

PretoDirEX.inicia()
PretoDir.inicia()
PretoEs.inicia()
PretoEsEX.inicia()

BrancoDirEX.inicia()
BrancoDir.inicia()
BrancoEs.inicia()
BrancoEsEX.inicia()

RampaSubiu.inicia()
RampaDesceu.inicia()

fezGap.inicia()

parachoqueFrenteEsquerdo.inicia()
parachoqueFrenteDireito.inicia()
parachoqueTrasDireito.inicia()
parachoqueTrasEsquerdo.inicia()

parachoqueFrente.inicia()
parachoqueTras.inicia()

motorEsquerdoTravado.inicia()
motorDireitoTravado.inicia()

FezFuncao.inicia()

def pretoCronometros():
    return PretoEsEX.tempo(), PretoEs.tempo(), PretoDir.tempo(), PretoDirEX.tempo()


def reset():
    ##reset dos cronometros, pra mostrar quanto tempo faz des de o ultimo momento em que eles viram algo
    # print(sensor.leHSVdir())
    if sensor.checarCorHSV(sensor.leHSVdir()) == const.VERDE: VerdeDir.reseta(); tcl.alteraLed(2, 1); print("reset verde dir")
    else: tcl.alteraLed(2, 0)
    if sensor.checarCorHSV(sensor.leHSVmeio()) == const.VERDE: VerdeMeio.reseta(); tcl.alteraLed(2, 1); print("reset verde meio")
    else: tcl.alteraLed(2, 0)
    if sensor.checarCorHSV(sensor.leHSVesq()) == const.VERDE: VerdeEs.reseta(); tcl.alteraLed(2, 1); print("reset verde esq")
    else: tcl.alteraLed(2, 0)

    if sensor.checarCorHSV(sensor.leHSVdir()) == const.VERMELHO: VermDir.reseta()
    if sensor.checarCorHSV(sensor.leHSVmeio()) == const.VERMELHO: VermMeio.reseta()
    if sensor.checarCorHSV(sensor.leHSVesq()) == const.VERMELHO: VermEs.reseta()

    if sensor.checarCorRGBC(sensor.leRGBCdir()) == const.PRATA: PrataDir.reseta()
    if sensor.checarCorRGBC(sensor.leRGBCmeio()) == const.PRATA: PrataMeio.reseta()
    if sensor.checarCorRGBC(sensor.leRGBCesq()) == const.PRATA: PrataEs.reseta()

    if sensor.checarCorRGBC(sensor.leRGBCdir()) == const.CINZA: CinzaDir.reseta()
    if sensor.checarCorRGBC(sensor.leRGBCmeio()) == const.CINZA: CinzaMeio.reseta()
    if sensor.checarCorRGBC(sensor.leRGBCesq()) == const.CINZA: CinzaEs.reseta()

    if sensor.leReflexaoDirEX() < const.PRETO: PretoDirEX.reseta()
    if sensor.leReflexaoDir() < const.PRETO: PretoDir.reseta()
    if sensor.leReflexaoEsq() < const.PRETO: PretoEs.reseta()
    if sensor.leReflexaoEsqEX() < const.PRETO: PretoEsEX.reseta()

    if sensor.leReflexaoDirEX() > const.BRANCO: BrancoDirEX.reseta()
    if sensor.leReflexaoDir() > const.BRANCO: BrancoDir.reseta()
    if sensor.leReflexaoEsq() > const.BRANCO: BrancoEs.reseta()
    if sensor.leReflexaoEsqEX() > const.BRANCO: BrancoEsEX.reseta()


def thread_reset():
    while True: 
        reset()
        sleep(0.01)

def dorme(ms):
    print("dorme")
    espera.reseta()
    while espera.tempo() <= ms:
        pass
    print("saiu dorme")

threadCronometros = None
def iniciarThreadCronometros():
        global threadCronometros
        """Inicia a thread para chamar `atualiza` periodicamente."""
        threadCronometros = threading.Thread(target=thread_reset)
        threadCronometros.daemon = True  # Permite que o programa principal encerre mesmo com a thread ativa
        threadCronometros.start()

def thread_parachoque():
    while True: 
        if sensor.botaoApertado(1) or sensor.botaoApertado(4): 
            parachoqueFrente.reseta(); 
            # print("pfrente")
        if sensor.botaoApertado(2) or sensor.botaoApertado(3): 
            parachoqueTras.reseta(); 
            # print("ptras")

        if sensor.botaoApertado(1):
            parachoqueFrenteEsquerdo.reseta(); 
            print("pfrenteESQ")
        if sensor.botaoApertado(4): 
            parachoqueFrenteDireito.reseta(); 
            print("pfrenteDIR")
        
        if sensor.botaoApertado(2): 
            parachoqueTrasEsquerdo.reseta(); 
            print("ptrasDIR")

        if sensor.botaoApertado(3): 
            parachoqueTrasDireito.reseta(); 
            print("ptrasESQ")
            
        sleep(0.02)

threadParachoque = None
def iniciarThreadParachoque():
        global threadParachoque
        """Inicia a thread para chamar `atualiza` periodicamente."""
        threadParachoque = threading.Thread(target=thread_parachoque)
        threadParachoque.daemon = True  # Permite que o programa principal encerre mesmo com a thread ativa
        threadParachoque.start()
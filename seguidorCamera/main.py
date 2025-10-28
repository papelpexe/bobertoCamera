from defs import sleep
sleep(2)
#sudo dmesg

#pra logar: ssh banana@192.168.1.113
#pra entrar no ambiente especifico do pyhton: source meu_venv/bin/activate
#source meu_venv/bin/activate
#sudo shutdown now

#ordem dos botoes 
#ESC ENTER UP DOWN

import threading
from defs import tela
from defs import teclado
from defs import Teclado
from defs import motores
import movimentos as mov
import constantes as const
from defs import giroscopio
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
import camera
import processOpenCv

# ========== SISTEMA DE PARADA ELEGANTE ==========
class ThreadStopSignal(Exception):
    """Exceção para parada elegante da thread"""
    pass

class ThreadAsyncController:
    def __init__(self):
        self.thread_id = None
        self.stop_requested = False
    
    def register_thread(self):
        """Registra a thread para poder pará-la via exceção assíncrona"""
        self.thread_id = threading.get_ident()
        self.stop_requested = False
    
    def stop_thread(self):
        """Para a thread levantando exceção nela de forma assíncrona"""
        if self.thread_id and not self.stop_requested:
            self.stop_requested = True
            print(f"🎯 Enviando exceção assíncrona para thread {self.thread_id}")
            
            # Método 1: Usando ctypes (mais direto)
            try:
                result = ctypes.pythonapi.PyThreadState_SetAsyncExc(
                    ctypes.c_long(self.thread_id), 
                    ctypes.py_object(ThreadStopSignal)
                )
                if result == 0:
                    print("❌ Thread não encontrada ou já terminou")
                elif result > 1:
                    print("⚠️  Múltiplas exceções, restaurando...")
                    ctypes.pythonapi.PyThreadState_SetAsyncExc(self.thread_id, None)
            except Exception as e:
                print(f"❌ Erro no método ctypes: {e}")
                # Método 2: Fallback usando flag
                self.stop_requested = True

# Instância global do controlador
thread_controller = ThreadAsyncController()

def seguidorDeLinha():
    """funcao contendo todas as outras funcoes que checam e realizam os movimentos necessarios de acordo com os perigos da pista"""

    funcs.verdes()
    funcs.intercessao()

    ## segue linha continua
    mov.pid() 

threadRunning = False
def main():
    global flagThreadMorreu

    """funcao que contem todo o funcionamento do robo em um loop"""
    
    # Registra a thread para poder pará-la
    thread_controller.register_thread()

    # inicia thread do flask
    print("Exemplo processamento de IA encontrando posição dos objetos detectados na camera")
    # o código do flask deve ser iniciado em uma thread separada para poder rodar junto com o código principal
    flask_thread = threading.Thread(target=camera.iniciar_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    ## RESETA AS VARIAVEIS NECESSARIAS E POSICIONA OS SERVOS EM SUAS RESPECTIVAS POSICOES
    debug.piscarLed(1)
    giroscopio.reseta_z()
    debug.apagarTodosLeds()
    ser.subirGarra()
    ser.abrirGarra()
    ser.fecharPorta()
    mov.m.para_motores()
    motores.set_modo_freio(0)
    count = 0
    const.contadorGap = 0
    # area.vitimasCapturadas = []
    # area.vitimasEntregues = False
    # area.fugiuDaArea = False
    run = 1

    sleep(1)
  
    tela.escreve("MAIN", 0)
    count = 1

    try:
        while run == 1 and threadRunning:
            #VERIFICAÇÃO NO LOOP PRINCIPAL (obrigatória)
            if thread_controller.stop_requested:
                raise ThreadStopSignal("Parada solicitada no loop principal")
            
            # ser.m.atualiza_servos() ## joga o servos na posicao correta, para remediar os espasmos

            seguidorDeLinha()

           
    except ThreadStopSignal:
        print("✅ Thread main parada elegantemente!")
    except KeyboardInterrupt:
        print("✅ Interrupção via Ctrl+C")
    finally:
        # Limpeza garantida
        debug.piscarLed(1)
        mov.m.para_motores()
        flagThreadMorreu = True
        print("🎯 Thread main finalizada com segurança!")

## thread principal que contem o funcionamento do robo
def thread_main():
    main()

threadMain = None
def iniciarThreadMain():
    global threadMain, threadRunning
    print("iniciou thread main")
    threadMain = threading.Thread(target=thread_main)
    threadMain.daemon = True
    threadRunning = True
    thread_controller.stop_requested = False  # Reseta flag
    threadMain.start()

def matarThreadMain():
    global threadMain, threadRunning
    print("🛑 Solicitando parada da thread main...")
    threadRunning = False
    
    # Para a thread de forma assíncrona
    thread_controller.stop_thread()
    
    if threadMain and threadMain.is_alive():
        threadMain.join(timeout=2)  # Timeout de segurança
        if threadMain.is_alive():
            print("⚠️  Thread não respondeu - forçando parada")
            # Força parada se necessário
        else:
            print("✅ Thread main parada com sucesso!")

iniciaDireto = False   
if len(sys.argv) >= 2:
    iniciaDireto = True

## loop onde podemos reinicar o codigo matando todas as threads, e reiniciar, apenas aoertando o botao enter
try:   
    flagThreadMorreu = False

    print("Exemplo processamento de IA encontrando posição dos objetos detectados na camera")
    # o código do flask deve ser iniciado em uma thread separada para poder rodar junto com o código principal
    flask_thread = threading.Thread(target=camera.iniciar_flask)
    flask_thread.daemon = True
    flask_thread.start()

    camera.iniciarThreadCamera()
    sleep(1)
    # cr.iniciarThreadParachoque()
    # cr.iniciarThreadCronometros()
    # dist.iniciarThreadDistancia()
    # mov.iniciarThreadAnguloMotores()

    while True:
        tela.escreve('esperando')

        while True:
            if (teclado.botao_pressionado(Teclado.ENTER)):
                break
            sleep(0.1)  # Pequeno sleep para não sobrecarregar

        sleep(0.5)
        iniciarThreadMain()
        tela.escreve('rodando codigo')

        while True:
            if (teclado.botao_pressionado(Teclado.ENTER)):
                break
            sleep(0.1)  # Pequeno sleep para não sobrecarregar

        sleep(0.5)
        matarThreadMain()

except KeyboardInterrupt as e:
    mov.motores.para_motores()
    print("\nInterrupção detectada! Parando os motores e encerrando...")
    debug.apagarTodosLeds()
    # Parar os motores
    motores.desligaMotores()
    #desativo todos os servos
    motores.desativaServo(1)
    motores.desativaServo(2)
    motores.desativaServo(3)
    motores.desativaServo(4)
    motores.desativaServo(5)
    motores.desativaServo(6)
    print("Programa encerrado com segurança.")
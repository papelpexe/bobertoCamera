from defs import sensorCor
# from defs import botoes as bo
import constantes as const



#RETORNA OS VALORES DE REFLEXAO
def leReflexaoEsqEX(): 
    return sensorCor.leReflexao()[3]

def leReflexaoEsq(): 
    return sensorCor.leReflexao()[2]

def leReflexaoDir(): 
    return sensorCor.leReflexao()[1]

def leReflexaoDirEX(): 
    return sensorCor.leReflexao()[0]

def leReflexaoTodos():
    return sensorCor.leReflexao()[0], sensorCor.leReflexao()[1], sensorCor.leReflexao()[2], sensorCor.leReflexao()[3]

#calcula o erro pro pid
def erro_pid():
    valErro = (leReflexaoEsqEX() + leReflexaoEsq()) - (leReflexaoDirEX() + leReflexaoDir())

    return valErro


#RETORNA OS VALORES RGBC
def leRGBCesq():
    return sensorCor.leRGBC(1)

def leRGBCmeio():
    return sensorCor.leRGBC(2)

def leRGBCdir():
    return sensorCor.leRGBC(3)

def leRGBCtodos():
    return leRGBCesq(), leRGBCmeio(), leRGBCdir()


#RETORNA OS VALORES HSV 
def leHSVesq():
    return sensorCor.leHSV(3)

def leHSVmeio():
    return sensorCor.leHSV(2)

def leHSVdir():
    return sensorCor.leHSV(1)

def leHSVtodos():
    return leHSVesq(), leHSVmeio(), leHSVdir()


#FAZ A CHEACAGEM DE COR POR VALORES HSV
def checarCorHSV(valores):
    h = valores[0]
    s = valores[1]
    v = valores[2]

    if (52 >= h >= 26) and (45 >= s >= 15) and (60 >= v >= 24): #VERDE
        # print(h,s,v)
        return const.VERDE
   
    elif ((5 >= h >= 0) or (119 >= h >= 112)) and (s >= 40) and (95 > v > 35): #VERMELHO
        # print("viu vermelho")
        return const.VERMELHO
    
    else: return "erro"
    

#FAZ A CHEACAGEM DE COR POR VALORES RGB
def checarCorRGBC(valores):
    r = valores[0]
    g = valores[1]
    b = valores[2]
    c = valores[3]

    # if 100 < c:
    if (r > 126 and g > 126 and b > 126 and c > 65) or c > 71:
        return const.PRATA
    
    ## TEM QUE MUDAR O CINZA
    # elif 58 <= r <= 77 and 62 <=  g <= 83 and 65 <= b <= 85 and 28 <= c <= 41:
    #     return const.CINZA

    else: return "erro"


# def botaoApertado(p):
    
#     #p1 esquerda frente
#     #p4 direita frente

#     #p2 direita atras
#     #p3 esquerda atras

#     match p:
#         case 1:
#             if bo.get_button_value(bo.P1) == bo.LIBERADO: return False 
#             else: return True
#         case 2:
#             if bo.get_button_value(bo.P2) == bo.LIBERADO: return False 
#             else: return True
#         case 3:
#             if bo.get_button_value(bo.P3) == bo.LIBERADO: return False 
#             else: return True
#         case 4:
#             if bo.get_button_value(bo.P4) == bo.LIBERADO: return False 
#             else: return True

# def botaoEsquerdoFrenteApertado():
#     if bo.get_button_value(bo.P1) == bo.LIBERADO: return False 
#     else: return True

# def botaoDireitoFrenteApertado():
#     if bo.get_button_value(bo.P4) == bo.LIBERADO: return False 
#     else: return True

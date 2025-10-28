import camera as cam
import cv2
import numpy as np
from constantes import VERDE, VERMELHO
import constantes as const

## a detectcao de verde e vermelho na pista vai ser por outra funcao q vai ficar rodando numa thread talvezzzzzz

def seguidor_centro(img):
   
    frame = img
    height, width, _ = frame.shape
    metade = width/2

    # Seleção da linha de interesse/ROI (faixa vertical inferior)
    roi_height = 80
    roi = frame[0:roi_height, int(metade/2):int(3*metade/2)]
    # roi = frame[0:roi_height, :]
    # Processamento
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY_INV)
    # Opcional: binary = cv2.bitwise_not(binary)
    # cam.frameProcessado = binary

    contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    heightbin, widthbin = binary.shape

    error = 0
    if len(contours) > 0:
        biggest = max(contours, key=cv2.contourArea)
        M = cv2.moments(biggest)
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            error = cx - widthbin // 2
            # Aqui entra o controle PD (ver seção a seguir)
            # print(f"Erro de posição: {error}")
            # Comando para motores pode ser enviado via serial/IO
    else:
        error = 0  # Linha não encontrada
    return error

#esq e dir estao invertidos dps concerta
def verificaIntercessao(img):
    
    frame = img
    height, width, _ = frame.shape
    metade = width/2
    existeEsq = False
    existeDir = False
    existeCima = False
    resultado = "nada"

    # Processamento - criar binary para processamento
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(blur, 100 , 255, cv2.THRESH_BINARY_INV)
    
    # Criar imagem colorida para visualização
    visualizacao = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
    
    roi_height = 140
    # AUMENTAR a largura do ROI
    roi_x_start = int(width/9)    # Começa em 1/4 da imagem
    roi_x_end = int(8*width/9)    # Termina em 3/4 da imagem

    roi_x_start_cima = int(width/4)    # Começa em 1/4 da imagem
    roi_x_end_cima = int(3*width/4)    # Termina em 3/4 da imagem
    
    roi_y_start = int(height/2 - roi_height/2)
    roi_y_end = int(height/2 + roi_height/2)
    
    roi = binary[roi_y_start:roi_y_end, roi_x_start:roi_x_end]
    frameCima = binary[0:int(height/2 - (3*roi_height/4)), roi_x_start_cima:roi_x_end_cima]

    heightbin, widthbin = roi.shape
    
    # MANTER as áreas das pontas no mesmo tamanho (1/4 da ROI cada)
    frameDir = roi[:, int(5*widthbin/6):widthbin]  # Último 1/4 da ROI (direita)
    frameEsq = roi[:, 0:int(widthbin/6)]           # Primeiro 1/4 da ROI (esquerda)

    ## DESENHAR RETÂNGULOS DAS ÁREAS NA IMAGEM COLORIDA ##
    
    # Desenhar retângulo da área ROI principal (CINZA) - MAIS LARGO
    cv2.rectangle(visualizacao, 
                  (roi_x_start, roi_y_start), 
                  (roi_x_end, roi_y_end), 
                  (128, 128, 128), 2)  # Cinza para ROI
    
    # Desenhar retângulo da área frameCima (CINZA CLARO)
    cv2.rectangle(visualizacao, 
                  (roi_x_start_cima, 0), 
                  (roi_x_end_cima, int(height/2 - (3*roi_height/4))), 
                  (200, 200, 200), 2)  # Cinza claro para CIMA
    
    # Desenhar retângulo da área frameEsq (AZUL) - EXTREMA DIREITA da ROI
    esq_x_start = roi_x_start + int(5*widthbin/6)
    esq_x_end = roi_x_end
    cv2.rectangle(visualizacao, 
                  (esq_x_start, roi_y_start), 
                  (esq_x_end, roi_y_end), 
                  (255, 0, 0), 2)  # Azul para ESQUERDA (mas está na direita)
    
    # Desenhar retângulo da área frameDir (VERMELHO) - EXTREMA ESQUERDA da ROI
    dir_x_start = roi_x_start
    dir_x_end = roi_x_start + int(widthbin/5)
    cv2.rectangle(visualizacao, 
                  (dir_x_start, roi_y_start), 
                  (dir_x_end, roi_y_end), 
                  (0, 0, 255), 2)  # Vermelho para DIREITA (mas está na esquerda)
    
    # Adicionar labels para identificar cada área
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(visualizacao, "ROI", (roi_x_start + 10, roi_y_start + 20), font, 0.5, (128, 128, 128), 1)
    cv2.putText(visualizacao, "CIMA", (roi_x_start + 10, 20), font, 0.5, (200, 200, 200), 1)
    cv2.putText(visualizacao, "DIR", (dir_x_start + 10, roi_y_start + 20), font, 0.5, (255, 0, 0), 1)
    cv2.putText(visualizacao, "ESQ", (esq_x_start + 10, roi_y_start + 20), font, 0.5, (0, 0, 255), 1)

    ## cria os contornos referentes a cada parte da imagem
    contoursEsq, _ = cv2.findContours(frameEsq, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contoursDir, _ = cv2.findContours(frameDir, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contoursCima, _ = cv2.findContours(frameCima, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    ## DESENHAR CONTORNOS ENCONTRADOS NA IMAGEM COLORIDA ##
    
    # Desenhar contornos da ESQUERDA em CYAN (na área azul)
    for cnt in contoursEsq:
        area = cv2.contourArea(cnt)
        if area > 1000:
            # Ajustar coordenadas para a imagem principal
            cnt_ajustado = cnt + [roi_x_start + int(3*widthbin/4), roi_y_start]
            cv2.drawContours(visualizacao, [cnt_ajustado], -1, (255, 255, 0), 2)  # Cyan
    
    # Desenhar contornos da DIREITA em AMARELO (na área vermelha)
    for cnt in contoursDir:
        area = cv2.contourArea(cnt)
        if area > 1000:
            # Ajustar coordenadas para a imagem principal
            cnt_ajustado = cnt + [roi_x_start, roi_y_start]
            cv2.drawContours(visualizacao, [cnt_ajustado], -1, (0, 255, 255), 2)  # Amarelo
    
    # Desenhar contornos de CIMA em MAGENTA
    for cnt in contoursCima:
        area = cv2.contourArea(cnt)
        if area > 1000:
            # Ajustar coordenadas para a imagem principal
            cnt_ajustado = cnt + [roi_x_start, 0]
            cv2.drawContours(visualizacao, [cnt_ajustado], -1, (255, 0, 255), 2)  # Magenta

    ## verifica se existem contornos em cada parte da imagem
    if len(contoursEsq) > 0:
        maiorCntesq = max(contoursEsq, key = cv2.contourArea)
        # print(f"Area Esq: {cv2.contourArea(maiorCntesq)}")
        if cv2.contourArea(maiorCntesq) > 1000:
            existeEsq = True
    if len(contoursDir) > 0:
        maiorCntdir = max(contoursDir, key = cv2.contourArea)
        # print(f"Area Dir: {cv2.contourArea(maiorCntdir)}")
        if cv2.contourArea(maiorCntdir) > 1000:
            existeDir = True
    if len(contoursCima) > 0:
        maiorCntcima = max(contoursCima, key = cv2.contourArea)
        # print(f"Area Cima: {cv2.contourArea(maiorCntcima)}")
        if cv2.contourArea(maiorCntcima) > 1000:
            existeCima = True

    ##toma a decisao com base nas informacoes obtidas
    if existeEsq and not existeDir and not existeCima:
        resultado = const.ESQ
    elif existeDir and not existeEsq and not existeCima:
        resultado = const.DIR
    elif not existeDir and not existeEsq and not existeCima:
        resultado = "gap"
    else:
        resultado = "nada"

    # Adicionar resultado na imagem
    cv2.putText(visualizacao, f"Resultado: {resultado}", (10, height - 20), font, 0.7, (255, 255, 255), 2)

    # Usar a imagem colorida para visualização
    # cam.frameProcessado = visualizacao

    return resultado

def checarVerdes(img):

    verdesDetectados = []

    frame = img.copy()
    fheight, fwidth, _ = frame.shape
    

    # Processamento - criar binary para processamento
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
   
    valorBaixoVerde = np.array([40, 80, 70])
    valorAltoVerde = np.array([80, 255, 235])

    valorBaixoPreto = np.array([0, 0, 0])
    valorAltoPreto = np.array([255, 50, 50])

    maskVerde = cv2.inRange(hsv, valorBaixoVerde, valorAltoVerde)
    
    kernel = np.ones((10,10), np.uint8)
    maskVerdeK = cv2.morphologyEx(maskVerde, cv2.MORPH_CLOSE, kernel)

    contoursVerde, _ = cv2.findContours(maskVerdeK, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   

    for cnt in contoursVerde:
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        meio = int(h/2)
        deltaH = 80
        
        # if area > 100 and (int(fheight/2) - deltaH < meio and int(fheight/2) + deltaH > meio):
        if area > 100:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            indQuadrado = 20
            y1 = max(0, y - indQuadrado)
            y2 = min(frame.shape[0], y + h + indQuadrado)
            x1 = max(0, x - indQuadrado)
            x2 = min(frame.shape[1], x + w + indQuadrado)
            
            quadMaior = frame[y1:y2, x1:x2]

            if quadMaior.size == 0:
                continue
            
            qheight, qwidth, _ = quadMaior.shape

            # quadEsqSup = quadMaior[0:int(qheight/2),0:int(qwidth/2)]
            # quadDirSup = quadMaior[0:int(qheight/2),int(qwidth/2):qwidth]
            # quadEsqInf = quadMaior[int(qheight/2):qheight,0:int(qwidth/2)]
            # quadDirInf = quadMaior[int(qheight/2):qheight,int(qwidth/2):qwidth]

            # quads = [quadEsqSup, quadDirSup, quadEsqInf, quadDirInf]

            quads = [
                (0, qheight//2, 0, qwidth//2),      # ESQ_SUP
                (0, qheight//2, qwidth//2, qwidth), # DIR_SUP  
                (qheight//2, qheight, 0, qwidth//2), # ESQ_INF
                (qheight//2, qheight, qwidth//2, qwidth) # DIR_INF
            ]


            # Definir os quadrantes com suas coordenadas relativas
            quadrantes = [
                (0, int(qheight/2), 0, int(qwidth/2), "ESQ_SUP"),      # Quadrante Esquerdo Superior
                (0, int(qheight/2), int(qwidth/2), qwidth, "DIR_SUP"), # Quadrante Direito Superior
                (int(qheight/2), qheight, 0, int(qwidth/2), "ESQ_INF"), # Quadrante Esquerdo Inferior
                (int(qheight/2), qheight, int(qwidth/2), qwidth, "DIR_INF") # Quadrante Direito Inferior
            ]

            bools = []
            for y_start, y_end, x_start, x_end in quads:

                quad = quadMaior[y_start:y_end, x_start:x_end]
                
                if quad.size == 0:
                    bools.append(False)
                    continue
                    
                maskPreto = cv2.inRange(quad, valorBaixoPreto, valorAltoPreto)
                kernel = np.ones((10,10), np.uint8)
                maskPretoK = cv2.morphologyEx(maskPreto, cv2.MORPH_CLOSE, kernel)
                contoursPreto, _ = cv2.findContours(maskPretoK, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                if len(contoursPreto) > 0:
                    maiorCntcima = max(contoursPreto, key = cv2.contourArea)
                    if cv2.contourArea(maiorCntcima) > 100:
                        bools.append(True)

                    else: bools.append(False)
                else: bools.append(False)
            
            verde_mov = "verde falso"
            if bools[0] == True and bools[1]==True:
                if bools[2] and not bools[3]:
                    verde_mov= "verde dir" #ta invertido aqui por motivos nao explicados
                elif bools[3] and not bools[2]:
                    verde_mov= "verde esq"

            verdesDetectados.append(verde_mov)
    
    return verdesDetectados

# Intervalo de azul em HSV
valorBaixoAzul = np.array([100, 100, 100])
valorAltoAzul = np.array([130, 255, 255])

valorBaixoVerde = np.array([40, 80, 70])
valorAltoVerde = np.array([80, 255, 235])

valorBaixoVermelho1 = np.array([0, 100, 100])
valorAltoVermelho1 = np.array([10, 255, 235])
valorBaixoVermelho2 = np.array([160, 100, 100])
valorAltoVermelho2 = np.array([179, 255, 235])

def encontraObjetos():
    frame = cam.getFrameAtual()

    if frame is None or frame.size == 0: 
        print("frame vazio")
        return
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    objetos_detectados = []  # Limpa a lista de objetos detectados a cada frame

    maskVerde = cv2.inRange(hsv, valorBaixoVerde, valorAltoVerde)
    maskVermelho1 = cv2.inRange(hsv, valorBaixoVermelho1, valorAltoVermelho1)
    maskVermelho2 = cv2.inRange(hsv, valorBaixoVermelho2, valorAltoVermelho2)

    kernel = np.ones((10,10), np.uint8)
    maskVerdeK = cv2.morphologyEx(maskVerde, cv2.MORPH_CLOSE, kernel)
    maskVerm1K = cv2.morphologyEx(maskVermelho1, cv2.MORPH_CLOSE, kernel)
    maskVerm2K = cv2.morphologyEx(maskVermelho2, cv2.MORPH_CLOSE, kernel)

    # Encontrar contornos
    contoursVerde, _ = cv2.findContours(maskVerdeK, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contoursVermelho1, _ = cv2.findContours(maskVerm1K, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contoursVermelho2, _ = cv2.findContours(maskVerm2K, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours = [contoursVermelho1, contoursVermelho2, contoursVerde]

    # Desenhar contornos que são retângulos
    i=0
    for cnt in contours:
        for cnt2 in cnt:
            area = cv2.contourArea(cnt2)
            if area > 100:
                x, y, w, h = cv2.boundingRect(cnt2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                #pego os dados retornados pelo boundingRect para mapear onde na imagem o objeto foi encontrado
                # e calculo o centro do retângulo
                centro_x = x + w // 2
                centro_y = y + h // 2
                #adiciono os dados do objeto detectado na lista de objetos detectados
                #assim posso trabalhar com esses dados depois para tomar alguma decisão

                cor = None
                if cnt is contoursVerde: cor = VERDE
                elif cnt is contoursVermelho1 or cnt is contoursVermelho2: cor = VERMELHO
                if w*h > 2000: 
                    cam.appendObjDetectados([centro_x, centro_y, w*h, i, cor])
                    i+=1

    print(cam.getObjDetectados())
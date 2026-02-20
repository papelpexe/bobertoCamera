import camera as cam
import cv2
import numpy as np
from constantes import VERDE, VERMELHO
import constantes as const

## a detectcao de verde e vermelho na pista vai ser por outra funcao q vai ficar rodando numa thread talvezzzzzz

def seguidor_centro(img):

    if img is None: return 0; print("frame nulo")
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

def verificaLinhaPreta(img = cam.getFrameAtual()):
    """Verifica se existe uma linha preta na imagem, retornando True ou False."""
    if img is None: return False; print("frame nulo")
    frame = img
    height, width, _ = frame.shape
    metade = width/2

    # Seleção da linha de interesse/ROI (faixa vertical inferior)
    roi_height = 80
    roi = frame[0:roi_height, int(metade/2):int(3*metade/2)]
    
    # Processamento
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        return True
    else:
        return False

#esq e dir estao invertidos dps concerta
def verificaIntercessao(img):
    
    if img is None: return "nada"; print("frame nulo")
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
    _, binary = cv2.threshold(blur, 84, 255, cv2.THRESH_BINARY_INV)
    
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

    if img is None: return verdesDetectados; print("frame nulo")
    frame = img.copy()
    fheight, fwidth, _ = frame.shape
    
    # Cria uma cópia da imagem para desenhar os contornos
    krn = 15
    frameblur = cv2.GaussianBlur(frame, (krn,krn), 0)
    frame_com_contornos = frameblur.copy()

    # Processamento - criar binary para processamento
    # frameMenor = frame[int(fheight * 2/10):int(fheight * 8/10), int(fwidth * 2/10):int(fwidth * 8/10)]
    # hsv = cv2.cvtColor(frameMenor, cv2.COLOR_BGR2HSV)
    hsv = cv2.cvtColor(frameblur, cv2.COLOR_BGR2HSV)
   
    valorBaixoVerde = np.array([40, 150, 70])
    valorAltoVerde = np.array([80, 255, 235])

    valorBaixoPreto = np.array([0, 0, 0])
    valorAltoPreto = np.array([180, 35, 27])

    maskVerde = cv2.inRange(hsv, valorBaixoVerde, valorAltoVerde)
    
    kernel = np.ones((krn,krn), np.uint8)
    maskVerdeK = cv2.morphologyEx(maskVerde, cv2.MORPH_CLOSE, kernel)

    contoursVerde, _ = cv2.findContours(maskVerdeK, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   
    # Desenha todos os contornos verdes encontrados
    cv2.drawContours(frame_com_contornos, contoursVerde, -1, (0, 255, 255), 2)

    for i, cnt in enumerate(contoursVerde):
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        meio = int(y + h/2)
        deltaH = 80
        
        if area > 100:
            # Desenha retângulo verde ao redor da região detectada
            cv2.rectangle(frame_com_contornos, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Adiciona texto com o número do contorno
            cv2.putText(frame_com_contornos, f"Verde {i+1}", (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            indQuadrado = 60
            y1 = max(0, y - indQuadrado)
            y2 = min(frame.shape[0], y + h + indQuadrado)
            x1 = max(0, x - indQuadrado)
            x2 = min(frame.shape[1], x + w + indQuadrado)
            
            quadMaior = frame[y1:y2, x1:x2]

            if quadMaior.size == 0:
                continue
            
            qheight, qwidth, _ = quadMaior.shape

            quads = [
                (0, qheight//2, 0, qwidth//2),      # ESQ_SUP
                (0, qheight//2, qwidth//2, qwidth), # DIR_SUP  
                (qheight//2, qheight, 0, qwidth//2), # ESQ_INF
                (qheight//2, qheight, qwidth//2, qwidth) # DIR_INF
            ]

            bools = []
            contornos_pretos_quadrantes = []  # Para armazenar contornos pretos por quadrante
            
            for j, (y_start, y_end, x_start, x_end) in enumerate(quads):
                quad = quadMaior[y_start:y_end, x_start:x_end]
                
                if quad.size == 0:
                    bools.append(False)
                    contornos_pretos_quadrantes.append([])
                    continue
                    
                maskPreto = cv2.inRange(quad, valorBaixoPreto, valorAltoPreto)
                kernel = np.ones((10,10), np.uint8)
                maskPretoK = cv2.morphologyEx(maskPreto, cv2.MORPH_CLOSE, kernel)
                contoursPreto, _ = cv2.findContours(maskPretoK, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                # Armazena os contornos pretos para desenho posterior
                contornos_pretos_quadrantes.append(contoursPreto)
                
                if len(contoursPreto) > 0:
                    maiorCntcima = max(contoursPreto, key = cv2.contourArea)
                    if cv2.contourArea(maiorCntcima) > 100:
                        bools.append(True)
                    else: 
                        bools.append(False)
                else: 
                    bools.append(False)
            
            verde_mov = "verde falso"
            if bools[0] == True and bools[1] == True: 
                if int(fheight * 1/10) < meio < int(fheight * 7/10):
                    if bools[2] and not bools[3]:
                        verde_mov= "verde dir"
                    elif bools[3] and not bools[2]:
                        verde_mov= "verde esq"
                else:
                    if bools[2] and not bools[3]:
                        verde_mov= "verde dir fora"
                    elif bools[3] and not bools[2]:
                        verde_mov= "verde esq fora"

            # Adiciona texto com o resultado da detecção
            cv2.putText(frame_com_contornos, verde_mov, (x, y+h+20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            
            # Desenha contornos pretos nos quadrantes
            for j, (y_start, y_end, x_start, x_end) in enumerate(quads):
                contours_preto = contornos_pretos_quadrantes[j]
                if contours_preto:
                    # Ajusta coordenadas para a imagem principal
                    for contour in contours_preto:
                        contour_ajustado = contour + [x1 + x_start, y1 + y_start]
                        cv2.drawContours(frame_com_contornos, [contour_ajustado], -1, (255, 0, 0), 2)
                        
                    # Desenha retângulos dos quadrantes
                    cor_quadrante = (0, 0, 255) if bools[j] else (255, 255, 0)
                    cv2.rectangle(frame_com_contornos, 
                                (x1 + x_start, y1 + y_start),
                                (x1 + x_end, y1 + y_end),
                                cor_quadrante, 1)
                    
                    # Adiciona label do quadrante
                    nomes_quadrantes = ["ESQ_SUP", "DIR_SUP", "ESQ_INF", "DIR_INF"]
                    cv2.putText(frame_com_contornos, nomes_quadrantes[j], 
                               (x1 + x_start, y1 + y_start - 5),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.3, cor_quadrante, 1)

            verdesDetectados.append(verde_mov)

    cam.frameProcessado = frame_com_contornos
    
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

#função de tratar a imagem do vermelho
def verVermelho(freme, min_area_threshold=50, decision_area_threshold=1000):
    
    """
    Detecta vermelho considerando apenas um contorno (o maior).
    Retorno: (resultado_bool, area_do_maior_contorno, frame_com_contorno)
    - min_area_threshold: ignora contornos menores que esse valor
    - decision_area_threshold: limiar de área para considerar "vermelho"
    """
    # print("Analisando vermelho")
    img = freme.copy()

    # Tratamento morfológico
    kernel = np.ones((5, 5), np.uint8)
    freme_kernel = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    freme_kernel = cv2.morphologyEx(freme_kernel, cv2.MORPH_CLOSE, kernel)

    '''
    # K-means para simplificar cores
    data = freme_kernel.reshape((-1, 3)).astype(np.float32)
    K = 8
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(data, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    simplified = centers[labels.flatten()].reshape(freme_kernel.shape)
    '''

    # Cortar a imagem (centro)
    altura, largura = freme_kernel.shape[:2]
    y_start, x_start = altura // 4, largura // 4
    y_end, x_end = altura * 3 // 4, largura * 3 // 4
    frame_cortado = freme_kernel[y_start:y_end, x_start:x_end]

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

    # cam.frameProcessado = frame_com_contornos
    

    return resultado#, int(maior_area), frame_com_contornos

import cv2
import numpy as np

def detectaPrata(image_path, min_area_percentage=5.0):
    """
    Identifica se uma porcentagem mínima de uma imagem (após corte) é composta por tons de cinza/prata.

    A imagem é cortada para remover 1/4 da altura e 1/4 da largura de cada extremidade,
    resultando em uma imagem central com metade da altura e metade da largura originais.

    Args:
        image_path (str): Caminho para o arquivo de imagem.
        min_area_percentage (float): Porcentagem mínima da área total da imagem CORTADA
                                     que deve ser cinza/prata para retornar 'Vi cinza'.

    Returns:
        str: 'Vi cinza' se a condição for atendida, caso contrário, uma string vazia.
    """
    # 1. Carregar a imagem
    img = image_path

    if img is None:
        print(f"Erro: Não foi possível carregar a imagem em {image_path}")
        return ""

    # 2. Aplicar o corte (Cropping)
    height, width = img.shape[:2]

    # Calcular os pontos de início e fim para o corte (1/4 de cada lado)
    # O corte resultará na área central (metade da altura e metade da largura)
    start_row = height // 4
    end_row = height - (height // 4)
    start_col = width // 4
    end_col = width - (width // 4)

    # Realizar o corte
    cropped_img = img[start_row:end_row, start_col:end_col]

    # 3. Converter a imagem CORTADA para o espaço de cores HSV
    hsv = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2HSV)

    # Faixa de cores para cinza/prata em HSV (H: 0-180, S: 0-255, V: 0-255)
    # Cinza/Prata: Baixa Saturação (S <= 50) e Brilho (V) moderado a alto (V >= 50)
    lower_gray = np.array([0, 0, 50])
    upper_gray = np.array([180, 50, 255])

    # 4. Criar a máscara
    mask = cv2.inRange(hsv, lower_gray, upper_gray)

    # 5. Calcular a área de pixels cinza/prata na imagem CORTADA
    total_pixels = cropped_img.shape[0] * cropped_img.shape[1]
    gray_pixels = cv2.countNonZero(mask)

    # 6. Calcular a porcentagem
    gray_area_percentage = (gray_pixels / total_pixels) * 100

    # 7. Verificar a condição e retornar
    if gray_area_percentage >= min_area_percentage:
        print("Estou vendo cinza")
        return "Vi cinza"
    else:
        return ""

import sys 

def contains_silver(img, min_contour_area=1000):
    """
    Verifica a presença de prata em uma imagem usando análise de textura (Laplacian)
    e retorna True se um contorno significativo for encontrado, False caso contrário.
    
    :param image_path: Caminho para o arquivo de imagem.
    :param min_contour_area: Área mínima do contorno para ser considerado "significativo".
    :return: True se a imagem contiver prata, False caso contrário.
    """
    # 1. Carregar a imagem
    if img is None:
        print("Erro: Não foi possível carregar a imagem ")
        return False

    # 2. Converter para escala de cinza
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. Análise de Textura: Operador de Laplace
    # O Laplaciano realça áreas de alta variação de intensidade (textura).
    laplacian = cv2.Laplacian(img_gray, cv2.CV_64F)
    laplacian_abs = cv2.convertScaleAbs(laplacian)

    # 4. Limiarização (Thresholding) para isolar áreas de alta textura (prata)
    # Limiar de 10 é um bom ponto de partida para separar textura de fundo liso.
    _, texture_mask = cv2.threshold(laplacian_abs, 10, 255, cv2.THRESH_BINARY)

    # 5. Detecção de Contornos na máscara de textura
    contours, _ = cv2.findContours(texture_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 6. Verificar a presença de contornos significativos
    for contour in contours:
        if cv2.contourArea(contour) > min_contour_area:
            # Se encontrar um contorno com área maior que o mínimo, consideramos que há prata.
            return True

    # Se nenhum contorno significativo for encontrado
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python silver_detector_final.py <caminho_para_imagem>")
        sys.exit(1)
    
    image_file = sys.argv[1]
    
    # Executar a função e imprimir o resultado
    result = contains_silver(image_file)
    print(f"A imagem '{image_file}' contém prata: {result}")
    
    # O script retorna o valor booleano para o sistema
    sys.exit(0 if result else 1)

def salvaImagem(nomeArquivo, dest_dir: str = None):
    """Salva o frame atual em um diretório.

    - Se `dest_dir` for fornecido, a imagem será salva em `dest_dir/nomeArquivo`.
    - Se `nomeArquivo` já contiver um caminho (ex.: `pasta/arquivo.jpg`), a pasta será criada automaticamente.
    - Se nenhum diretório for especificado e `nomeArquivo` for apenas um nome (sem caminho), o arquivo será salvo em `./imagens/`.

    Retorna True em sucesso, False caso contrário.
    """
    import os
    from pathlib import Path

    # Decide caminho final
    if dest_dir:
        Path(dest_dir).mkdir(parents=True, exist_ok=True)
        final_path = os.path.join(dest_dir, nomeArquivo)
    else:
        dirname = os.path.dirname(nomeArquivo)
        if dirname:
            Path(dirname).mkdir(parents=True, exist_ok=True)
            final_path = nomeArquivo
        else:
            default_dir = './imagens'
            Path(default_dir).mkdir(parents=True, exist_ok=True)
            final_path = os.path.join(default_dir, nomeArquivo)

    print("Salvando imagem em:", final_path)
    frame = cam.getFrameAtual()
    # Verifica se o frame está disponível e não está vazio antes de salvar
    if frame is None:
        print("Aviso: frame vazio (None). Imagem não salva.")
        return False
    if not hasattr(frame, 'size') or frame.size == 0:
        print("Aviso: frame vazio (size==0). Imagem não salva.")
        return False

    try:
        ok = cv2.imwrite(final_path, frame)
        if not ok:
            print(f"Falha ao salvar imagem em: {final_path}")
            return False
    except Exception as e:
        print(f"Erro ao salvar imagem: {e}")
        return False

    return True
   
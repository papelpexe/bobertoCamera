from ultralytics import YOLO
import cv2
import threading
import time
import camera as cam

device = 'cpu'
print(f"Usando dispositivo: {device}")
model = YOLO("/home/banana/best_old.onnx")

lock = threading.Lock()

def processamentoVitima():

    with lock:
        if cam.getFrameAtual() is None:
            print("frame vazio")
            return
        frame_copy = cam.getFrameAtual().copy()

    start_time = time.time()
    results = model(frame_copy, imgsz=320, conf=0.7, device=device)
    cam.limpaObjDetectados()

    boxes = results[0].boxes.xyxy.cpu().numpy()
    classes = results[0].boxes.cls.cpu().numpy()

    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = box[:4]
        centro_x = int((x1 + x2) / 2)
        centro_y = int((y1 + y2) / 2)
        largura = int(x2 - x1)
        altura = int(y2 - y1)
        area = largura * altura

        classe_idx = int(classes[i])
        classe_nome = model.names[classe_idx] if hasattr(model, "names") else str(classe_idx)

        listaObjeto = [centro_x, centro_y, area, classe_nome]
        cam.appendObjDetectados(listaObjeto)

        cv2.circle(frame_copy, (centro_x, centro_y), 5, (0, 0, 255), -1)
        cv2.putText(frame_copy, f"Area: {area}", (centro_x, centro_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.putText(frame_copy, f"Classe: {classe_nome}", (centro_x, centro_y + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

    print(cam.getObjDetectados())
    # print(frame)

    annotated_frame = results[0].plot()
    fps = 1 / (time.time() - start_time)
    cv2.putText(annotated_frame, f"FPS: {fps:.1f}", (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    with lock:
        cam.frameProcessado = annotated_frame.copy()

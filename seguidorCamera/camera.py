import cv2
import torch
from flask import Flask, Response
import time
import threading
import numpy as np
import logging
from typing import List, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

torch.set_num_threads(4)

app = Flask(__name__)

# Shared variables with proper initialization
frame: Optional[np.ndarray] = None
frameBack: Optional[np.ndarray] = None
frameProcessado: Optional[np.ndarray] = None
frameProcessadoBack: Optional[np.ndarray] = None
lock = threading.Lock()
objetos_detectados: List[Any] = []
kframe = None

# # Initialize camera with error handling
# def init_camera():
#     try:
#         # Try multiple camera indices to be more robust (0..4)
#         for idx in range(0, 5):
#             logger.info(f"Tentando abrir câmera no índice {idx}...")
#             camera = cv2.VideoCapture(idx)
#             if camera is not None and camera.isOpened():
#                 logger.info(f"Camera aberta no índice {idx}")
#                 # Configure camera properties
#                 try:
#                     camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
#                     camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#                     camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#                     camera.set(cv2.CAP_PROP_FPS, 30)
#                 except Exception:
#                     # Ignore property set failures
#                     pass
#                 return camera
#             else:
#                 logger.warning(f"Índice {idx} não disponível")

#         logger.error("Nenhuma câmera disponível nos índices testados (0-4)")
#         return None
#     except Exception as e:
#         logger.error(f"Error initializing camera: {e}")
#         return None


# camera = init_camera()
cameraFront = cv2.VideoCapture(1)
cameraBack = cv2.VideoCapture(3)

indQualidade = 4

camWidth = 160 *indQualidade
camHeight = 120 *indQualidade

cameraFront.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cameraFront.set(cv2.CAP_PROP_FRAME_WIDTH, camWidth)
cameraFront.set(cv2.CAP_PROP_FRAME_HEIGHT, camHeight)
cameraFront.set(cv2.CAP_PROP_FPS, 30)

cameraBack.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cameraBack.set(cv2.CAP_PROP_FRAME_WIDTH, camWidth)
cameraBack.set(cv2.CAP_PROP_FRAME_HEIGHT, camHeight)
cameraBack.set(cv2.CAP_PROP_FPS, 30)


# MJPEG Streaming
def atualizaTransmissaoFront():
    global frameProcessado, frame
    
    while True:
        with lock:
            
            # if frameProcessado is None:
            #     time.sleep(0.1)
            #     continue
            
            # Encode frame to JPEG
            ret, buffer = cv2.imencode('.jpg', frameProcessado, 
                                     [cv2.IMWRITE_JPEG_QUALITY, 160])
        
        if ret:
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        time.sleep(0.033)  # ~30 FPS

def atualizaTransmissaoBack():
    global frameProcessado, frameBack, frameProcessadoBack
    
    while True:
        with lock:
            
            # if frameProcessado is None:s
            #     time.sleep(0.1)
            #     continue
            
            # Encode frame to JPEG
            ret, buffer = cv2.imencode('.jpg', frameBack, 
                                     [cv2.IMWRITE_JPEG_QUALITY, 160])
        
        if ret:
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        time.sleep(0.033)  # ~30 FPS

# @app.route('/')
# def index():
#     return '<h1>IMAGENS malucas</h1> <img src="/videoFront" width="640">  <img src="/videoBack" width="640">'

@app.route('/videoFront')
def video_feed():
    return Response(atualizaTransmissaoFront(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/videoBack')
# def video_feedBack():
#     return Response(atualizaTransmissaoBack(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

def vercamera():
    global frame, frameProcessado, frameProcessadoBack, cameraFront, cameraBack, frameBack
    
    # if cameraFr is None or not camera.isOpened():
    #     logger.warning('Camera not available - tentando reiniciar')
    #     # tenta reiniciar a câmera (com backoff curto)
    #     # camera = init_camera()
    #     # time.sleep(0.5)
    #     return

    retFront, captured_frameFront = cameraFront.read()
    # retBack, captured_frameBack = cameraBack.read()
    # if not ret or captured_frame is None or getattr(captured_frame, 'size', 0) == 0:
    #     logger.debug('Leitura da câmera falhou (ret False ou frame vazio)')
    #     return

    with lock:
        frame = captured_frameFront.copy()
        # frameBack = None
        # Initialize frameProcessado if it's None
        if frameProcessado is None:
            frameProcessado = captured_frameFront.copy()
            # frameProcessadoBack = captured_frameBack.copy()

def thread_camera():
    logger.info("Camera thread started")

    while True:
        try:
            vercamera()
            time.sleep(1/30)  # ~30 FPS capture
        except Exception as e:
            logger.exception(f"Error in camera thread: {e}")
            time.sleep(1)

def iniciarThreadCamera():
    logger.info("Starting camera thread (iniciarThreadCamera)")
    threadCamera = threading.Thread(target=thread_camera)
    threadCamera.daemon = True
    threadCamera.start()

def getFrameAtual() -> Optional[np.ndarray]:
    global frame
    with lock:
        return frame.copy() if frame is not None else None
    
def getFrameBack() -> Optional[np.ndarray]:
    global frameBack
    with lock:
        return frameBack.copy() if frameBack is not None else None

def getObjDetectados() -> List[Any]:
    with lock:
        return objetos_detectados.copy()

def limpaObjDetectados():
    with lock:
        objetos_detectados.clear()
        logger.info("Cleared detected objects")

def appendObjDetectados(obj: Any):
    with lock:
        objetos_detectados.append(obj)
        logger.info(f"Added object: {obj}")

def iniciar_flask():
    """Start Flask server with better configuration"""
    logger.info("Starting Flask server on 0.0.0.0:8080")
    app.run(host='0.0.0.0', port=8080, threaded=True, debug=False, use_reloader=False)

# Cleanup function
def cleanup():
    logger.info("Cleaning up resources")
    if cameraFront is not None and cameraBack is not None:
        cameraFront.release()
        cameraBack.release()
    cv2.destroyAllWindows()

# Register cleanup on exit
import atexit
atexit.register(cleanup)
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

# Initialize camera with error handling
def init_camera():
    try:
        camera = cv2.VideoCapture(1)  # Try default camera first
        if not camera.isOpened():

            logger.warning("Camera index 0 not available, trying index 1")
            logger.warning("Camera index 1 not available, trying index 2")

            camera = cv2.VideoCapture(2)
        
        if not camera.isOpened():
            logger.error("No camera available")
            return None
            
        camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        camera.set(cv2.CAP_PROP_FPS, 60)
        
        logger.info("Camera initialized successfully")
        return camera
        
    except Exception as e:
        logger.error(f"Error initializing camera: {e}")
        return None

camera = init_camera()

# Shared variables with proper initialization
frame: Optional[np.ndarray] = None
frameProcessado: Optional[np.ndarray] = None
lock = threading.Lock()
objetos_detectados: List[Any] = []

# MJPEG Streaming
def atualizaTransmissao():
    global frameProcessado, frame
    
    while True:
        with lock:
            if frameProcessado is None:
                time.sleep(0.1)
                continue
            
            # Encode frame to JPEG
            ret, buffer = cv2.imencode('.jpg', frameProcessado, 
                                     [cv2.IMWRITE_JPEG_QUALITY, 160])
        
        if ret:
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        time.sleep(0.033)  # ~30 FPS

@app.route('/video')
def video_feed():
    return Response(atualizaTransmissao(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/health')
def health_check():
    status = camera is not None and camera.isOpened()
    logger.info(f"Health check: {status}")
    return {'status': 'ok', 'camera_available': status}

def vercamera():
    global frame, frameProcessado, camera
    
    if camera is None or not camera.isOpened():
        print('PAROU DE PEGAR IMAGEM')
        time.sleep(1)
        camera = init_camera()
        return
    
    ret, captured_frame = camera.read()
    if ret:
        with lock:
            frame = captured_frame.copy()
            # frame = cv2.flip(frame, 0)
            # Initialize frameProcessado if it's None
            if frameProcessado is None:
                frameProcessado = captured_frame.copy()

def thread_camera():
    logger.info("Camera thread started")
    
    while True:
        try:
            vercamera()
            time.sleep(0.01)  # ~100 FPS capture
        except Exception as e:
            logger.error(f"Error in camera thread: {e}")
            time.sleep(1)

def iniciarThreadCamera():
    if camera is None or not camera.isOpened():
        logger.warning("Camera not available")
        return
    
    logger.info("Starting camera thread")
    threadCamera = threading.Thread(target=thread_camera)
    threadCamera.daemon = True
    threadCamera.start()

def getFrameAtual() -> Optional[np.ndarray]:
    with lock:
        return frame.copy() if frame is not None else None

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
    if camera is not None:
        camera.release()
    cv2.destroyAllWindows()

# Register cleanup on exit
import atexit
atexit.register(cleanup)
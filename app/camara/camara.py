import cv2

def iniciar_camara():
    cap = cv2.VideoCapture(0)  # Inicia la cámara (0 es el índice de la cámara predeterminada)
    if not cap.isOpened():
        print("No se pudo abrir la cámara")
        return None         
    return cap

def obtener_frame(cap):
    ret, frame = cap.read()  # Lee un frame de la cámara
    if not ret:
        print("No se pudo leer el frame")
        return None
    return frame

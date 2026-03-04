import cv2
import face_recognition
import numpy as np


def procesar_frame(frame):
    #Esto convertira el frame de BGR a RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #Este detectara las caras en el frame
    face_locations = face_recognition.face_locations(rgb)

    num_faces = len(face_locations)

    #Politicas de deteccion

    if num_faces == 0:
        return frame, None, "No se detectó ninguna cara"
    
    if num_faces > 1:
        return frame, None, "Se detectaron múltiples caras"
    
    #Puntos clave para la deteccion de rostro
    face_lankmarks = face_recognition.face_landmarks(rgb, face_locations)

    #Vector numérico de la cara
    face_encoding = face_recognition.face_encodings(rgb, face_locations)[0]

    #Dibujar un rectángulo alrededor de la cara detectada
    top, right, bottom, left = face_locations[0]
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    #Dibujar puntos clave en la cara
    for (x,y) in face_lankmarks[0]['chin']:
        cv2.circle(frame, (x,y), 1, (0, 0, 255), -1)

    return frame, face_encoding, "Cara detectada correctamente"

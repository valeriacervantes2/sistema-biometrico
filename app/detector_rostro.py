import cv2

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

#Esto es para inicializar la cámara
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Ajusta los parametros de detección
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,    #Escala de reducción de la imagen para la detección, en este caso se reduce un 30% cada vez.
        minNeighbors=5,     #Se usa para confirmar que es realemente una cara, en este caso se verifica 5 veces.
        minSize=(30, 30)    #Tamaño mínimo de la cara a detectar, en este caso 30x30 píxeles
    
    )

    #Dibuja el rectangulo detector de rostro
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), ( 0, 255, 0), 2)

    cv2.imshow('Face Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
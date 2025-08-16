import cv2
import face_recognition
import serial
import time

# En este programa se reconoce a una persona específica y se envía un mensaje a la ESP32 cuando se reconoce.
# Solo es capaz de reconocer a una persona a la vez, en este caso Ernesto.

# Configurar puerto serial (ajusta el puerto y baudios si es necesario)
ser = serial.Serial('COM3', 115200, timeout=1)
time.sleep(2)  # Esperar que se inicialice la comunicación serial

# Cargar imagen de referencia y codificar
imagen_referencia = face_recognition.load_image_file("imagenes/Ernesto.jpg")
codificacion_referencia = face_recognition.face_encodings(imagen_referencia)[0]
nombre_referencia = "Ernesto"

codificaciones_conocidas = [codificacion_referencia]
nombres_conocidos = [nombre_referencia]

cap = cv2.VideoCapture(0)

# Control para no mandar comandos repetidos constantemente
ultimo_envio = 0
intervalo_envio = 5  # segundos

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error accediendo a la cámara")
        break

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations, num_jitters=1)

    nombres_detectados = []
    activar_sistema = False

    for codificacion in face_encodings:
        resultados = face_recognition.compare_faces(codificaciones_conocidas, codificacion)
        nombre = "Desconocido"

        if True in resultados:
            index = resultados.index(True)
            nombre = nombres_conocidos[index]
            activar_sistema = True  # Hay alguien reconocido

        nombres_detectados.append(nombre)

    # Enviar comando serial si hay persona conocida y ha pasado el intervalo
    ahora = time.time()
    if activar_sistema and (ahora - ultimo_envio) > intervalo_envio:
        ser.write(b"ACTIVAR\n")
        print("Comando ACTIVAR enviado por serial")
        ultimo_envio = ahora

    # Dibujar rectángulos y nombres
    for (top, right, bottom, left), nombre in zip(face_locations, nombres_detectados):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, nombre, (left, bottom + 25), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

    cv2.imshow("Reconocimiento Facial Fácil", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()

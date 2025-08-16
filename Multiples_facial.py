import cv2
import dlib
import os
import numpy as np
import serial  # Librería para puerto serial
import time

##En este programa esta hecho para reconcocer a multiples personas y enviar un mensaje a la ESP32 cuando se reconoce a alguien.
# Este código utiliza OpenCV y dlib para reconocimiento facial y comunicación con una ESP32 a través de un puerto serial.


dataset_path = "dataset"
tolerance = 0.6
frame_process_rate = 3

# Configurar puerto serial (ajusta COM y baudrate)
ser = serial.Serial("COM3", 115200, timeout=1)  # Cambia "COM3" al puerto correcto de tu ESP32 o arduino
time.sleep(2)  
ser.write(b"CONECTADO\n")
print("[SERIAL] Python conectado a ESP32")

# Detector de rostros y extractor de características
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
facerec = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

# Verificar si los archivos de modelo existen
def load_dataset():
    known_encodings = []
    known_names = []
    for person_name in os.listdir(dataset_path):
        person_folder = os.path.join(dataset_path, person_name)
        if not os.path.isdir(person_folder):
            continue
        for image_name in os.listdir(person_folder):
            image_path = os.path.join(person_folder, image_name)
            img = cv2.imread(image_path)
            if img is None:
                continue
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            dets = detector(rgb_img, 1)
            if len(dets) == 0:
                continue
            shape = sp(rgb_img, dets[0])
            face_encoding = np.array(facerec.compute_face_descriptor(rgb_img, shape))
            known_encodings.append(face_encoding)
            known_names.append(person_name)
    return known_encodings, known_names

def compare_faces(known_encodings, face_encoding):
    distances = np.linalg.norm(known_encodings - face_encoding, axis=1)
    min_distance = min(distances) if len(distances) > 0 else 1.0
    if min_distance < tolerance:
        return np.argmin(distances), min_distance
    return None, None

# Cargar dataset
known_encodings, known_names = load_dataset()
print(f"[INFO] Se cargaron {len(known_names)} rostros registrados.")

cap = cv2.VideoCapture(0)
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    small_frame = cv2.resize(frame, (0,0), fx=0.3, fy=0.3)
    rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_data = []
    if frame_count % frame_process_rate == 0:
        dets = detector(rgb_small, 1)
        for det in dets:
            shape = sp(rgb_small, det)
            face_encoding = np.array(facerec.compute_face_descriptor(rgb_small, shape))
            idx, dist = compare_faces(np.array(known_encodings), face_encoding)
            name = known_names[idx] if idx is not None else "Desconocido"
            face_data.append((det, name))

            # Enviar mensaje a ESP32 si reconoce alguien
            if idx is not None:
                ser.write(b"ACTIVAR\n")  # Enviar comando por serial
                print(f"[SERIAL] Enviado ACTIVAR para {name}")

    # Dibujar en pantalla
    for det, name in face_data:
        x1, y1, x2, y2 = det.left()*3.33, det.top()*3.33, det.right()*3.33, det.bottom()*3.33
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,255,0), 2)
        cv2.putText(frame, name, (int(x1), int(y1)-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    cv2.imshow("Reconocimiento Facial", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC para salir
        break

cap.release()
cv2.destroyAllWindows()
ser.close()

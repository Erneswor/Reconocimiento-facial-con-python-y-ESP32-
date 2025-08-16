import cv2
import mediapipe as mp
import serial
import time

# Configuración
ARDUINO_PORT = 'COM3' 
BAUD_RATE = 115200
GESTO_ACTIVACION = 4  # Número de dedos para activar (4 dedos)

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# Conectar con Arduino
try:
    arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
    print(f"✅ Arduino conectado en {ARDUINO_PORT}")
except:
    arduino = None
    print(f"⚠️  No se pudo conectar a Arduino")

# Función para contar dedos levantados
def contar_dedos(landmarks):
    dedos = []
    # Pulgar (comparar coordenada x)
    dedos.append(landmarks[4].x < landmarks[3].x)
    # Otros dedos (comparar coordenada y)
    for i in [8, 12, 16, 20]:  # Índice, Medio, Anular, Meñique
        dedos.append(landmarks[i].y < landmarks[i-2].y)
    return sum(dedos)

# Captura de video
cap = cv2.VideoCapture(0)
ultima_activacion = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue
    
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Contar dedos
            num_dedos = contar_dedos(hand_landmarks.landmark)
            
            # Dibujar landmarks
            mp.solutions.drawing_utils.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
                mp.solutions.drawing_styles.get_default_hand_connections_style()
            )
            
            # Mostrar conteo en pantalla
            cv2.putText(frame, f"Dedos: {num_dedos}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Activar si se detectan 4 dedos
            if num_dedos == GESTO_ACTIVACION and arduino:
                if time.time() - ultima_activacion > 5:  # Cooldown 5s
                    arduino.write(b'ACTIVAR\n')  # Enviar señal
                    print("🖐️ Señal enviada: 4 dedos detectados")
                    ultima_activacion = time.time()
    
    cv2.imshow('Control por Gestos', frame)
    if cv2.waitKey(1) & 0xFF == 27:  # Tecla ESC
        break

cap.release()
cv2.destroyAllWindows()
if arduino:
    arduino.close()
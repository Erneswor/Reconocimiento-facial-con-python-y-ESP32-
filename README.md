<div align="center">

# 🎭 Sistema de Reconocimiento Facial
### *Reconocimiento facial en tiempo real con Python y Arduino*

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?style=for-the-badge&logo=opencv&logoColor=white)
![Arduino](https://img.shields.io/badge/Arduino-Compatible-teal?style=for-the-badge&logo=arduino&logoColor=white)


*Un sistema inteligente de reconocimiento facial que conecta el mundo digital con dispositivos físicos*

</div>

---

## 🌟 Características Principales

- 🎯 **Reconocimiento facial en tiempo real** con alta precisión
- 🔗 **Integración Arduino/ESP32** para control de dispositivos
- 📷 **Soporte múltiples cámaras** (USB, webcam integrada)
- ⚡ **Procesamiento optimizado** con OpenCV y Dlib
- 🔒 **Sistema de acceso seguro** basado en biometría
- 📊 **Detección de puntos faciales** (68 landmarks)
- 🌐 **Comunicación serial** 

## 🎬 Demo

> 📹 *Próximamente: Video demostrativo del sistema en funcionamiento*

### Casos de uso comunes:
- 🚪 **Control de acceso** - Apertura automática de puertas
- 💡 **Domótica inteligente** - Activación de luces y dispositivos
- 🔔 **Sistema de alertas** - Notificaciones por personas no reconocidas
- 📱 **IoT Integration** - Conexión con sistemas smart home

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| ![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white) | 3.10+ | Lenguaje principal |
| ![OpenCV](https://img.shields.io/badge/-OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white) | 4.x | Procesamiento de imágenes |
| ![Dlib](https://img.shields.io/badge/-Dlib-FF6B6B?style=flat) | Latest | Reconocimiento facial |
| ![Arduino](https://img.shields.io/badge/-Arduino-00979D?style=flat&logo=arduino&logoColor=white) | Compatible | Control de hardware |
| ![Serial](https://img.shields.io/badge/-PySerial-4CAF50?style=flat) | Latest | Comunicación serial |

## 📋 Requisitos del Sistema

### 💻 Software
- **Sistema Operativo**: Windows 10/11, macOS, Linux
- **Python**: 3.10 o superior
- **IDE recomendado**: VS Code, PyCharm
- **Arduino IDE**: Para programar microcontroladores

### 🔧 Hardware
- **Cámara**: Webcam USB o cámara integrada (HD recomendada)
- **Microcontrolador**: Arduino UNO/Nano/Mega/ESP32
- **Conexiones**: Cable USB para comunicación serial
- **Opcional**: LEDs, buzzers, relés para dispositivos externos

### ⚡ Rendimiento Recomendado
- **RAM**: 4GB mínimo, 8GB recomendado
- **Procesador**: Intel i5 o AMD Ryzen 5 (o superior)
- **GPU**: NVIDIA (opcional, para aceleración CUDA)

## 🚀 Instalación

### 1️⃣ Clonar el repositorio
\`\`\`bash
git clone https://github.com/Erneswor/Reconocimiento-facial-con-python-y-ESP32-.git
cd reconocimiento-facial
\`\`\`

### 2️⃣ Crear entorno virtual

\`\`\`bash
python -m venv venv
venv\Scripts\activate
\`\`\`

**O instalar manualmente:**
\`\`\`bash
pip install opencv-python
pip install dlib
pip install imutils
pip install pyserial
pip install numpy
\`\`\`

**Descargar y extraer modelos:**
- [`shape_predictor_68_face_landmarks.dat`](https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2)
- [`dlib_face_recognition_resnet_model_v1.dat`](https://github.com/davisking/dlib-models/raw/master/dlib_face_recognition_resnet_model_v1.dat.bz2)
- [`shape_predictor_5_face_landmarks.dat`](https://github.com/davisking/dlib-models/raw/master/shape_predictor_5_face_landmarks.dat.bz2)

\`\`\`bash
# Extraer archivos .bz2
bunzip2 *.bz2
\`\`\`

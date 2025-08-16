# Reconocimiento Facial con Python y Arduino

Este proyecto implementa un sistema de **reconocimiento facial en tiempo real** utilizando **Python, OpenCV y Dlib**, con comunicación serial hacia un **Arduino/ESP32** para activar dispositivos externos (ej. abrir una puerta, encender un LED o un buzzer).

---

## 📌 Requisitos del sistema

- **Python**: 3.10
- **Sistema operativo**: Windows 
- **Cámara web** o cámara USB
- **Arduino UNO/Nano/Mega/ESP32** (o cualquier compatible con puerto serial)
---

## 📦 Instalación de librerías

Ejecuta los siguientes comandos en tu entorno virtual o terminal:

 📦 bash
pip install opencv-python
pip install dlib
pip install imutils
pip install pyserial

## 📂 Modelos necesarios
* shape_predictor_68_face_landmarks.dat.bz2
* dlib_face_recognition_resnet_model_v1.dat.bz2
* shape_predictor_5_face_landmarks.dat.bza
Esto modelos los deben de descomprimir

Los modelos los puedes encontra en este repositorio : *https://github.com/davisking/dlib-models.git*
Los modelos de dlib puedes encontralo en este repositorio : *https://github.com/davisking/dlib.git*

## 🔧 Notas
Para mejor rendimiento, asegúrate de usar cámara HD y buena iluminación.
Se recomienda usar dlib con CUDA si tienes GPU NVIDIA para mejorar la velocidad.
En caso de errores con los modelos .dat, verifica que estén descomprimidos y en la carpeta correcta.
Otro punto a tomar en cuenta es el puerto serial, en mi caso en el *COM3*

---




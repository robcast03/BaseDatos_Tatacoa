# import cv2 
# import cv2.aruco as aruco

# # Inicializar la captura de vídeo desde la cámara web
# cap = cv2.VideoCapture(0)

# # Crear un objeto de diccionario ArUco predeterminado
# dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)

# # Crear un objeto de parámetros ArUco
# parameters = aruco.DetectorParameters()
# detector = aruco.ArucoDetector(dictionary, parameters)

# while True:
#     # Capturar fotograma por fotograma
#     ret, frame = cap.read()

#     # Convertir el fotograma a escala de grises
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Detectar marcadores ArUco
#     corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dictionary, parameters=parameters)

#     # Dibujar los marcadores detectados en el fotograma
#     frame = aruco.drawDetectedMarkers(frame, corners, ids)

#     # Mostrar el fotograma con los marcadores detectados
#     cv2.imshow('ArUco Detection', frame)

#     # Esperar a que se presione la tecla 'q' para salir del bucle
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Liberar la captura y cerrar la ventana
# cap.release()
# cv2.destroyAllWindows()

#-------------------------------------------------------------------------------------------------------------------
from flask import Flask, render_template, Response
import cv2
import numpy as np

app = Flask(__name__)

# Inicializar la cámara (puedes ajustar los parámetros según tu configuración)
cap = cv2.VideoCapture(0)
cap.set(3, 500)
cap.set(4, 500)

# Definir los parámetros para la detección de códigos ArUco de forma alternativa
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)

parameters.minMarkerPerimeterRate = 0.02  # Ajusta este valor según tus necesidades

def gen_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convertir la imagen a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar los códigos ArUco
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
        corners_ent = np.int64(corners)
        cv2.polylines(frame, corners_ent, True, (0, 0, 255), 5)
        proporcion_cm = 0

        if corners_ent.any():
            perimetro_aruco = cv2.arcLength(corners_ent[0], True)
            proporcion_cm = perimetro_aruco / 16
            print(proporcion_cm)
            # Dibujar el valor de proporcion_cm sobre el marcador ArUco
            cv2.putText(frame, f'Proporcion: {proporcion_cm:.2f} cm', (corners_ent[0][0][0][0], corners_ent[0][0][0][1] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        else:
            print("No se han detectado marcadores ArUco en la imagen.")

        if proporcion_cm > 100:
            print("Parar rover a menos de dos mentros")
        else:
            print("Seguir avanzado")

        # Dibujar los códigos ArUco detectados en el frame
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        # Convertir el frame a JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('joy.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)


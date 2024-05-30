from flask import Flask, render_template, Response
from flask import Flask, render_template, Response
import cv2
import requests
from ultralytics import YOLO
import numpy as np
app=Flask(__name__)


#camera = cv2.VideoCapture(0)

# URL a la que enviar el video
# Definir los parámetros para la detección de códigos ArUco de forma alternativa
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)

parameters.minMarkerPerimeterRate = 0.02  # Ajusta este valor según tus necesidadesk

# Carga el modelo YOLOv8 entrenado
model = YOLO('C:/JJCA/indexprin3/indexprin3/indexprin3/model/best.pt')


def gen_frames(): 
    camera = cv2.VideoCapture(0) 
    camera.set(cv2.CAP_PROP_FRAME_WIDTH,80)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT,80)
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            #detector=cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml') # esto es de haarcasdade

            # Detectar los códigos ArUco
            corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
            corners_ent = np.int64(corners)
            cv2.polylines(frame, corners_ent, True, (0,0,255),5)
            proporcion_cm = 0


            if corners_ent.any():
     
             perimetro_aruco = cv2.arcLength(corners_ent[0], True)
             proporcion_cm=perimetro_aruco/16
             print("se han detectado marcadores ArUco en la imagen.")
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
    
            # Mostrar la imagen con los códigos ArUco detectados
            #cv2.imshow('Frame', frame)

            ##################### esto es de haarcascade #########################
           
            # faces=detector.detectMultiScale(frame,1.1,7)
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #  #Draw the rectangle around each face
            # for (x, y, w, h) in faces:
            #     cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            #     cv2.putText(frame, 'planta', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2,
            #         cv2.LINE_AA) 
            #     roi_gray = gray[y:y+h, x:x+w]
            #     roi_color = frame[y:y+h, x:x+w]
            #######################################################################    


        #################################### AQUI VA LO DE DETECCIÓN ###################

            # Realiza la detección de objetos
            results = model(frame, imgsz=640, conf=0.6)

            # Inicializa el contador de cada clase
            class_counts = [0] * len(model.names)
    
            for result in results:
               boxes = result.boxes  # Obtén las cajas de los objetos detectados

            # Cuenta el número de objetos detectados por clase
               for box in boxes:
                 cls = int(box.cls[0])  # Clase del objeto
                 class_counts[cls] += 1

                 x1, y1, x2, y2 = map(int, box.xyxy[0])  # Coordenadas de la caja
                 conf = box.conf[0]  # Confianza de la detección

                 # Dibuja la caja en la imagen
                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                 # Dibuja la etiqueta y la confianza en la imagen
                 label = f'{model.names[cls]} {conf:.2f}'
                 cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Muestra el conteo de cada clase en la imagen
            x_offset = 10  # Desplazamiento inicial para el texto en el eje x
            y_offset = 30  # Desplazamiento inicial para el texto
            for cls_id, count in enumerate(class_counts):
                text = f'{model.names[cls_id]}: {count}'
                cv2.putText(frame, text, (x_offset, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                x_offset += text_size[0] + 20  # Incrementa el desplazamiento en x para la siguiente línea de texto
    
            # Muestra el total de objetos detectados
            total_text = f'Total muestras: {sum(class_counts)}'
            cv2.putText(frame, total_text, (x_offset, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

             # Muestra la imagen con las detecciones y el conteo
            cv2.imshow('Detecciones', frame)



            #################################################################################

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # Enviar el frame a la URL especificada
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
  
    numero = 42
    return render_template('joy.html', numero=numero)
@app.route('/video_feed')
def video_feed():
    
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/ejecutar_codigo', methods=['POST'])
def ejecutar_codigo():
    # Aquí puedes colocar el código de Python que deseas ejecutar al presionar el botón
    print("Código de Python ejecutado")
    return "Código de Python ejecutado con éxito"
if __name__=='__main__':
  app.run(host='127.0.0.1',port=5000, debug=True)

# ###############################################3
# import cv2
# import numpy as np
# import time
# #import cv2.aruco as aruco

# # Inicializar la cámara (puedes ajustar los parámetros según tu configuración)
# cap = cv2.VideoCapture(0)
# cap.set(3,500)
# cap.set(4,500)

# # Definir los parámetros para la detección de códigos ArUco de forma alternativa
# dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
# parameters = cv2.aruco.DetectorParameters()
# detector = cv2.aruco.ArucoDetector(dictionary, parameters)

# parameters.minMarkerPerimeterRate = 0.02  # Ajusta este valor según tus necesidades

# while True:
#     ret, frame = cap.read()
#     if ret== False:
#         break
    
#     # Convertir la imagen a escala de grises
#     #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Detectar los códigos ArUco
#     corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
#     corners_ent = np.int64(corners)
#     cv2.polylines(frame, corners_ent, True, (0,0,255),5)
#     proporcion_cm = 0

#     if corners_ent.any():
     
#      perimetro_aruco = cv2.arcLength(corners_ent[0], True)
#      proporcion_cm=perimetro_aruco/16
#      print(proporcion_cm)
#       # Dibujar el valor de proporcion_cm sobre el marcador ArUco
#      cv2.putText(frame, f'Proporcion: {proporcion_cm:.2f} cm', (corners_ent[0][0][0][0], corners_ent[0][0][0][1] - 20),
#         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
#     else: 
#      print("No se han detectado marcadores ArUco en la imagen.")

#     if proporcion_cm > 100:
#      print("Parar rover a menos de dos mentros")
#     else:
#      print("Seguir avanzado")
    
     
#     # Dibujar los códigos ArUco detectados en el frame
#     cv2.aruco.drawDetectedMarkers(frame, corners, ids)
    
#     # Mostrar la imagen con los códigos ArUco detectados
#     cv2.imshow('Frame', frame)
    
#     # Salir del bucle si se presiona la tecla 'q'
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

#     #time.sleep(0.5)



# # Liberar la cámara y cerrar todas las ventanas
# cap.release()
# cv2.destroyAllWindows()
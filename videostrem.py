from flask import Flask, render_template, Response, request, jsonify
import cv2
import os
import numpy as np
import mysql.connector
from mysql.connector import Error
from flask_socketio import SocketIO, emit
import threading

app = Flask(__name__)
socketio = SocketIO(app)

# Inicializar la cámara
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 680)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Definir los parámetros para la detección de códigos ArUco
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
parameters = cv2.aruco.DetectorParameters()
parameters.minMarkerPerimeterRate = 0.02  # Ajusta este valor según tus necesidades

# Cargar Haarcascades para la detección de rostros
xml_path = os.path.abspath('Haarcascades/haarcascade_frontalface_default.xml')
face_detector = cv2.CascadeClassifier(xml_path)

led = [0]  # Usar una lista para permitir la mutabilidad en gen_frames

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="buggy"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    
def get_db_connectionAU():
    try:
        mydb_senrobert = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="senrobert"
        )
        if mydb_senrobert.is_connected():
            return mydb_senrobert
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def gen_frames():
    previous_led = 0  # Para almacenar el valor anterior de LED
    while True:
        success, frame = camera.read()  # Leer el frame de la cámara
        if not success:
            break
        else:
            # Convertir la imagen a escala de grises
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detectar los rostros
            faces = face_detector.detectMultiScale(gray, 1.1, 7)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(frame, 'Sub normal detectado', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

            # Detectar los códigos ArUco
            corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
            if len(corners) > 0:
                corners_ent = np.int64(corners)
                cv2.polylines(frame, corners_ent, True, (0, 0, 255), 5)
                proporcion_cm = 0

                if corners_ent.any():
                    perimetro_aruco = cv2.arcLength(corners_ent[0], True)
                    proporcion_cm = perimetro_aruco / 16
                    print(proporcion_cm)
                    cv2.putText(frame, f'Proporcion: {proporcion_cm:.2f} cm', (corners_ent[0][0][0][0], corners_ent[0][0][0][1] - 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)             

                if proporcion_cm > 100:
                    led[0] = 1
                else:
                    led[0] = 0

                # Emitir el valor de LED solo si ha cambiado
                if led[0] != previous_led:
                    socketio.emit('led_status', {'led': led[0]})
                    previous_led = led[0]

            # Dibujar los códigos ArUco detectados en el frame
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

            # Convertir el frame a JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    numero = 42
    return render_template('joy.html', numero=numero)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json
    print("Datos recibidos desde el cliente:")
    for key, value in data.items():
        print(f"{key}: {value}")

    direccion = data.get('direccion') if data.get('direccion') is not None else 0
    ruedas = float(data.get('ruedas')) if data.get('ruedas') is not None else 0

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        sql = """INSERT INTO velocidades (direccion, ruedas) VALUES (%s, %s)"""
        val = (direccion, ruedas)
        cursor.execute(sql, val)
        connection.commit()
        cursor.close()
        connection.close()

    mydb_senrobert = get_db_connectionAU()
    if mydb_senrobert:
        cursor = mydb_senrobert.cursor()
        sql = """INSERT INTO sensores (led) VALUES (%s)"""
        val = (led[0],)
        cursor.execute(sql, val)
        mydb_senrobert.commit()
        cursor.close()
        mydb_senrobert.close()

    return jsonify({'message': 'Datos recibidos correctamente'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=4000, debug=True)

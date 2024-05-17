from flask import Flask, render_template, Response,request,jsonify
import cv2
import os
import mysql.connector
from flask_socketio import SocketIO

app=Flask(__name__)
socketio = SocketIO(app)

camera = cv2.VideoCapture(0)


db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="buggy"
)


def gen_frames(): 
    camera = cv2.VideoCapture(0) 
    camera.set(cv2.CAP_PROP_FRAME_WIDTH,680)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            xml_path = os.path.abspath('Haarcascades/haarcascade_frontalface_default.xml')
            detector = cv2.CascadeClassifier(xml_path)
           
            faces=detector.detectMultiScale(frame,1.1,7)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
             #Draw the rectangle around each face
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(frame, 'planta', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2,
                    cv2.LINE_AA) 
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                

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
@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json
    print("Datos recibidos desde el cliente:")
    for key, value in data.items():
        print(key + ":", value)

    direccion = data.get('direccion') if data.get('direccion') is not None else 0
    ruedas = float(data.get('ruedas')) if data.get('ruedas') is not None else 0

    cursor = db_connection.cursor()
    sql = "INSERT INTO velocidades (direccion, ruedas) VALUES (%s, %s)"
    val = (direccion, ruedas)
    cursor.execute(sql, val)
    db_connection.commit()
    
    # Cerrar el cursor y la conexión a la base de datos
    cursor.close()

    return jsonify({'message': 'Datos recibidos correctamente'})

if __name__=='__main__':
    socketio.run(app, host='0.0.0.0', port=4000, debug=True)



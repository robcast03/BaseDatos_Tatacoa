import cv2
from flask import Flask, render_template, Response
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

rostros_cascada = cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')



def gen_frames():
    captura = cam = cv2.VideoCapture(cv2.CAP_V4L2)
    captura.set(cv2.CAP_PROP_FRAME_WIDTH,500)
    captura.set(cv2.CAP_PROP_FRAME_HEIGHT,500)
    while True:
        success, img = captura.read()
        if not success:
            break

        gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rostros = rostros_cascada.detectMultiScale(gris, 1.2, 5)

        for (x, y, w, h) in rostros:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    captura.release()
    cv2.destroyAllWindows()
  
@app.route('/')
def index():
    numero = 42
    return render_template('joy.html', numero=numero)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('request_frame')
def handle_request_frame():
    socketio.emit('frame', {'image': True, 'data': next(gen_frames())})

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True
)



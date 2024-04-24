from flask import Flask, render_template, Response
from flask import Flask, render_template, Response
import cv2
import requests
app=Flask(__name__)
camera = cv2.VideoCapture(0)

# URL a la que enviar el video



def gen_frames(): 
    camera = cv2.VideoCapture(0) 
    camera.set(cv2.CAP_PROP_FRAME_WIDTH,80)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT,80)
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            detector=cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')
           
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
@app.route('/ejecutar_codigo', methods=['POST'])
def ejecutar_codigo():
    # Aquí puedes colocar el código de Python que deseas ejecutar al presionar el botón
    print("Código de Python ejecutado")
    return "Código de Python ejecutado con éxito"
if __name__=='__main__':
  app.run(host='127.0.0.1',port=5000, debug=True)


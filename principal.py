from flask import Flask, render_template, Response
from flask import Flask, render_template, Response
import cv2
import requests
app=Flask(__name__)


@app.route('/')
def index():
  
    numero = 42
    return render_template('index.html', numero=numero)

@app.route('/ejecutar_codigo', methods=['POST'])
def ejecutar_codigo():
    # Aquí puedes colocar el código de Python que deseas ejecutar al presionar el botón
    print("Código de Python ejecutado")
    return "Código de Python ejecutado con éxito"
if __name__=='__main__':
    app.run(host='127.0.0.5',port=5000, debug=True)

from flask import Flask, render_template,jsonify,request, Response
from class_firebase_database import FirebaseDB
import time
import mysql.connector
import threading
from flask_socketio import SocketIO, emit

app=Flask(__name__)
socketio = SocketIO(app)

def show_values():
    while True:
        # Conexión a la base de datos buggy
        mydb_buggy = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="buggy"
        )
        cursor_buggy = mydb_buggy.cursor()
        sql_buggy = "SELECT direccion, ruedas FROM velocidades ORDER BY id DESC LIMIT 1"
        cursor_buggy.execute(sql_buggy)
        result_buggy = cursor_buggy.fetchone()

        # Conexión a la base de datos senrobert
        mydb_senrobert = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="senrobert"
        )
        cursor_senrobert = mydb_senrobert.cursor()
        sql_senrobert = "SELECT temperatura, presion, altitud, gas, distancia, led, lat, lon FROM sensores ORDER BY id DESC LIMIT 1"
        cursor_senrobert.execute(sql_senrobert)
        result_senrobert = cursor_senrobert.fetchone()

        if result_buggy and result_senrobert:
            # Asignar los valores de las filas a variables
            direccion, ruedas = result_buggy
            temperatura, presion, altitud, gas, distancia, led, lat, lon = result_senrobert
            
            # Enviar los valores al cliente
            socketio.emit('update_values', {
                'direccion': direccion,
                'ruedas': ruedas,
                'temperatura': temperatura,
                'presion': presion,
                'altitud': altitud,
                'gas': gas,
                'distancia': distancia,
                'led': led,
                'lat': lat,
                'lon': lon
            })
        else:
            print("No hay valores en una de las tablas")

        time.sleep(3)

thread = threading.Thread(target=show_values)
thread.daemon = True  # Esto hace que el hilo se detenga cuando el programa principal termine
thread.start()

@app.route('/')
def index():
    return render_template('Roverto.html')

@app.route('/ejecutar_codigo', methods=['POST'])
def ejecutar_codigo():
    # Aquí puedes colocar el código de Python que deseas ejecutar al presionar el botón
    print("Código de Python ejecutado")
    return "Código de Python ejecutado con éxito"

if __name__=='__main__':
    socketio.run(app, host='0.0.0.0', port=2000, debug=True)
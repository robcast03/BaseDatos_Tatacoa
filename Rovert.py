
from flask import Flask, render_template,jsonify,request, Response
from class_firebase_database import FirebaseDB
import time
import mysql.connector
import threading
from flask_socketio import SocketIO

app=Flask(__name__)
socketio = SocketIO(app)
def show_values():
     while True:
            mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="buggy"
  
)

            
            cursor = mydb.cursor()
            sql = "SELECT direccion, ruedas FROM velocidades ORDER BY id DESC LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()

            if result:
                # Asignar los valores de la fila a variables
                direccion, ruedas = result
                
                # Imprimir los valores por consola
                print("direccion:", direccion)
                print("Velocidades:", ruedas)
            else:
                print("No hay valores en la tabla")

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
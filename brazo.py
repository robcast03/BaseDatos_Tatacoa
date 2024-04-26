from flask import Flask, render_template,jsonify,request, Response
import mysql.connector
import time
import threading

app=Flask(__name__)

def show_values():
     
 while True:
            mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="angulosbrazo"
  
)

            
            cursor = mydb.cursor()
            sql = "SELECT angulo1, angulo2, angulo3, angulo4, angulo5, angulo6, angulo7, velocidad1, velocidad2, velocidad3, velocidad4, velocidad5, velocidad6, velocidad7, referancia, valorX, valorY, valorZ FROM angulos ORDER BY id DESC LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()

            if result:
                # Asignar los valores de la fila a variables
                angulo1, angulo2, angulo3, angulo4, angulo5, angulo6, angulo7, velocidad1, velocidad2, velocidad3, velocidad4, velocidad5, velocidad6, velocidad7, referencia, posicionX, posicionY, posicionZ = result
                
                # Imprimir los valores por consola
                print("Angulos:", angulo1, angulo2, angulo3, angulo4, angulo5, angulo6, angulo7)
                print("Velocidades:", velocidad1, velocidad2, velocidad3, velocidad4, velocidad5, velocidad6, velocidad7)
                print("Referencia:", referencia)
                print("Posición (X, Y, Z):", posicionX, posicionY, posicionZ)
            else:
                print("No hay valores en la tabla")

            time.sleep(3)

    

thread = threading.Thread(target=show_values)
thread.daemon = True  # Esto hace que el hilo se detenga cuando el programa principal termine
thread.start()

@app.route('/')
def index():
  
    return render_template('brazo.html',)

@app.route('/ejecutar_codigo', methods=['POST'])
def ejecutar_codigo():
    # Aquí puedes colocar el código de Python que deseas ejecutar al presionar el botón
    print("Código de Python ejecutado")
    return "Código de Python ejecutado con éxito"
if __name__=='main_':
    app.run(host='127.0.0.7',port=5000, debug=True)
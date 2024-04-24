
from flask import Flask, render_template,jsonify,request, Response
from class_firebase_database import FirebaseDB
import time
import threading

app=Flask(__name__)

path ="basededatosprueva-79653-firebase-adminsdk-uu60k-78a8daca61.json"
url = "https://basededatosprueva-79653-default-rtdb.firebaseio.com/"
fb_db = FirebaseDB(path,url)
datos_mapa={
        'lat': 4.6767219,
        'lon':-74.201803111,
    }
print("Valores de los ángulos que se van a enviar:", datos_mapa)
fb_db.write_record('/Mapa/Cordenadas', datos_mapa)
datos_angulos = fb_db.read_record('/angulosBrazo/angulos')
# Suponiendo que `fb_db` es una instancia de la clase FirebaseDB y `read_record` devuelve un diccionari
def obtener_datos_actualizados():
    # Bucle infinito para obtener datos actualizados
    while True:
        # Obtener los datos de la base de datos Firebase
        datos_angulos = fb_db.read_record('/angulosBrazo/angulos')

        # Verificar si los datos existen antes de intentar acceder a ellos
        if datos_angulos:
            # Almacenar los valores en variables individuales
            angulo1 = datos_angulos.get('angulo1', 0)
            angulo2 = datos_angulos.get('angulo2', 0)
            angulo3 = datos_angulos.get('angulo3', 0)
            angulo4 = datos_angulos.get('angulo4', 0)
            angulo5 = datos_angulos.get('angulo5', 0)
            velocidad1 = datos_angulos.get('velocidad1', 0)
            velocidad2 = datos_angulos.get('velocidad2', 0)
            velocidad3 = datos_angulos.get('velocidad3', 0)
            velocidad4 = datos_angulos.get('velocidad4', 0)
            velocidad5 = datos_angulos.get('velocidad5', 0)

            # Imprimir las variables
            print("Angulo 1:", angulo1)
            print("Angulo 2:", angulo2)
            print("Angulo 3:", angulo3)
            print("Angulo 4:", angulo4)
            print("Angulo 5:", angulo5)
            print("Velocidad 1:", velocidad1)
            print("Velocidad 2:", velocidad2)
            print("Velocidad 3:", velocidad3)
            print("Velocidad 4:", velocidad4)
            print("Velocidad 5:", velocidad5)
        else:
            print("No se encontraron datos de ángulos.")

        # Esperar un tiempo antes de volver a obtener los datos
        time.sleep(10)  # Espera 10 segundos antes de volver a obtener los datos
# Aquí creamos un hilo para ejecutar la función obtener_datos_actualizados
thread = threading.Thread(target=obtener_datos_actualizados)
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
    app.run(host='127.0.0.9',port=5000, debug=True)
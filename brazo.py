from flask import Flask, render_template,jsonify,request, Response
from class_firebase_database import FirebaseDB
import time


app=Flask(__name__)
path ="basededatosprueva-79653-firebase-adminsdk-uu60k-78a8daca61.json"
url = "https://basededatosprueva-79653-default-rtdb.firebaseio.com/"
fb_db = FirebaseDB(path,url)
def obtener_datos_actualizados_buggy():
    datos_actualizados_buggy= {}  # Inicializar datos_actualizados fuera del bucle

    # Bucle infinito para obtener datos actualizados
    while True:
        # Obtener los datos de la base de datos Firebase
        datos_buggy = fb_db.read_record('/Buggy/velocidades')

        # Verificar si los datos existen antes de intentar acceder a ellos
        if datos_buggy:
            # Almacenar los valores en variables individuales
            direccion = datos_buggy.get('direccion', 0)
            ruedas = datos_buggy.get('ruedas', 0)
            

            # Imprimir las variables
            print("direccion:", direccion)
            print("ruedas:", ruedas)
          

            # Actualizar datos_actualizados con los nuevos valores
            datos_actualizados_buggy = {
                'direccion': direccion,
                'ruedas': ruedas
                
            }

        else:
            print("No se encontraron datos de ángulos.")

        # Esperar un tiempo antes de volver a obtener los datos
        time.sleep(3)

obtener_datos_actualizados_buggy()

def obtener_datos_actualizados():
    datos_actualizados = {}  # Inicializar datos_actualizados fuera del bucle

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
            angulo6 = datos_angulos.get('angulo6', 0)
            angulo7 = datos_angulos.get('angulo7', 0)
            velocidad1 = datos_angulos.get('velocidad1', 0)
            velocidad2 = datos_angulos.get('velocidad2', 0)
            velocidad3 = datos_angulos.get('velocidad3', 0)
            velocidad4 = datos_angulos.get('velocidad4', 0)
            velocidad5 = datos_angulos.get('velocidad5', 0)
            velocidad6 = datos_angulos.get('velocidad6', 0)
            velocidad7 = datos_angulos.get('velocidad7', 0)

            # Imprimir las variables
            print("Angulo 1:", angulo1)
            print("Angulo 2:", angulo2)
            print("Angulo 3:", angulo3)
            print("Angulo 4:", angulo4)
            print("Angulo 5:", angulo5)
            print("Angulo 6:", angulo6)
            print("Angulo 7:", angulo7)
            print("Velocidad 1:", velocidad1)
            print("Velocidad 2:", velocidad2)
            print("Velocidad 3:", velocidad3)
            print("Velocidad 4:", velocidad4)
            print("Velocidad 5:", velocidad5)
            print("Velocidad 6:", velocidad6)
            print("Velocidad 7:", velocidad7)

            # Actualizar datos_actualizados con los nuevos valores
            datos_actualizados = {
                'angulo1': angulo1,
                'angulo2': angulo2,
                'angulo3': angulo3,
                'angulo4': angulo4,
                'angulo5': angulo5,
                'velocidad1': velocidad1,
                'velocidad2': velocidad2,
                'velocidad3': velocidad3,
                'velocidad4': velocidad4,
                'velocidad5': velocidad5
            }

        else:
            print("No se encontraron datos de ángulos.")

        # Esperar un tiempo antes de volver a obtener los datos
        time.sleep(3)

    # Fuera del bucle while, ya no es necesario devolver datos_actualizados

# Llamar a la función para obtener datos actualizados
obtener_datos_actualizados()




@app.route('/')
def index():
  
    return render_template('brazo.html',)

@app.route('/ejecutar_codigo', methods=['POST'])
def ejecutar_codigo():
    # Aquí puedes colocar el código de Python que deseas ejecutar al presionar el botón
    print("Código de Python ejecutado")
    return "Código de Python ejecutado con éxito"
if __name__=='__main__':
    app.run(host='127.0.0.7',port=5000, debug=True)
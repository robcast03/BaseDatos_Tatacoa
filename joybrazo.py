from flask import Flask, render_template, jsonify, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="angulosbrazo",
            connect_timeout=10
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json
    print("Datos recibidos desde el cliente:")
    for key, value in data.items():
        print(f"{key}: {value}")

    # Obtener los ángulos del JSON recibido y asegurar que no sean None
    angulo1 = float(data.get('angulo1', 0.0) or 0.0)
    angulo2 = float(data.get('angulo2', 0.0) or 0.0)
    angulo3 = float(data.get('angulo3', 0.0) or 0.0)
    angulo4 = float(data.get('angulo4', 0.0) or 0.0)
    angulo5 = float(data.get('angulo5', 0.0) or 0.0)
    angulo6 = float(data.get('angulo6', 0.0) or 0.0)
    angulo7 = float(data.get('angulo7', 0.0) or 0.0)
    velocidad1 = float(data.get('vel1', 0.0) or 0.0)
    velocidad2 = float(data.get('vel2', 0.0) or 0.0)
    velocidad3 = float(data.get('vel3', 0.0) or 0.0)
    velocidad4 = float(data.get('vel4', 0.0) or 0.0)
    velocidad5 = float(data.get('vel5', 0.0) or 0.0)
    velocidad6 = float(data.get('vel6', 0.0) or 0.0)
    velocidad7 = float(data.get('vel7', 0.0) or 0.0)
    referencia = float(data.get('ref', 0.0) or 0.0)
    posicionX = float(data.get('posx', 0.0) or 0.0)
    posicionY = float(data.get('posy', 0.0) or 0.0)
    posicionZ = float(data.get('posz', 0.0) or 0.0)

    print(angulo1, angulo2, angulo3, angulo4, angulo5, angulo6, angulo7, 
          velocidad1, velocidad2, velocidad3, velocidad4, velocidad5, 
          velocidad6, velocidad7, referencia, posicionX, posicionY, posicionZ)

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        sql = """
            INSERT INTO angulos 
            (angulo1, angulo2, angulo3, angulo4, angulo5, angulo6, angulo7, 
             velocidad1, velocidad2, velocidad3, velocidad4, velocidad5, 
             velocidad6, velocidad7, referancia, valorx, valory, valorz) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        val = (angulo1, angulo2, angulo3, angulo4, angulo5, angulo6, angulo7, 
               velocidad1, velocidad2, velocidad3, velocidad4, velocidad5, 
               velocidad6, velocidad7, referencia, posicionX, posicionY, posicionZ)
        cursor.execute(sql, val)
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Datos recibidos correctamente'})
    else:
        return jsonify({'message': 'Error connecting to the database'}), 500

@app.route('/')
def index():
    return render_template('joybrazo.html')

@app.route('/ejecutar_codigo', methods=['POST'])
def ejecutar_codigo():
    print("Código de Python ejecutado")
    return "Código de Python ejecutado con éxito"

if __name__ == '__main__':
    app.run(host='127.0.0.2', port=5000, debug=True)


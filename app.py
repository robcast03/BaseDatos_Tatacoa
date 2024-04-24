from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# Configuración de la conexión a la base de datos MySQL
config = {
  'user': 'root',
  'password': '',
  'host': 'localhost',
  'database': 'posicion_1'
}

@app.route('/')
def index():
    
    try:
        # Establecer la conexión a la base de datos
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Realizar una consulta SQL para obtener los datos de la tabla
        cursor.execute("SELECT * FROM posicion1")
        rows = cursor.fetchall()

        # Convertir los datos a una lista de diccionarios
        data = [{'id': row[0], 'roll': row[1]} for row in rows]

        # Cerrar el cursor y la conexión
        cursor.close()
        conn.close()

        # Devolver los datos como JSON
        return jsonify(data)
    except mysql.connector.Error as err:
        return str(err)


if __name__ == '__main__':
    app.run(debug=True)


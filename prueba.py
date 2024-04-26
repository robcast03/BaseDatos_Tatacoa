from flask import Flask,render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

db_connection = mysql.connector.connect(
    host="172.17.32.116",
    user="root",
    password="",
    database="brazo"
)

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json

    for i in range(1, 8):
        if data[f'angulo{i}'] is None:
            data[f'angulo{i}'] = 0
    
    # Asigna un valor predeterminado de 0 si alguna velocidad es nula
    for i in range(1, 8):
        if data[f'vel{i}'] is None:
            data[f'vel{i}'] = 0

    if data[f'ref'] is None:
            data[f'ref'] = 0

    cursor = db_connection.cursor()
    sql = "INSERT INTO posiciones (angulo1, angulo2, angulo3, angulo4, angulo5, angulo6, angulo7, vel1, vel2, vel3, vel4, vel5, vel6, vel7, referencia) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (data['angulo1'], data['angulo2'], data['angulo3'], data['angulo4'], data['angulo5'], data['angulo6'], data['angulo7'], data['vel1'], data['vel2'], data['vel3'], data['vel4'], data['vel5'], data['vel6'], data['vel7'], data['ref'])
    cursor.execute(sql, val)
    db_connection.commit()
    
    # Cerrar el cursor y la conexión a la base de datos
    cursor.close()

    return jsonify({'message': 'Datos recibidos correctamente'})


@app.route('/')
def index():
    return render_template('joybrazo.html')

if __name__ == '__main__':
    app.run(debug=True)
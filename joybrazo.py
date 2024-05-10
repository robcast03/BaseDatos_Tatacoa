
from flask import Flask, render_template,jsonify,request, Response
import mysql.connector
app=Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="angulosbrazo",
    connect_timeout=10000
)


@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json
    print("Datos recibidos desde el cliente:")
    for key, value in data.items():
        print(key + ":", value)
         # Obtener los ángulos del JSON recibido
    angulo1 = float(data.get('angulo1')) if data.get('angulo1') is not None else 0
    angulo2 = float(data.get('angulo2')) if data.get('angulo2') is not None else 0
    angulo3 = float(data.get('angulo3')) if data.get('angulo3') is not None else 0
    angulo4 = float(data.get('angulo4')) if data.get('angulo4') is not None else 0
    angulo5 = float(data.get('angulo5')) if data.get('angulo5') is not None else 0
    angulo6 = float(data.get('angulo6')) if data.get('angulo6') is not None else 0
    angulo7 = float(data.get('angulo7')) if data.get('angulo7') is not None else 0
    velocidad1 = float(data.get('vel1')) if data.get('vel1') is not None else 0
    velocidad2 = float(data.get('vel2')) if data.get('vel2') is not None else 0
    velocidad3 = float(data.get('vel3')) if data.get('vel3') is not None else 0
    velocidad4 = float(data.get('vel4')) if data.get('vel4') is not None else 0
    velocidad5 = float(data.get('vel5')) if data.get('vel5') is not None else 0
    velocidad6 = float(data.get('vel6')) if data.get('vel6') is not None else 0
    velocidad7 = float(data.get('vel7')) if data.get('vel7') is not None else 0
    referencia = float(data.get('ref'))if data.get('ref') is not None else 0
    posicionX = float(data.get('posx'))if data.get('posx') is not None else 0
    posicionY = float(data.get('posy'))if data.get('posy') is not None else 0
    posicionZ = float(data.get('posz'))if data.get('posz') is not None else 0
    print(angulo1, angulo2, angulo3,angulo4,angulo5,angulo6,angulo7,velocidad1,velocidad2,velocidad3,velocidad4,velocidad5,velocidad6,velocidad7, referencia,posicionX,posicionY,posicionZ)
    # Guardar los ángulos en la base de datos de Firebase
    cursor = mydb.cursor()
    sql = "INSERT INTO angulos(angulo1, angulo2, angulo3,angulo4,angulo5,angulo6,angulo7,velocidad1,velocidad2,velocidad3,velocidad4,velocidad5,velocidad6,velocidad7, referancia,valorx,valory,valorz) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (angulo1, angulo2, angulo3,angulo4,angulo5,angulo6,angulo7,velocidad1,velocidad2,velocidad3,velocidad4,velocidad5,velocidad6,velocidad7, referencia,posicionX,posicionY,posicionZ)  # Asegúrate de tener los valores correctos aquí
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    

   
    return jsonify({'message': 'Datos recibidos correctamente'})
           

@app.route('/')
def index():
  
    return render_template('joybrazo.html')
@app.route('/ejecutar_codigo', methods=['POST'])
def ejecutar_codigo():
    # Aquí puedes colocar el código de Python que deseas ejecutar al presionar el botón
    print("Código de Python ejecutado")
    return "Código de Python ejecutado con éxito"
if __name__=='__main__':
    app.run(host='127.0.0.2',port=5000, debug=True)
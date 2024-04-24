from flask import Flask, request

app = Flask(__name__)

@app.route('/datosBrazo', methods=['POST'])
def receive_data():
    data = request.json
    print("Datos recibidos desde el cliente:")
    for key, value in data.items():
        print(key + ":", value)
    
    # Obtener los valores de las claves correspondientes
    Joint1 = data.get('Joint1', 0)
    Joint2 = data.get('Joint2', 0)
    Joint3 = data.get('Joint3', 0)
    Joint4 = data.get('Joint4', 0)
    Joint5 = data.get('Joint5', 0)
    Motor1 = data.get('Motor1', 0)
    Motor2 = data.get('Motor2', 0)
    Motor3 = data.get('Motor3', 0)
    Motor4 = data.get('Motor4', 0)
    Motor5 = data.get('Motor5', 0)

    # Aquí puedes hacer lo que desees con estos valores, por ejemplo, guardarlos en una base de datos

    return "Datos recibidos correctamente por el servidor."

if __name__ == '__main__':
    app.run()







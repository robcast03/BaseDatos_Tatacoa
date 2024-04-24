from flask import Flask, render_template, jsonify, request
import socket
import json

app = Flask(__name__)

# Configuración del cliente
HOST = '127.0.0.1'  # Dirección IP del servidor
PORT = 5000       # Puerto para la conexión con el servidor TCP

# Función para enviar los datos a otro script Python
def enviar_datos_a_otro_script(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data_string = json.dumps(data)
        s.sendall(data_string.encode())

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json
    print("Datos recibidos desde el cliente:")
    for key, value in data.items():
        print(key + ":", value)
    enviar_datos_a_otro_script(data)
    return jsonify({'message': 'Datos recibidos correctamente'})

@app.route('/')
def index():
    return render_template('brazo.html')

if __name__=='__main__':
    app.run(host='127.0.0.7', port=5000, debug=True)









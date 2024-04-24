import socket
import sqlite3

# Configuración del servidor
HOST = '127.0.0.1'  # Dirección IP del servidor
PORT = 65432        # Puerto para la conexión

# Función para llenar la base de datos con los datos del archivo
def llenar_base_de_datos(datos):
    # Conectar a la base de datos (si no existe, se creará)
    conn = sqlite3.connect('ejemplo.db')
    cursor = conn.cursor()
    # Crear tabla si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                      (id INTEGER PRIMARY KEY, nombre TEXT)''')
    # Insertar datos en la tabla
    cursor.executemany("INSERT INTO usuarios (nombre) VALUES (?)", datos)
    conn.commit()
    conn.close()

# Configurar el servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    print("Servidor esperando conexión...")
    conn, addr = s.accept()
    with conn:
        print('Conexión establecida desde', addr)
        # Recibir datos del archivo
        datos_del_archivo = conn.recv(1024).decode()
        print("Datos recibidos del cliente:")
        print(datos_del_archivo)
        # Parsear los datos del archivo
        datos_parseados = [tuple(line.strip().split(',')) for line in datos_del_archivo.split('\n')]
        # Llenar la base de datos con los datos del archivo
        llenar_base_de_datos(datos_parseados)
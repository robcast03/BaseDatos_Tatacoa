import socket

# Configuración del cliente
HOST = '127.0.0.1'  # Dirección IP del servidor
PORT = 65432        # Puerto para la conexión

# Datos a enviar
datos_a_enviar = """Juan
María
Pedro"""

# Establecer conexión con el servidor y enviar datos
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # Enviar datos al servidor
    s.sendall(datos_a_enviar.encode())
    print("Datos enviados al servidor.")
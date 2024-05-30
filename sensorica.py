import mysql.connector
import serial
import time

# Define los parámetros de la conexión serial
puerto = "COM3"
baudrate = 115200

# Establece la conexión con la base de datos
try:
    conexion = mysql.connector.connect(
        user='root',
        host='localhost',
        database='senrobert',
        password=''
    )
except mysql.connector.Error as err:
    print(f"Error conectando a la base de datos: {err}")
    exit(1)

# Establece la conexión serial
try:
    ser = serial.Serial(puerto, baudrate)
except serial.SerialException as e:
    print(f"Error abriendo el puerto serial: {e}")
    conexion.close()
    exit(1)

# Ignora las primeras 10 líneas (mensajes del ESP32)
for _ in range(10):
    ser.readline()  # Lee y descarta cada línea

try:
    while True:
        # Leer valor de led desde la base de datos
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT led FROM sensores ORDER BY id DESC LIMIT 1")
            result = cursor.fetchone()
            if result:
                led = result[0]
                ser.write(str(led).encode())
                print(f"Valor de led obtenido de la base de datos: {led}")
            else:
                led = 1  # Valor por defecto en caso de no encontrar registros
                print("No se encontraron registros en la base de datos. Usando valor por defecto para led.")
        except mysql.connector.Error as err:
            print(f"Error al leer valor de led desde la base de datos: {err}")
            led = 1  # Valor por defecto en caso de error
            print("Usando valor por defecto para led.")

        # Leer datos del puerto serial
        try:
            data = ser.readline().decode().strip()
        except serial.SerialException as e:
            print(f"Error leyendo del puerto serial: {e}")
            break

        # Espera un segundo antes de enviar el siguiente dato
        time.sleep(1)

        # Divide los datos en valores individuales
        data_split = data.split(";")
        if len(data_split) == 5:
            # Convertir los valores de cadena a los tipos de datos apropiados
            try:
                gas = float(data_split[0])
                temperatura = float(data_split[1])
                altitud = float(data_split[2])
                presion = float(data_split[3])
                distancia = float(data_split[4])
                lat = 7  # Ajusta según tus necesidades
                lon = 8  # Ajusta según tus necesidades
                
                insertar = "INSERT INTO sensores (temperatura, presion, altitud, gas, distancia, led, lat, lon) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                valores = (temperatura, presion, altitud, gas, distancia, led, lat, lon)
                
                cursor.execute(insertar, valores)
                conexion.commit()
                print("Valores insertados correctamente.")
            except ValueError as e:
                print(f"Error convirtiendo los datos: {e}")
            except mysql.connector.Error as err:
                print(f"Error insertando datos en la base de datos: {err}")

        # Retraso entre lecturas
        time.sleep(1)
finally:
    # Cerrar el puerto serial y la conexión a la base de datos
    ser.close()
    conexion.close()

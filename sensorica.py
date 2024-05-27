
import mysql.connector
from mysql.connector import Error
import serial
import time

# Define serial parameters
port = "COM9"  # Replace with the actual port
baudrate = 115200
conexion = mysql.connector.connect(
    
    user='root',
    host='localhost',
    database='senrobert',
    password=''

)


# Establish serial connection
ser = serial.Serial(port, baudrate)
# Variables to store sensor data
gas = 0.0
temperature = 0.0
altitude = 0.0
pressure = 0.0
distance = 0.0
data_to_send = "2"
# Ignore the first 10 lines (messages from ESP32)
for _ in range(10):
    ser.readline()  # Read and discard each line

while True:
    # Read data from the serial port
    data = ser.readline().decode().strip()
    ser.write(data_to_send.encode())
    # Espera un segundo antes de enviar el siguiente dato
    time.sleep(1)
    # Split the data into individual values
    data_split = data.split(";")
    if len(data_split) == 5:
        # Convert string values to appropriate data types
        gas = float(data_split[0])
        temperatura = float(data_split[1])
        altitud = float(data_split[2])
        presion = float(data_split[3])
        distancia = float(data_split[4])
        led=2
        lat=7
        lon=8
    insertar="INSERT INTO sensores(temperatura, presion, altitud, gas, distancia,led,lat,lon) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
    valores=(temperatura,presion,altitud,gas,distancia,led,lat,lon)
    mibase=conexion.cursor()
    mibase.execute(insertar,valores)
    conexion.commit()
    print("Valores insertados correctamente.")

    # Delay between readings
    time.sleep(1)






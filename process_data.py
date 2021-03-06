import glob
import sys
import mysql.connector
from pprint import pprint

# this port address is for the serial tx/rx pins on the GPIO header
import serial

SERIAL_PORT = '/dev/ttyAMA0'
# SERIAL_PORT = 'COM7'
# be sure to set this to the same rate used on the Arduino
SERIAL_RATE = 9600

mydb = mysql.connector.connect(
    database="envolsadora",
    host="localhost",
    user="root",
    passwd="tecnomotor"
)

mycursor = mydb.cursor()


def serial_ports():
    print("Verificando Conexion")
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.timeout = 1.0
            try:
                asd = s.read(100).decode('utf-8')
                if asd:
                    result.append(port)
            except Exception as e:
                print(e)
        except (OSError, serial.SerialException):
            pass
    return result


def read_port(puertos):
    for puerto in puertos:
        try:
            ser = serial.Serial(puerto, SERIAL_RATE)
            numeros = []
            while True:
                try:
                    reading = ser.readline().decode('utf-8')
                    if reading and reading[10].isnumeric():
                        numero = float(reading[6:14])
                        print(numero)
                        if numero > 10:
                            numeros.append(numero)
                        else:

                            if len(numeros) > 0:
                                max_item = max(numeros, key=float)
                                print("guardando peso",str(max_item))
                                mycursor.execute("insert into pesajes (pesaje) values (" + str(max_item) + ")")

                            numeros = []
                except Exception as e:
                    pass
        except serial.SerialException as ecxeption:
            print('Ha ocurrido un error')
            print(ecxeption)
            pass


if __name__ == "__main__":

    array_puertos_disponibles = serial_ports()
    if len(array_puertos_disponibles) > 0:
        print("Iniciando guardado de pesajes")
        read_port(array_puertos_disponibles)
    else:
        input('No se ha podido establecer una conexion, presione enter para salir')

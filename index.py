import glob
import sys

import serial


def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
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
            asd = s.read(100).decode('utf-8')
            if asd:
                print(asd)
                result.append(port)
        except (OSError, serial.SerialException):
            pass

    return result


if __name__ == "__main__":
    variable = serial_ports()
    print(variable)
    if len(variable) > 0:
        print('Se encontro Conexion')
        print('Puertos: ' + ','.join(variable))

    else:
        print('No se ha podido establecer una conexion')

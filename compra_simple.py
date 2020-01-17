# import requests
# import simplejson as json
#
# var = {
#     "public_key": "5Omt7ILlnkj1ozdfvGGsDvGzglIB7tNb",
#     "operation": {
#         "token": "2551d7b3e1b3f6e57574f0a7879e7cf8",
#         "shop_process_id": 408778,
#         "amount": "398531.00",
#         "currency": "PYG",
#         "additional_data": "",
#         "description": "に到着を待 1",
#         "return_url": "https://comercios.bancard.com.py/services/vpos/test_case/408778/result",
#         "cancel_url": "https://comercios.bancard.com.py/services/vpos/test_case/408778/result"
#     },
#     "test_client": "true"
# }
# # print(var)
#
# url = "https://vpos.infonet.com.py:8888/vpos/api/0.3/single_buy"
# data = var
# headers = {'Content-type': 'application/json'}
# r = requests.post(url, data=json.dumps(data), headers=headers)
# print(r)
# print(r.content)


import sys
import glob
import serial


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
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
            if port != 'COM4':
                print(port)
                asd = s.read(100)
                print(asd.decode("utf-8"))
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


if __name__ == '__main__':
    print(serial_ports())



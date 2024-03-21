import serial
import math
import serial.tools.list_ports

serialInst = serial.Serial()

def Connect_Serial(Serial_Port):
    serialInst.baudrate = 115200
    serialInst.port = Serial_Port
    serialInst.open()
    


def get_SerialPorts():
    return serial.tools.list_ports.comports()

def is_float(string):
    if string.count(".") == 1:
        if string.replace(".", "").replace("+", "").replace("-", "").isnumeric():
            return True
        else:
            return False
    else:
        return False

def ReadData():
    #serialInst.flush()
    packet = serialInst.readline()
    while( "$"  not in str(packet) and len(str(packet))!=135):
        packet = serialInst.readline()

    word=str(packet).strip("b'$").strip("'\\n")
    lista_parole = word.strip(";").split(",").copy()

    return lista_parole

def check_sum_calculator(strin):
    somma=[0,0,0,0,0,0,0]

    for lettera in  (strin):
        check=bin(ord(lettera))[2:]
        for i in range(0,len(check)):
            somma[len(somma)-i-1]=somma[len(somma)-i-1]^int(check[len(check)-i-1])

        tot=0
    for i in range(0,len(somma)):
        tot+=somma[i]*(2**(len(somma)-1-i))
    return hex(tot)
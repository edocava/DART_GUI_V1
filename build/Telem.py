import serial
import math
import serial.tools.list_ports

serialInst = serial.Serial

def Connect_Serial(Serial_Port):
    serialInst.baudrate = 115200
    serialInst.port = Serial_Port
    serialInst.open()
    


def get_SerialPorts():
    return serial.tools.list_ports.comports()

def is_float(string):
    if string.count(".") <= 1:
        if string.replace(".", "").replace("+", "").replace("-", "").isnumeric():
            return True
        else:
            return False
    else:
        return False

def ReadData():
    #serialInst.flush()
    packet = serialInst.read_until(expected=b"\n",size=None)
    print(packet)
    #while( "$"  not in str(packet) and len(str(packet))!=135):
    #    packet = serialInst.read(64)

    word=str(packet).strip("b'$").strip("'\\n")
    lista_parole = word.strip(";").split(",").copy()
    
    if pkt_check(packet,lista_parole):
        lista_parole.insert(18,True)
    else:
        lista_parole.insert(18,False)
    
    return lista_parole

def checksum(string):
    result = 0
    hex_str = '00'
    for i in range(len(string)-4):
        result = result ^ string[i]
    
    #result = result % 256
    hex_str = "{:02x}".format(result)

    return hex_str.upper()

def pkt_check(String,Packet):
    Check_Flag = True
    if len(Packet) == 18:
        for i in range(1,17):
            if is_float(Packet[i]) == False:
                Check_Flag = False

        if Check_Flag:
            if checksum(String) != Packet[17]:
                Check_Flag = False
    else:
        Check_Flag = False
    return Check_Flag

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
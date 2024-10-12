import tkinter as tk

import serial
import struct
from enum import IntEnum
import serial.tools.list_ports as ports

serialInst = serial.Serial()

MB_GET_STATUS = 0

TIMEOUT_STD = 2.0
TIMEOUT_RESET = 5.0


def init_Serial():
    serialInst.baudrate = 115200
    serialInst.parity = serial.PARITY_NONE
    serialInst.stopbits = serial.STOPBITS_ONE
    serialInst.bytesize = serial.EIGHTBITS
    serialInst.timeout = 2.0
    # print("Listing all available ports...")
    # for [index, port] in enumerate(ports.comports()):
    #     print(f"{index} > {str(port).split(' ')[0]}")
    # opt = int(input("Select port: "))
    # Connect_Serial(str(ports.comports()[opt]).split(' ')[0])


def choose_Serial_term(text_widget: tk.Text):
    while True:
        opt = text_widget.get("end-1l linestart", "end-1c").strip()
        opt = opt.replace('> ', '')
        try:
            Connect_Serial(str(ports.comports()[int(opt)]).split(' ')[0])
            text_widget.insert(tk.END, f"Serial port: {str(ports.comports()[int(opt)]).split(' ')[0]} connected\n")
            return True
        except:
            text_widget.insert(tk.END, "> Syntax Error!\n")
            text_widget.insert(tk.END, "> Listing all available ports...\n")
            for [index, port] in enumerate(ports.comports()):
                text_widget.insert(tk.END, f"{index} > {str(port).split(' ')[0]}\n")
            text_widget.insert(tk.END, "Select port: ")
            return False


def set_timeout(timeout):
    serialInst.timeout = timeout


class MB_STATE(IntEnum):
    MB_FSM_GET_STATUS = 0,
    MB_SLEEP_REQ = 1,
    MB_WAKEUP_REQ = 2,
    MB_DISARM_REQ = 3,
    MB_ARM_REQ = 4

    @classmethod
    def items(cls):
        return [(e.name, e.value) for e in cls]


class MB_CMD(IntEnum):
    MB_INIT_CMD_GET_STATUS = 0,
    MB_INIT_CMD_RESET = 1,
    MB_INIT_CMD_GET_ERRORS = 2

    @classmethod
    def items(cls):
        return [(e.name, e.value) for e in cls]


class MB_FSM(IntEnum):
    MB_STDBY_STATE = 0,
    MB_INIT_STATE = 1,
    MB_READY_STATE = 2,
    MB_ARM_STATE = 3,
    MB_PRE_THR_STATE = 4,
    MB_THR_STATE = 5,
    MB_COAST_STATE = 6,
    MB_DROGUE_STATE = 7,
    MB_FINAL_STATE = 8,
    MB_LAND_STATE = 9

    @classmethod
    def items(cls):
        return [(e.name, e.value) for e in cls]

    @classmethod
    def to_dict(cls):
        return {e.value: e.name for e in cls}


class MB_ERROR(IntEnum):
    ERR_BITMSK_SHIFT_IMU = 0,
    ERR_BITMSK_SHIFT_MAG = 1,
    ERR_BITMSK_SHIFT_GPS = 2,
    ERR_BITMSK_SHIFT_ALT = 3,
    ERR_BITMSK_SHIFT_PB_INIT = 4,
    ERR_BITMSK_SHIFT_PB_OP = 5,
    ERR_BITMSK_SHIFT_LD_COM = 6,
    ERR_BITMSK_SHIFT_LD_SD = 7

    @classmethod
    def items(cls):
        return [(e.name, e.value) for e in cls]


def Connect_Serial(Serial_Port: str):
    serialInst.port = Serial_Port
    serialInst.open()


def ReadData():
    packet = serialInst.read(13)

    if len(packet) == 0:
        print("General Communication Error")
        return None, None, None, None, None, None

    state = packet[0]
    err = packet[1]

    latb = packet[2:6]
    lonb = packet[6:10]
    altb = packet[10:12]
    chk = packet[12]

    lat = struct.unpack('f', latb)
    lon = struct.unpack('f', lonb)
    alt = struct.unpack('H', altb)
    alt = alt[0] / 10
    #state = struct.unpack('B',stateb)
    #error = struct.unpack('B',errb)
    #chk = struct.unpack('B',chkb)

    checksum = 0
    pckt = packet[0:12]
    for byte in pckt:
        checksum = int(byte) ^ checksum

    check = 0
    if (checksum == chk):
        check = 1

    return state, err, lat, lon, alt, check


def WriteData(Command, Data):
    packet = []

    CMD = (struct.pack('H', Command))
    DAT = (struct.pack('H', Data))

    packet = CMD + DAT

    checksum = 0
    for byte in packet:
        checksum = int(byte) ^ checksum

    packet += (struct.pack('B', checksum))

    serialInst.write(packet)

    return packet

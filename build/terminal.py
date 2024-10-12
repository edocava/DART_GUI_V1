import tkinter as tk
import serial
import struct
import GS_Funcs
from GS_Funcs import MB_CMD, MB_STATE, MB_GET_STATUS
import time
import datetime
import serial.tools.list_ports as ports

current_state = None
state = None
err = None
lat = None
lon = None
alt = None
check = None

VERBOSE_ON = 1
RX_CNT = 0

class TerminalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Terminale in Tkinter")

        # Creazione del widget Text
        self.text_widget = tk.Text(root, height=20, width=80, bg="black", fg="green")
        self.text_widget.pack()

        # Binding per il tasto Invio
        self.text_widget.bind("<Return>", self.on_enter)
        self.text_widget.bind("<Up>", lambda event: "break")
        self.text_widget.bind("<Down>", lambda event: "break")

        self.history = list()
        self.history_idx = 0
        self.history_idx_back = 0
        self.text_widget.mark_set("insert", "end")
        self.waiting_for_serial_input = True
        GS_Funcs.init_Serial()
        self.showPorts()
        self.root.resizable(width=False, height=False)

    def showPorts(self):
        self.text_widget.insert(tk.END, "Listing all available ports...\n")
        for [index, port] in enumerate(ports.comports()):
            self.text_widget.insert(tk.END, f"{index} > {str(port).split(' ')[0]}\n")
        self.text_widget.insert(tk.END, "> Select serial port: ")
        self.text_widget.mark_set("insert", "end")

    def on_enter(self, event):
        opt = self.text_widget.get("end-1l linestart", "end-1c").strip()
        if '> ' in opt:
            opt = opt.replace('> ', '')

        if self.waiting_for_serial_input:
            opt = opt.split(' ')[-1]
            print(opt)
            try:
                GS_Funcs.Connect_Serial(str(ports.comports()[int(opt)]).split(' ')[0])
                self.waiting_for_serial_input = False
                self.text_widget.insert(tk.END, "\nSerial port connected\n")
            except ValueError:
                self.text_widget.insert(tk.END, "\nSyntax Error!!")
                self.showPorts()
        else:
            self.text_widget.insert(tk.END, "\n")
            if "set_state" in opt:
                if len(opt.strip().split(' ')) == 1:
                    self.text_widget.insert(tk.END,"Possible states\n")
                    self.text_widget.insert(tk.END,"- sleep\n")
                    self.text_widget.insert(tk.END,"- wake_up\n")
                    self.text_widget.insert(tk.END,"- disarm\n")
                    self.text_widget.insert(tk.END, "- arm\n")
                    self.history.append(opt)
                    self.history_idx += 1
                    self.history_idx_back = self.history_idx
                elif len(opt.strip().split(' ')) == 2:
                    st = opt.strip().split(' ')[1]
                    if st == "sleep":
                        GS_Funcs.WriteData(MB_STATE.MB_SLEEP_REQ, 0)
                        self.read_current_state()
                    elif st == "wake_up":
                        GS_Funcs.WriteData(MB_STATE.MB_WAKEUP_REQ, 0)
                        self.read_current_state()
                    elif st == "disarm":
                        GS_Funcs.WriteData(MB_STATE.MB_DISARM_REQ, 0)
                        self.read_current_state()
                    elif st == "arm":
                        GS_Funcs.WriteData(MB_STATE.MB_ARM_REQ, 0)
                        self.read_current_state()
                    else:
                        self.text_widget.insert(tk.END, "\n")
                        self.text_widget.insert(tk.END, "Invalid state\n")

                    self.history.append(opt)
                    self.history_idx += 1
                    self.history_idx_back = self.history_idx
                else:
                    self.text_widget.insert(tk.END,"Syntax error\n")
            elif "set_reset" == opt:
                self.history.append(opt)
                self.history_idx += 1
                self.history_idx_back = self.history_idx
                GS_Funcs.WriteData(MB_CMD.MB_INIT_CMD_RESET, 0)
                self.text_widget.insert(tk.END,"System resetting...\n")
                self.text_widget.insert(tk.END,"Checking for new status...\n")
                GS_Funcs.set_timeout(GS_Funcs.TIMEOUT_RESET)
                GS_Funcs.WriteData(MB_GET_STATUS, 0)
                self.read_current_state()
                if check != 0:
                    if state == GS_Funcs.MB_FSM.MB_INIT_STATE:
                        self.text_widget.insert(tk.END,"System reset success\n")
                    else:
                        self.text_widget.insert(tk.END,"System reset failed\n")
                else:
                    self.text_widget.insert(tk.END,"General Communication error\n")

                GS_Funcs.set_timeout(GS_Funcs.TIMEOUT_STD)
            elif "get_state" == opt:
                self.history.append(opt)
                self.history_idx += 1
                self.history_idx_back = self.history_idx

                GS_Funcs.WriteData(MB_GET_STATUS, 0)
                self.read_current_state()
            elif "get_errors" == opt:
                self.history.append(opt)
                self.history_idx += 1
                self.history_idx_back = self.history_idx

                GS_Funcs.WriteData(MB_CMD.MB_INIT_CMD_GET_ERRORS, 0)
                self.read_current_state()
            elif "set_verbosity" in opt:
                if len(opt.strip().split(' ')) == 2:
                    if opt.strip().split(' ')[1].lower() == "on":
                        VERBOSE_ON = 1
                        self.history.append(opt)
                        self.history_idx += 1
                        self.history_idx_back = self.history_idx
                    elif opt.strip().split(' ')[1].lower() == "off":
                        VERBOSE_ON = 0
                        self.history.append(opt)
                        self.history_idx += 1
                        self.history_idx_back = self.history_idx
                    else:
                        self.print_help()
                else:
                    self.print_help()
            elif "set_lat" in opt:
                global lat
                lat = int(opt.strip().split(' ')[1])
            elif "set_rx_cont" in opt:
                if len(opt.strip().split(' ')) == 2:
                    if opt.strip().split(' ')[1].lower() == "on":
                        RX_CNT = 1
                        self.history.append(opt)
                        self.history_idx += 1
                        self.history_idx_back = self.history_idx
                    elif opt.strip().split(' ')[1].lower() == "off":
                        RX_CNT = 0
                        self.history.append(opt)
                        self.history_idx += 1
                        self.history_idx_back = self.history_idx
                    else:
                        self.print_help()
                else:
                    self.print_help()
            else:
                self.print_help()

        self.text_widget.bind("<Up>", self.on_up_arrow)
        self.text_widget.bind("<Down>", self.on_down_arrow)

        # self.text_widget.insert(tk.END, output_text)

        self.text_widget.insert(tk.END, "> ")

        self.text_widget.mark_set("insert", "end")
        # Previene un ritorno a capo automatico
        return "break"

    def on_up_arrow(self, event):
        if self.history_idx_back > 0:
            self.history_idx_back -= 1
            self.text_widget.delete("end-1l+2c", "end")
            self.text_widget.insert(tk.END, f"{self.history[self.history_idx_back]}")
        self.text_widget.mark_set("insert", "end")
        return "break"

    def on_down_arrow(self, event):
        if self.history_idx_back < self.history_idx:
            self.history_idx_back += 1
            self.text_widget.delete("end-1l+2c", "end")
            self.text_widget.insert(tk.END, f"{self.history[self.history_idx_back]}")
        self.text_widget.mark_set("insert", "end")
        return "break"

    def print_help(self):
        self.text_widget.insert(tk.END, "\n")
        self.text_widget.insert(tk.END, "Available commands\n")
        self.text_widget.insert(tk.END, "- set_verbosity (on/off)\n")
        self.text_widget.insert(tk.END, "- set_state <state>\n")
        self.text_widget.insert(tk.END, "- set_reset\n")
        self.text_widget.insert(tk.END, "- get_state\n")
        self.text_widget.insert(tk.END, "- get_errors\n")

    def print_err(self):
        global err
        err_list = list()
        for (err_name, err_val) in GS_Funcs.MB_ERROR.items():
            if err & (0b01 << err_val):
                err_list.append(err_name.replace('BITMSK_SHIFT_', ''))
        if len(err_list) == 0:
            self.text_widget.insert(tk.END, "No errors found\n")
        else:
            self.text_widget.insert(tk.END, "Errors:\n", err_list)

    def read_current_state(self):
        global state, err, lat, lon, alt, check
        state, err, lat, lon, alt, check = GS_Funcs.ReadData()
        if check == None:
            self.text_widget.insert(tk.END, "Error while fetching state\n")
            return
        if VERBOSE_ON == 1:
            self.text_widget.insert(tk.END, "BOARD STATUS\n")
            self.text_widget.insert(tk.END, f"{datetime.datetime.now()}\n")
            self.text_widget.insert(tk.END, "-" * 10)
            self.text_widget.insert(tk.END, f"\nState:{GS_Funcs.MB_FSM.to_dict()[state]}\n")
            self.print_err()
            self.text_widget.insert(tk.END, f"Latitude:{lat[0]} deg\n")
            self.text_widget.insert(tk.END, f"Longitude:{lon[0]} deg\n")
            self.text_widget.insert(tk.END, f"Altitude:{alt} m\n")

    def choose_serial(self):
        return GS_Funcs.choose_Serial_term(self.text_widget)

# root = tk.Tk()
# app = TerminalApp(root)
# root.geometry("550x250+300+300")
# root.focus_force()
#
# root.mainloop()



# import serial
# import struct
# import GS_Funcs
# from GS_Funcs import MB_CMD, MB_STATE, MB_GET_STATUS
# import time
# import datetime
#
# TelemOnlyMode = 3
#
# current_state = None
# state = None
# err = None
# lat = None
# lon = None
# alt = None
# check = None
#
# VERBOSE_ON = 1
#
# def print_help():
#     print("Available commands")
#     print("> set_verbosity (on/off)")
#     print("> set_state <state>")
#     print("> set_reset")
#     print("> get_state")
#     print("> get_errors\n")
#
# def print_err():
#     global err
#     err_list = list()
#     for (err_name, err_val) in GS_Funcs.MB_ERROR.items():
#         if err & (0b01 << err_val):
#             err_list.append(err_name.replace('BITMSK_SHIFT_', ''))
#     if len(err_list) == 0:
#         print("No errors found")
#     else:
#         print("Errors:", err_list)
#
#
# def read_current_state():
#     global state, err, lat, lon, alt, check
#     state, err, lat, lon, alt, check = GS_Funcs.ReadData()
#     if check == None:
#         print("Error while fetching state")
#         return
#     if VERBOSE_ON == 1:
#         print("BOARD STATUS")
#         print(datetime.datetime.now())
#         print("-"*10)
#         print(f"State:{GS_Funcs.MB_FSM.to_dict()[state]}")
#         print_err()
#         print(f"Latitude:{lat[0]} deg")
#         print(f"Longitude:{lon[0]} deg")
#         print(f"Altitude:{alt} m")
#
#
# def main():
#     global state, err, lat, lon, alt, check
#     while 1:
#         opt = input("\n> ")
#         if "set_state" in opt:
#             if len(opt.strip().split(' ')) == 1:
#                 print("Possible states")
#                 print("> sleep")
#                 print("> wake_up")
#                 print("> disarm")
#                 print("> arm\n")
#             elif len(opt.strip().split(' ')) == 2:
#                 st = opt.strip().split(' ')[1]
#                 if st == "sleep":
#                     GS_Funcs.WriteData(MB_STATE.MB_SLEEP_REQ, 0)
#                     read_current_state()
#                 elif st == "wake_up":
#                     GS_Funcs.WriteData(MB_STATE.MB_WAKEUP_REQ, 0)
#                     read_current_state()
#                 elif st == "disarm":
#                     GS_Funcs.WriteData(MB_STATE.MB_DISARM_REQ, 0)
#                     read_current_state()
#                 elif st == "arm":
#                     GS_Funcs.WriteData(MB_STATE.MB_ARM_REQ, 0)
#                     read_current_state()
#                 else:
#                     print("Invalid state")
#             else:
#                 print("Syntax error")
#         elif "set_reset" == opt:
#             GS_Funcs.WriteData(MB_CMD.MB_INIT_CMD_RESET, 0)
#             print("System resetting...")
#             print("Checking for new status...")
#             GS_Funcs.set_timeout(GS_Funcs.TIMEOUT_RESET)
#             GS_Funcs.WriteData(MB_GET_STATUS, 0)
#             read_current_state()
#             if check != 0:
#                 if state == GS_Funcs.MB_FSM.MB_INIT_STATE:
#                     print("System reset success")
#                 else:
#                     print("System reset failed")
#             else:
#                 print("General Communication error")
#             GS_Funcs.set_timeout(GS_Funcs.TIMEOUT_STD)
#         elif "get_state" == opt:
#             GS_Funcs.WriteData(MB_GET_STATUS, 0)
#             read_current_state()
#         elif "get_errors" == opt:
#             GS_Funcs.WriteData(MB_CMD.MB_INIT_CMD_GET_ERRORS, 0)
#             read_current_state()
#         elif "set_verbosity" in opt:
#             if len(opt.strip().split(' ')) == 2:
#                if opt.strip().split(' ')[1].lower() == "on":
#                    VERBOSE_ON = 1
#                elif opt.strip().split(' ')[1].lower() == "off":
#                    VERBOSE_ON = 0
#                else:
#                    print_help()
#             else:
#                 print_help()
#         else:
#             print_help()
#
#
# if __name__ == "__main__":
#     GS_Funcs.init_Serial()
#     main()
#

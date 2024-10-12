class Bitmask:
    def __init__(self, imu, mag, gps, alt, pb_init, pb_op, ld_com, ld_sd):
        self.imu = imu
        self.mag = mag
        self.gps = gps
        self.alt = alt
        self.pb_init = pb_init
        self.pb_op = pb_op
        self.ld_com = ld_com
        self.ld_sd = ld_sd

def unpack_bitmask(mask: Bitmask, y_start, canvas):
    imu_color = ""
    mag_color = ""
    gps_color = ""
    alt_color = ""
    pb_init_color = ""
    pb_op_color = ""
    ld_com_color = ""
    ld_sd_color = ""

    y_start_1 = y_start
    y_start_2 = y_start

    if mask.imu == 0:
        imu_color = 'red'
    else:
        imu_color = 'green'

    if mask.gps == 0:
        gps_color = 'red'
    else:
        gps_color = 'green'

    if mask.alt == 0:
        alt_color = 'red'
    else:
        alt_color = 'green'

    if mask.mag == 0:
        mag_color = 'red'
    else:
        mag_color = 'green'

    if mask.pb_init == 0:
        pb_init_color = 'red'
    else:
        pb_init_color = 'green'

    if mask.pb_op == 0:
        pb_op_color = 'red'
    else:
        pb_op_color = 'green'

    if mask.ld_sd == 0:
        ld_sd_color = 'red'
    else:
        ld_sd_color = 'green'

    if mask.ld_com == 0:
        ld_com_color = 'red'
    else:
        ld_com_color = 'green'

    #IMU
    canvas.create_text(
        56.0,  # Posizione orizzontale fissa
        y_start_1,
        anchor="nw",
        text="IMU",
        fill=imu_color,
        font=("Inter", 16)
    )
    y_start_1 += 30

    #MAG
    canvas.create_text(
        56.0,  # Posizione orizzontale fissa
        y_start_1,
        anchor="nw",
        text="MAG",
        fill=mag_color,
        font=("Inter", 16)
    )
    y_start_1 += 30

    #GPS
    canvas.create_text(
        56.0,  # Posizione orizzontale fissa
        y_start_1,
        anchor="nw",
        text="GPS",
        fill=gps_color,
        font=("Inter", 16)
    )
    y_start_1 += 30

    #ALT
    canvas.create_text(
        56.0,  # Posizione orizzontale fissa
        y_start_1,
        anchor="nw",
        text="ALT",
        fill=alt_color,
        font=("Inter", 16)
    )
    y_start_1 += 30

    #PB_INIT
    canvas.create_text(
        200.0,  # Posizione orizzontale fissa
        y_start_2,
        anchor="nw",
        text="PB_INIT",
        fill=pb_init_color,
        font=("Inter", 16)
    )
    y_start_2 += 30

    #PB_OP
    canvas.create_text(
        200.0,  # Posizione orizzontale fissa
        y_start_2,
        anchor="nw",
        text="PB_OP",
        fill=pb_op_color,
        font=("Inter", 16)
    )
    y_start_2 += 30

    #LD_SD
    canvas.create_text(
        200.0,  # Posizione orizzontale fissa
        y_start_2,
        anchor="nw",
        text="LD_SD",
        fill=ld_sd_color,
        font=("Inter", 16)
    )
    y_start_2 += 30

    #LD_COM
    canvas.create_text(
        200.0,  # Posizione orizzontale fissa
        y_start_2,
        anchor="nw",
        text="LD_COM",
        fill=ld_com_color,
        font=("Inter", 16)
    )

    y_start_2 += 30

    return y_start_1

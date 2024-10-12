from GS_Funcs import MB_ERROR

def unpack_error(err, x_start, y_start, canvas):

    color_vec = list()
    name_vec = ['IMU', 'MAG', 'GPS', 'ALT', 'PB_INIT', 'PB_OP', 'LD_COM', 'LD_SD']

    for i in range(8):
        if err & (0b01 << i):
            color_vec.append('red')
        else:
            color_vec.append('green')

    y_start_tmp = y_start

    for i in range(4):
        canvas.create_text(
            x_start,
            y_start_tmp,
            anchor="nw",
            text=name_vec[i],
            fill=color_vec[i],
            font=("Inter", 16)
        )

        canvas.create_text(
            x_start+120.0,
            y_start_tmp,
            anchor="nw",
            text=name_vec[i+4],
            fill=color_vec[i+4],
            font=("Inter", 16)
        )

        y_start_tmp += 30

    return y_start_tmp

from GS_Funcs import MB_ERROR

def unpack_error(err, x_start, y_start, canvas):

    color_vec = list()
    name_vec = ['IMU', 'MAG', 'GPS', 'ALT', 'PB_INIT', 'PB_OP', 'LD_COM', 'LD_SD']

    for i in range(8):
        if err & (0b01 << i):
            color_vec.append('red')
        else:
            color_vec.append('green')

    #TODO: improve this f*****g layout
    for i in range(4):
        canvas.create_text(
            x_start+60*i,
            y_start,
            anchor="nw",
            text=name_vec[i],
            fill=color_vec[i],
            font=("Courier", 18, "bold")
        )

    for i in range(4,8):
        canvas.create_text(
            x_start+80*i-60,
            y_start,
            anchor="nw",
            text=name_vec[i],
            fill=color_vec[i],
            font=("Courier", 18, "bold")
        )



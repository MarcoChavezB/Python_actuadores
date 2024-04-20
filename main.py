from comunicacion import comunicacion

com = comunicacion()
for data in com.read_serial():
    print(data)

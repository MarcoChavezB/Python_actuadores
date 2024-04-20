from comunicacion import comunicacion
#from controlador import Controlador
import RPi.GPIO as GPIO
from time import sleep

com = comunicacion()
#controlador = Controlador()

print("Iniciando")
try:
    while True:
        if(com.get_alarm_value() == 1):
            #controlador.alarma()
            print(com.get_alarm_value(), "Alarma") 
        elif(com.get_luz_value() > 900):
            #controlador.turn_on_lights()
            print(com.get_luz_value(),"Luz")
        elif(com.get_distance_value() < 10):
            #controlador.short_distance()
            print(com.get_distance_value(), "Corto")
        elif(com.get_distance_value() > 11):
            #controlador.long_distance()
            print(com.get_distance_value(),"Largo")
except KeyboardInterrupt:
    pass

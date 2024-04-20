from comunicacion import comunicacion
from controlador import Controlador
import RPi.GPIO as GPIO
from time import sleep

# alarma de precencia

com = comunicacion()
controlador = Controlador()

try:
    while True:
        if(com.get_alarm_value() == 1):
            controlador.alarma()
        elif(com.get_luz_value() > 900):
            controlador.turn_on_lights()
        elif(com.get_distance_value() < 10):
            controlador.short_distance()
        elif(com.get_distance_value() > 11):
            controlador.long_distance()
            
        
except KeyboardInterrupt:
    pass

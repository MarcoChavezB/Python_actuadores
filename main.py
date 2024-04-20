from comunicacion import comunicacion
#from controlador import Controlador
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
buzzer_pin = 40 
led_left = 33
led_right = 37
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(led_left, GPIO.OUT)
GPIO.setup(led_right, GPIO.OUT)


com = comunicacion()
#controlador = Controlador()

print("Iniciando")
try:
    while True:
        if(com.get_alarm_value() == 1):
            #controlador.alarma()
            for _ in range(10):
                GPIO.output(buzzer_pin, GPIO.HIGH)
                GPIO.output(led_left, GPIO.HIGH)
                GPIO.output(led_right, GPIO.HIGH)
                sleep(1)
                GPIO.output(buzzer_pin, GPIO.LOW)
                GPIO.output(led_left, GPIO.LOW)
                GPIO.output(led_right, GPIO.LOW)
                sleep(1)
                
            print(com.get_alarm_value(), "Alarma") 
        elif(com.get_luz_value() > 900):
            #controlador.turn_on_lights()
            GPIO.output(led_left, GPIO.HIGH)
            GPIO.output(led_right, GPIO.HIGH)
            print(com.get_luz_value(),"Luz")
        elif(com.get_luz_value() < 900):
            #controlador.turn_off_lights()
            GPIO.output(led_left, GPIO.LOW)
            GPIO.output(led_right, GPIO.LOW)
            print(com.get_luz_value(),"Oscuro")
    
        elif(com.get_distance_value() < 10):
            #controlador.short_distance()
            print(com.get_distance_value(), "Corto")
        elif(com.get_distance_value() > 11):
            #controlador.long_distance()
            print(com.get_distance_value(),"Largo")
except KeyboardInterrupt:
    pass

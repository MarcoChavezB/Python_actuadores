from comunicacion import comunicacion
import RPi.GPIO as GPIO
from time import sleep
import sys
sys.path.append("/home/server/.local/lib/python3.9/site-packages")
import paho.mqtt.client as mqtt
import ssl
import signal

topic = "triggers/control"

alarm_active = False

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
            for _ in range(2):
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


def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT con resultado: " + str(rc))        
    client.subscribe(topic)
    
def on_message(client, userdata, msg):
    global alarm_active
    if(msg.payload.decode() == "v"):
        alarm_active = True
    elif(msg.payload.decode() == "b"):
        alarm_active = False
        
def cleanup_gpio(signal, frame):
    print("\nLimpiando pines GPIO...")
    GPIO.cleanup()
    sys.exit(0)
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.tls_set(
    ca_certs='/home/server/MQTT_Receptor/AmazonRootCA1.pem',
    certfile='/home/server/MQTT_Receptor/cec69141d6f3a0869a78f2331a3b6acebf6bc9ddb27a738dc3945c2ea4a99618-certificate.pem.crt',
    keyfile='/home/server/MQTT_Receptor/cec69141d6f3a0869a78f2331a3b6acebf6bc9ddb27a738dc3945c2ea4a99618-private.pem.key',
    tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)


"""sleep(15)"""
client.connect("a169mg5ru5h2z1-ats.iot.us-east-2.amazonaws.com", 8883, 60)

signal.signal(signal.SIGINT, cleanup_gpio)

client.loop_forever()
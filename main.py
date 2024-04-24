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
com = comunicacion()

GPIO.setmode(GPIO.BOARD)
buzzer_pin = 40 
led_left = 33
led_right = 37
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(led_left, GPIO.OUT)
GPIO.setup(led_right, GPIO.OUT)

# Definir funciones de callback MQTT
def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT con resultado: " + str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    global alarm_active
    if msg.payload.decode() == "v":
        alarm_active = True
        print("Alarma activada")
    elif msg.payload.decode() == "b":
        alarm_active = False
        print("Alarma desactivada")

# Crear instancia del cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Configurar TLS
client.tls_set(
    ca_certs='/home/server/MQTT_Receptor/AmazonRootCA1.pem',
    certfile='/home/server/MQTT_Receptor/cec69141d6f3a0869a78f2331a3b6acebf6bc9ddb27a738dc3945c2ea4a99618-certificate.pem.crt',
    keyfile='/home/server/MQTT_Receptor/cec69141d6f3a0869a78f2331a3b6acebf6bc9ddb27a738dc3945c2ea4a99618-private.pem.key',
    tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)

# Conectar al broker MQTT
client.connect("a169mg5ru5h2z1-ats.iot.us-east-2.amazonaws.com", 8883, 60)

# Función para limpiar GPIO
def cleanup_gpio(signal, frame):
    print("\nLimpiando pines GPIO...")
    GPIO.cleanup()
    sys.exit(0)

# Configurar señal SIGINT para limpieza de GPIO
signal.signal(signal.SIGINT, cleanup_gpio)

# Esperar a que se establezca la conexión MQTT
client.loop_start()
while not client.is_connected():
    sleep(0.1)

# Después de conectarse, ejecutar el bucle principal
try:
    print("Conexión MQTT establecida. Iniciando bucle principal.")
    while True:
        if com.get_alarm_value() == 1 and alarm_active:
            for _ in range(10):
                if not alarm_active:
                    break
                GPIO.output(buzzer_pin, GPIO.HIGH)
                GPIO.output(led_left, GPIO.HIGH)
                GPIO.output(led_right, GPIO.HIGH)
                sleep(1)
                GPIO.output(buzzer_pin, GPIO.LOW)
                GPIO.output(led_left, GPIO.LOW)
                GPIO.output(led_right, GPIO.LOW)
                sleep(1)
                
        if com.get_inclinacion_value() > 25 or com.get_inclinacion_value() < -35:
            print("Inclinación detectada")
            
        if com.get_distance_value() < 20:
            client.publish(topic, "*")

        if com.get_luz_value() > 800:
            GPIO.output(led_left, GPIO.HIGH)
            GPIO.output(led_right, GPIO.HIGH)


        if com.get_luz_value() < 500:
            GPIO.output(led_left, GPIO.LOW)
            GPIO.output(led_right, GPIO.LOW)
except KeyboardInterrupt:
    pass

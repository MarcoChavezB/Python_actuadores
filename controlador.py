import RPi.GPIO as GPIO
import time

class Controlador:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.buzzer_pin = 40 
        self.led_left = 33
        self.led_right = 37
        GPIO.setup(self.buzzer_pin, GPIO.OUT)
        GPIO.setup(self.led_left, GPIO.OUT)
        GPIO.setup(self.led_right, GPIO.OUT)

    def alarma(self, repetitions=10):
        for _ in range(repetitions):
            GPIO.output(self.buzzer_pin, GPIO.HIGH)
            GPIO.output(self.led_left, GPIO.HIGH)
            GPIO.output(self.led_right, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.buzzer_pin, GPIO.LOW)
            GPIO.output(self.led_left, GPIO.LOW)
            GPIO.output(self.led_right, GPIO.LOW)
            time.sleep(1)
            
    def stopAlarm(self):
        GPIO.output(self.buzzer_pin, GPIO.LOW)
        GPIO.output(self.led_left, GPIO.LOW)
        GPIO.output(self.led_right, GPIO.LOW)
        
    def turn_on_lights(self):
        GPIO.output(self.led_left, GPIO.HIGH)
        GPIO.output(self.led_right, GPIO.HIGH)
        
    def turn_off_lights(self):
        GPIO.output(self.led_left, GPIO.LOW)
        GPIO.output(self.led_right, GPIO.LOW)
        
    def short_distance(self):
        GPIO.output(self.buzzer_pin, GPIO.HIGH)
        
    def long_distance(self):
        GPIO.output(self.buzzer_pin, GPIO.LOW)

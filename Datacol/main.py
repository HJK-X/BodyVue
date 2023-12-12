import os
from time import sleep
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
from RpiMotorLib import rpi_dc_lib
import Encoder
import picamera
from DropboxUtils import dropbox_connect, dropbox_upload_file

def take_picture(filename,camera):
    camera.resolution = (1024, 768)
    camera.capture(filename)

def start_video(filename, camera):
    camera.resolution = (1024, 768)
    camera.start_recording(filename)
def stop_video(camera):
    camera.stop_recording()

LED_PIN = 14
BUTTON_PIN = 23

MOTOR_IN1_PIN = 27
MOTOR_IN2_PIN = 22
MOTOR_PWM_PIN = 17
ENCODER_CHA_PIN = 18
ENCODER_CHB_PIN = 15

GPIO.setup(LED_PIN,GPIO.OUT)
GPIO.setup(BUTTON_PIN,GPIO.IN,pull_up_down=GPIO.PUD_UP)

motor = rpi_dc_lib.L298NMDc(MOTOR_IN1_PIN, MOTOR_IN2_PIN, MOTOR_PWM_PIN)
enc = Encoder.Encoder(ENCODER_CHA_PIN, ENCODER_CHB_PIN)
camera = picamera.PiCamera()
servo = ServoKit(channels=16).servo[0]

angles = [100, 180, 0]
circumference = 3400
interval = circumference/5
encoder_pause = .03
motor_pause = 2

try:

    while True: 
        while True:
            GPIO.output(LED_PIN,GPIO.HIGH)
            button_state = GPIO.input(BUTTON_PIN)
            if button_state == 0:
                break

        print("starting spin")
        GPIO.output(LED_PIN, GPIO.LOW)
        
        start_video("test.h264", camera) #start camera
        for i in angles: #set camera mount angle
            servo.angle = i

            start = enc.read() #obtain feedback for arm positioning
            motor.forward(30) #start motor with positional rotation
            
            while enc.read()-start < circumference:
                print(enc.read()-start)
                if enc.read()-start >= interval:
                    motor.brake()
                    interval += enc.read()-start
                    sleep(motor_pause)
                    motor.forward(30)
                sleep(encoder_pause)
                
            print(enc.read()-start)
            motor.brake()
            print(enc.read()-start)
        
        stop_video(camera)
        servo.angle = None

        dropbox_upload_file(os.getcwd(), "test.h264", "/test.h264")
except Exception as e:
    servo.angle = None
    GPIO.output(LED_PIN,GPIO.LOW)

    

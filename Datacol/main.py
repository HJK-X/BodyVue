from time import sleep
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
from RpiMotorLib import rpi_dc_lib
import Encoder
import picamera

def take_picture(filename,camera):
    camera.resolution = (1024, 768)
    camera.capture(filename)

def start_video(filename, camera):
    camera.resolution = (1024, 768)
    camera.start_recording(filename)
def stop_video(camera):
    camera.stop_recording()

LED_PIN = 3129301293
BUTTON_PIN = 10213

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


angles = [100, 200, 0]

while True: 
    while True: wait
        GPIO.output(LED_PIN,GPIO.HIGH)
        button_state = GPIO.input(BUTTON_PIN)
        print(button_state)
        if button_state == 0:
            break
    GPIO.output(LED_PIN, GPIO.LOW)
    
    for i in range(3):
        servo.angle = angles[i]
        start_video("test.mp4", camera)

        start = enc.read()
        motor.forward(50)
        while enc.read()-old < 5000:
            a = enc.read()-old
            sleep(.01)
            print(a)
            
        print(enc.read()-old)
        motor.brake()
        print(enc.read()-old)
    
    stop_video(camera)

    TOKEN = ''
    Send data to cloud
    Delete data from SSD


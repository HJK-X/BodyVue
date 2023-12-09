from gpiozero import Button # or manually program button 
from time import sleep
import RPi.GPIO as GPIO
import time

LED_PIN = 3129301293
BUTTON_IN_PIN = 10213
BUTTON_OUT_PIN = 10231923

MOTOR_IN1_PIN = 27
MOTOR_IN2_PIN = 22
MOTOR_PWM_PIN = 17
ENCODER_CHA_PIN = 18
ENCODER_CHB_PIN = 15


GPIO.setup(18,GPIO.OUT)
GPIO.output(18,GPIO.HIGH)

button = Button() # did not find documentation for this 
button.wait_for_press() # did not find documentation for this

# While True: 
    # While True: wait
        # if button is pressed: 
            # break
    
    # for i in range(3):
        # camera.start_capture() <- should start capturing camera data and saving it to storage
        # while distance < circumfrance of base:
            # arm.start_rotate()
        # camera.pause()
        # servo.rotate_camera()
        # if i == 2:
            #camera.stop()
        
    # Send data to cloud
    # Delete data from SSD


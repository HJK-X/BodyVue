import picamera, time
from adafruit_servokit import ServoKit
from time import sleep
kit = ServoKit(channels=16)
def take_picture(filename):
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        time.sleep(2)
        print('hello world')
        camera.capture(filename)

def take_video(filename):
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        sleep(1)
        camera.start_recording(filename)
        for i in range(180, 0, -1):
            kit.servo[0].angle = i
            sleep(0.1)

        camera.stop_recording()


take_video('vid.h264')
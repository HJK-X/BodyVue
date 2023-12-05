import picamera, time

def take_picture(filename):
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        time.sleep(2)
        print('hello world')
        camera.capture(filename)

def take_video(filename):
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)

        camera.start_recording(filename)
        # however long
        camera.stop_recording()

take_picture('photo.jpeg')
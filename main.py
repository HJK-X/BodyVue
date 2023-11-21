from gpiozero import Button # or manually program button 
from time import sleep

button = Button() # did not find documentation for this 
button.wait_for_press() # did not find documentation for this

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


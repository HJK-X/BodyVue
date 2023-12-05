from RpiMotorLib import rpi_dc_lib
from time import sleep
import Encoder

motor = rpi_dc_lib.L298NMDc(27, 22, 17)
enc = Encoder.Encoder(18, 15)

old = enc.read()
motor.forward(25)
p = []
    
try:
    while enc.read()-old < 5000:
        a = enc.read()-old
        p.append(a)
        sleep(.01)
        print(a)
        pass

except KeyboardInterrupt: 
    print(p)
print(enc.read()-old)
motor.brake()
print(enc.read()-old)
# sleep(2)
# motor.forward(100)
# sleep(2)
# motor.forward(15)
# sleep(2)
# motor.brake()
# sleep(2)
# motor.backward(50)
# sleep(2)
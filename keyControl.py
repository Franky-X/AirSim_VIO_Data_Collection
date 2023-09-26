import airsim
import numpy as np
import time
#import keyboard  # using module keyboard (install using pip3 install keyboard)
import sys, select, termios, tty
 
vx=0
ang_vy=0

#W forward
#S backward
#D right
#A left
#r brake
#q quit this program


client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)
car_controls = airsim.CarControls()

 
def getKey():
    settings = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key
 
while True:  # making a loop
        key = getKey()
        if key == 'w':  # if key 'q' is pressed 
            car_controls.throttle = car_controls.throttle + 0.1
        elif key == 's':
            car_controls.throttle = car_controls.throttle - 0.1
        else:
            vx = vx
        if key == 'd':  # if key 'q' is pressed 
            car_controls.steering = car_controls.steering + 0.1
        elif key == 'a':
            car_controls.steering = car_controls.steering - 0.1
        elif key == 'r':
            car_controls.brake = 1
        if key == 'q':
            break            
        client.setCarControls(car_controls)
        time.sleep(1.0e-2)

client.reset()
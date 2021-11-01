import os
import platform
# import yaml
# import time
import threading
# import argparse
import pygame

from aws-deepracer-control-v2 import Client
from core.logger import Logger

logger = Logger(logger="Gamepad_mode").getlog()

steer = 0
drive = 0
max_speed = 0.25
done = False
get_os = platform.system()

pygame.init()
joystick_count = pygame.joystick.get_count()
for i in range(joystick_count):
    j = pygame.joystick.Joystick(i)
    j.init()

def event_loop():
    global done, drive, steer, max_speed
    logger.info(u"Running On %s", get_os)
    while not done:
        pygame.init()
        events = pygame.event.get()
        for event in events:
            if get_os == "Windows":
                if event.type == pygame.JOYAXISMOTION and event.axis == 0: #stering_angle
                    if event.value < -1:
                         event.value = -1
                    else:
                        steer = event.value
                        drive = drive
                        max_speed = max_speed

                if event.type == pygame.JOYBUTTONDOWN and event.button == 12: # D1

                    max_speed = 0.25
                    print(max_speed)
                elif event.type == pygame.JOYBUTTONDOWN and event.button == 13: # D2
                    max_speed = 0.3
                    print(max_speed)
                elif event.type == pygame.JOYBUTTONDOWN and event.button == 14: # D3
                    max_speed = 0.45
                    print(max_speed)
                elif event.type == pygame.JOYBUTTONDOWN and event.button == 15: # D4
                    max_speed = 0.60
                    print(max_speed)
                elif event.type == pygame.JOYBUTTONDOWN and event.button == 16: # D5
                    max_speed = 0.75
                    print(max_speed)
                elif event.type == pygame.JOYBUTTONDOWN and event.button == 17: # D6
                    max_speed = 1.0
                    print(max_speed)             
                elif event.type == pygame.JOYAXISMOTION and event.axis == 1 and event.value > -1:#throttle
                    if event.value == 1.0:
                        event.value = 0
                    elif event.value > 0:
                        event.value = -0.1
                    drive = event.value      
                elif event.type == pygame.JOYBUTTONDOWN and event.button == 4: # + button hold it to back 
                    drive *= -1                              
                elif event.type == pygame.JOYBUTTONDOWN and event.button == 5: # - button hold it to back 
                    drive *= -1        
                elif event.type == pygame.JOYAXISMOTION and event.axis == 2: # break to parking
                    drive = 0
                elif event.type == pygame.JOYAXISMOTION and event.axis == 3 and event.value > -1: #clutch to back
                    if event.value == 1.0:
                        event.value = 0
                    elif event.value > 0:
                        event.value = -0.1
                    drive = event.value 
                    drive *= -1 
            elif get_os == "Darwin":
                if event.type == pygame.JOYAXISMOTION and event.axis == 0: #stering_angle
                    if event.value < -1:
                         event.value = -1
                    else:
                        steer = event.value
                        drive = drive
                        max_speed = max_speed
                        
                # print('\t', event.ev_type, event.code, event.state)
                if event.type == pygame.JOYBUTTONDOWN and event.button == 12: # D1
                    
                    max_speed = 0.25
                    print(max_speed)
                elif event.type == pygame.JOYBUTTONDOWN and event.button == 13: # D2
                    max_speed = 0.3
                    print(max_speed)
                elif event.type == pygame.JOYBUTTONDOWN and event.button == 14: # D3
                    max_speed = 0.45
                    print(max_speed)
                elif event.type == pygame.JOYBUTTONDOWN and event.button == 15: # D4
                    max_speed = 0.60
                    print(max_speed)
                elif event.type == pygame.JOYBUTTONDOWN and event.button == 16: # D5
                    max_speed = 0.75
                    print(max_speed)
                elif event.type == pygame.JOYBUTTONDOWN and event.button == 17: # D6
                    max_speed = 1.0
                    print(max_speed)             
                elif event.type == pygame.JOYAXISMOTION and event.axis == 2 and event.value > -1: # throttle to go
                    if event.value == 1.0:
                        event.value = 0
                    elif event.value > 0:
                        event.value = -0.1
                    drive = event.value      
                elif event.type == pygame.JOYBUTTONDOWN and event.button == 4:# + button hold it to back
                    drive *= -1                              
                elif event.type == pygame.JOYBUTTONDOWN and event.button == 5: # - button hold it to back
                    drive *= -1        
                elif event.type == pygame.JOYAXISMOTION and event.axis == 3: # break to parking
                    drive = 0
                elif event.type == pygame.JOYAXISMOTION and event.axis == 1 and event.value > -1: #clutch to back
                    if event.value == 1.0:
                        event.value = 0
                    elif event.value > 0:
                        event.value = -0.1
                    drive = event.value 
                    drive *= -1

    return max_speed


def main():
    #dir_path = os.path.dirname(os.path.realpath(__file__))

    #with open(os.path.join(dir_path, "config.yaml"), "r") as ymlfile:
    #    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    client = Client(password=os.getenv("password"), ip=os.getenv("hostIp"))
    client.set_manual_mode()
    client.start_car()
    t1 = threading.Thread(target=event_loop, name="t1")
    t1.start()
    global done, drive, steer
    while not done:
        client.move(steer, drive, max_speed)
        print(
            "Steering command: "
            + str(steer)
            + " Throttle command: "
            + str(drive)
            + " Max_speed: "
            + str(max_speed)
        )
    client.stop_car()
    t1.join


if __name__ == "__main__":
    main()
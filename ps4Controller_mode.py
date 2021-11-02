import os
import platform
import yaml
import time
import threading
import argparse
import pygame
import logging
import sys

from aws_deepracer_control_v3 import Client
# Used to manage how fast the screen updates.
clock = pygame.time.Clock()

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.getLogger().setLevel(logging.DEBUG)

steer = 0
drive = 0
max_speed = 0.5
done = False

# joystick events updates the global steer, drive, done values
get_os = platform.system()
def process_event(event):
    global done, drive, steer, max_speed
    # quit
    if event.type == pygame.QUIT: # If user clicked close.
        done = True # Flag that we are done so we exit this loop.
    # convert event to steer and drive value
    if get_os == "Linux":
        if event.type == pygame.JOYAXISMOTION and event.axis == 0:  # stering_angle
            if event.value < 0.2 and event.value > -0.2:  # turn right
                steer = 0
            elif event.value < -1:  # turn left
                event.value = -1
            else:
                steer = event.value
        elif event.type == pygame.JOYAXISMOTION and event.axis == 4:  # Throttle
            if event.value < 0.035 and event.value > -0.1:
                drive = 0
            elif event.value < -1:
                event.value = -1
            elif (event.value >= -1 and event.value < -0.1) or (
                event.value <= 1 and event.value > 0.035
            ):
                drive = event.value * -1
        elif event.type == pygame.JOYBUTTONDOWN and event.button == 0:  # parking
            drive = 0
    elif get_os == "Windows":
        if event.type == pygame.JOYAXISMOTION and event.axis == 0:  # stering_angle
            if event.value < 0.2 and event.value > -0.2: # turn right
                steer = 0
            elif event.value < -1 : # turn left
                event.value = -1
            else:
                steer = event.value
        elif event.type == pygame.JOYAXISMOTION and event.axis == 3: # Throttle
            if event.value < 0.035 and event.value > -0.1: 
                drive = 0
            elif event.value < -1 :
                event.value = -1
                # drive = 0
            elif (event.value >= -1 and event.value < -0.1) or (event.value <= 1 and event.value > 0.035):
                drive = event.value * -1
            logging.debug(u"11111 throttle %s %s", event.value, drive)
        elif event.type == pygame.JOYBUTTONDOWN and event.button == 0: # parking
            drive = 0   
    elif get_os == "Darwin":
        if event.type == pygame.JOYAXISMOTION and event.axis == 0:  # stering_angle
            if event.value < 0.2 and event.value > -0.2: # turn right
                steer = 0
            elif event.value < -1 : # turn left
                event.value = -1
            else:
                steer = event.value
        elif event.type == pygame.JOYAXISMOTION and event.axis == 5: # Throttle
            if event.value < 0.035 and event.value > -0.1: 
                drive = 0
            elif event.value < -1 :
                event.value = -1 
            elif (event.value >= -1 and event.value < -0.1) or (event.value <= 1 and event.value > 0.035):
                drive = event.value * -1
        elif event.type == pygame.JOYBUTTONDOWN and event.button == 1: # parking
            drive = 0



def main():

    # client = Client(password=os.getenv("password"), ip=os.getenv("hostIp"))
    client = Client(password="t7Nu2nr3", ip="192.168.1.118")
    logging.info("print vehicle info")
    client.show_vehicle_info()
    car_battery_level = client.get_battery_level()
    logging.info(u"car_battery_level %s", car_battery_level)
    logging.info("set to manual mode.")
    client.set_manual_mode()
    logging.info("start the car")
    client.start_car()
    global done, drive, steer
    
    # start listening to joystick
    pygame.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    try:
        while True:
            events = pygame.event.get()
            for event in events:
                process_event(event)
            logging.debug(u"client.move %s %s %s", steer, drive, max_speed)
            client.move(steer, drive, max_speed)

    except KeyboardInterrupt:
        print("EXITING NOW")
        joystick.quit()
        pygame.quit()
        client.stop_car()

if __name__ == "__main__":
    main()

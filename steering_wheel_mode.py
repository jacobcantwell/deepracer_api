from decouple import config
import platform
import pygame
import logging
import sys

from aws_deepracer_control_v3 import Client
# Used to manage how fast the screen updates.
clock = pygame.time.Clock()
# get operating system
get_os = platform.system()

# configure logging
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.getLogger().setLevel(logging.INFO)

# global variables used for DeepRacer manual driving
steer = 0
drive = 0
max_speed = 1
done = False

pygame.init()
joystick_count = pygame.joystick.get_count()
for i in range(joystick_count):
    j = pygame.joystick.Joystick(i)
    j.init()

# joystick events updates the global steer, drive, done values
# this code depends on the OS, the joystick, and joystick mode
# test the joystick with the ./test/pygame_joystick_full_test.py then update this code
def process_event(event):
    global done, drive, steer, max_speed
    # quit
    if event.type == pygame.QUIT: # If user clicked close.
        drive = 0
        done = True # Flag that we are done so we exit this loop.
    # convert event to steer and drive value
    if event.type == pygame.JOYAXISMOTION and event.axis == 0: #stering_angle
        if event.value < -1:
                event.value = -1
        else:
            steer = event.value
            drive = drive
            max_speed = max_speed
    elif event.type == pygame.JOYAXISMOTION and event.axis == 4: # any break button stop the car
        drive = 0
    elif event.type == pygame.JOYAXISMOTION and event.axis == 5 and event.value > -1: #throttle
        if event.value > -1:
            drive = (event.value + 1)/2
        else:
            drive = 0

def main():
    client = Client(password=config("DEEPRACER_PASSWORD"), ip=config("LOCAL_IP"))
    logging.info("print vehicle info")
    client.show_vehicle_info()
    car_battery_level = client.get_battery_level()
    logging.info(u"car_battery_level %s", car_battery_level)
    logging.info("set to manual mode.")
    client.set_manual_mode()
    # throttle = client.get_calibration_throttle()
    # logging.info(u"throttle %s", throttle)
    logging.info("start the car")
    client.start_car()
    global done, drive, steer, max_speed
    # start listening to joystick
    pygame.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    done = False
    try:
        while not done:
            events = pygame.event.get()
            for event in events:
                process_event(event)
            logging.debug(u"client.move %s %s %s", steer, drive, max_speed)
            client.move(steer, drive, max_speed)
            # Limit to 10 frames per second.
            clock.tick(10)
    except KeyboardInterrupt:
        print("EXITING NOW")
        joystick.quit()
        pygame.quit()
        client.stop_car()

if __name__ == "__main__":
    main()

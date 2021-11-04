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
def process_event(event):
    global done, drive, steer, max_speed
    # quit
    if event.type == pygame.QUIT: # If user clicked close.
        done = True # Flag that we are done so we exit this loop.
    # convert event to steer and drive value
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



def main():

    client = Client(password=config("DEEPRACER_PASSWORD"), ip=config("LOCAL_IP"))
    logging.info("print vehicle info")
    client.show_vehicle_info()
    car_battery_level = client.get_battery_level()
    logging.info(u"car_battery_level %s", car_battery_level)
    logging.info("set to manual mode.")
    client.set_manual_mode()

    throttle = client.get_calibration_throttle()
    logging.info(u"throttle %s", throttle)
    # client.set_calibration_throttle(throttle)

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
            # Limit to 20 frames per second.
            clock.tick(10)
    except KeyboardInterrupt:
        print("EXITING NOW")
        joystick.quit()
        pygame.quit()
        client.stop_car()

if __name__ == "__main__":
    main()

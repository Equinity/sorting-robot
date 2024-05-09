#!/usr/bin/env pybricks-micropython

"""
This program is for the EV3 robot to sort packages by color.
Follow the setup process in menu() 1 - 4 before starting.
"""

import math
import sys
import threading
import time
from pybricks.ev3devices import ColorSensor, Motor, TouchSensor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Button, Color, Direction, Port, Stop
from pybricks.tools import wait

# Define the destinations for picking up and moving the packages.
POSITIONS = []
# POSITIONS = [(0, -26), ('Red', (50, -21)), ('Yellow', (50, -21)),
#              ('Blue', (93, -21)), ('Green', (133, -21))]

SPEED = 1000
TIME = 4000

run = True

COLORS = []
# COLORS = [('Yellow', [(32, 21, 11), (16, 9, 6)]), ('Blue', [(0, 0, 7), (1, 3, 21)]),
#           ('Red', [(28, 4, 13), (15, 2, 0)]), ('Green', [(2, 8, 6), (2, 8, 7)])]

# Initialize the EV3 Brick
ev3 = EV3Brick()

# Configure the gripper motor on Port A with default settings.
gripper_motor = Motor(Port.A)

# Configure the elbow motor.
elbow_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])

# Configure the motor that rotates the base.
base_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])

# Limit the elbow and base accelerations.
elbow_motor.control.limits(SPEED, acceleration=200)
base_motor.control.limits(SPEED, acceleration=200)

# Set up the Touch Sensor.
base_switch = TouchSensor(Port.S1)

# Set up the Color Sensor.
color_sensor = ColorSensor(Port.S2)

# Calibrate all the motors
def initialize_movement():
    """
    This function initializes the motors to their starting positions.
    """
    # Initialize the gripper.
    gripper_motor.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
    gripper_motor.reset_angle(0)
    gripper_motor.run_target(200, -90)

    # Initialize the elbow.
    elbow_motor.run_time(-30, 1000)
    elbow_motor.run(15)
    while color_sensor.reflection() > 0:
        wait(10)
    elbow_motor.reset_angle(0)
    elbow_motor.hold()

    # Initialize the base.
    base_motor.run(-60)
    while not base_switch.pressed():
        wait(10)
    base_motor.run_angle(10,8) # Needed to recenter the base
    base_motor.hold()
    base_motor.reset_angle(0)

    # Play sound to indicate that the initialization is complete.
    ev3.speaker.play_notes(["E4/16"])
    return

def initialize_colors():
    """
    This function initializes the colors that the robot will sort.
    """
    color_complete= []
    color_rgb = []
    available_colors = [["Red",Button.LEFT],["Green", Button.RIGHT],["Blue", Button.UP],
                        ["Yellow", Button.DOWN]] # ändra på vad knapparna ska heta när de printars
    available_colors_buttons = [Button.LEFT, Button.RIGHT, Button.UP, Button.DOWN]

    while len(COLORS) < 4:
        button_pressed = []
        ev3.screen.print("Select a color")
        for i in available_colors:
            ev3.screen.print(i[0],i[1])

        while not any(ev3.buttons.pressed()):
            wait(1)

        # while not any(Button.LEFT, Button.RIGHT, Button.UP, Button.DOWN) in ev3.buttons.pressed():
        #     wait(1)

        # while not any(available_colors_buttons) in ev3.buttons.pressed():
        #     wait(1)

        ev3.screen.clear()
        button_pressed = ev3.buttons.pressed() # måste testas
        # print(button_pressed)
        for i in available_colors:
            # print(i[1])
            if button_pressed[0] == i[1]:
                color_complete.append(i[0])
                # print(color_complete)
                available_colors.remove(i)
                available_colors_buttons.remove(i[1])
        button_pressed = []

        ev3.screen.print("Put a 4x2 brick \nof the selected color \nin the pick-up location")
        ev3.screen.print("Press the middle button when done")
        print("Put a 4x2 brick of the selected color in the pick-up location")
        print("Press the middle button when done")

        while Button.CENTER not in ev3.buttons.pressed():
            wait(1)

        ev3.screen.clear()
        robot_pick(POSITIONS[0])
        color_rgb.append(color_sensor.rgb())
        robot_release(POSITIONS[0])
        ev3.screen.print("Put a 2x2 brick \nof the selected color \nin the pick-up location")
        ev3.screen.print("Press the middle when done")
        print("Put a 2x2 brick of the selected color in the pick-up location")
        print("Press the middle button when done")

        while Button.CENTER not in ev3.buttons.pressed():
            wait(1)

        ev3.screen.clear()
        robot_pick(POSITIONS[0])
        color_rgb.append(color_sensor.rgb())
        robot_release(POSITIONS[0])
        color_complete.append(color_rgb)
        COLORS.append(tuple(color_complete))
        color_complete = []
        color_rgb = []

    print(COLORS) # check
    return

def robot_pick(position):
    """
    This function it lowers the elbow, closes the
    gripper, and raises the elbow to pick up the package.
    """
    base_motor.run_target(SPEED, position[0])
    # Lower the arm.
    elbow_motor.run_target(SPEED, position[1])
    # Close the gripper to grab the package.
    gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=75)
    # Raise the arm to lift the package.
    elbow_motor.run_target(SPEED, 5)

def robot_release(position):
    """ 
    This function lowers the elbow, opens the gripper to
    release the package. Then it raises its arm again.
    """
    base_motor.run_target(SPEED, position[0])
    elbow_motor.run_target(SPEED, position[1])
    # Open the gripper to release the package.
    gripper_motor.run_target(200, -90)
    # Raise the arm.
    elbow_motor.run_target(SPEED, 20)

def color_distance(color1rgb, color2rgb):
    """
    This function calculates the distance between two colors.
    """
    color1rgbp = []
    color2rgbp = []

    for i in color1rgb:
        i = i/100*255 # round()
        color1rgbp.append(i)

    for i in color2rgb:
        i = i/100*255
        color2rgbp.append(i)

    # Extract the RGB values of the two colors.
    r0, g0, b0 = color1rgbp
    r1, g1, b1 = color2rgbp

    # Calculate the Euclidean distance between the two colors.
    distance = math.sqrt((r1 - r0) ** 2 + (g1 - g0) ** 2 + (b1 - b0) ** 2)
    # print(distance) # check
    return distance

def closest_color(color):
    """
    This function finds the closest color to the sensed color.
    """
    closest_color_name = []
    closest_color_distance = 999

    for i in COLORS:
        for j in i[1]:
            if color_distance(color,j) < closest_color_distance:
                closest_color_distance = color_distance(color, j)
                closest_color_name = i[0]

    print(closest_color_name) # Prints the color
    return closest_color_name

def color_sense():
    """
    This function senses the color of the package.
    """
    return closest_color(color_sensor.rgb())

def set_location():
    """
    This function sets the drop-off locations for the robot.
    """
    global POSITIONS
    POSITIONS = POSITIONS[:1]
    print("Please see robot")
    ev3.screen.print("Please calibrate the\ndrop-off locations and\nconfirm with center.")
    while len(POSITIONS) < 5:
        for i in COLORS:
            ev3.screen.clear()
            ev3.screen.print("Position for " + i[0])
            while Button.CENTER not in ev3.buttons.pressed():
                while Button.LEFT in ev3.buttons.pressed():
                    base_motor.run(50)
                while Button.RIGHT in ev3.buttons.pressed():
                    base_motor.run(-50)
                while Button.UP in ev3.buttons.pressed():
                    elbow_motor.run(50)
                while Button.DOWN in ev3.buttons.pressed():
                    elbow_motor.run(-50)

                base_motor.hold()
                elbow_motor.hold()

            while Button.CENTER in ev3.buttons.pressed():
                pass
            POSITIONS.append((i[0],(base_motor.angle(), elbow_motor.angle())))
    ev3.screen.clear()
    elbow_motor.run_target(60, 5)
    return

def set_pickup():
    """
    This function sets the pick-up location for the robot.
    """
    print("Please see robot")
    ev3.screen.print("Please calibrate the\npick-up location and\nconfirm with center.")
    while Button.CENTER not in ev3.buttons.pressed():
        while Button.LEFT in ev3.buttons.pressed():
            base_motor.run(50)
        while Button.RIGHT in ev3.buttons.pressed():
            base_motor.run(-50)
        while Button.UP in ev3.buttons.pressed():
            elbow_motor.run(50)
        while Button.DOWN in ev3.buttons.pressed():
            elbow_motor.run(-50)

        base_motor.hold()
        elbow_motor.hold()

    while Button.CENTER in ev3.buttons.pressed():
        pass
    if len(POSITIONS) == 0:
        POSITIONS.append((base_motor.angle(), elbow_motor.angle()))
    else:
        POSITIONS[0] = (base_motor.angle(), elbow_motor.angle())
    ev3.screen.clear()
    elbow_motor.run_target(60, 5)
    return

def check_location(position):
    """
    This function checks if there is a package at the specified location.
    """
    robot_pick(POSITIONS[position][1])
    if gripper_motor.angle() > -10:
        print("\nNo package present")
        gripper_motor.run_target(200,-80)
    else:
        color_sense()
        robot_release(POSITIONS[position][1])
    return

def sorting():
    """
    This function sorts the packages by color.
    """
    global run
    ev3.screen.clear()
    ev3.screen.print("\nEmergency: Center\nPause: Right")
    threading.Thread(target=emergency).start()
    threading.Thread(target=pause).start()
    if not run:
        return
    while run:
        ev3.light.on(Color.GREEN)
        robot_pick(POSITIONS[0])
        if gripper_motor.angle() < -10: # <>
            color = color_sense()
            for color_name, position in POSITIONS[1:5]:
                if color == color_name:
                    robot_release(position)
        else:
            print("\nNo package present")
            gripper_motor.run_target(200,-80)
            wait(TIME)

def set_timer():
    """
    This function sets the timer/schedule for the robot to run.
    """
    global run
    global timer
    ev3.screen.clear()
    ev3.screen.print("\nPlease see menu\n on computer")
    print("\n------ Set timer ------")
    print("1. Set time to run")
    print("2. Set schedule to run")
    choice = int(input("\nEnter your choice: "))
    time_seconds = round(time.time())
    if choice == 1:
        print("Current time is " + time.strftime("%H:%M:%S", time.localtime()))
        timer = time_seconds + (int(input("Enter time in seconds: ")))
        print("Timer set for ", time.strftime("%H:%M:%S", time.localtime(timer)), " seconds.")
        ev3.screen.clear()

    elif choice == 2:
        print("Current time is " + time.strftime("%H:%M:%S", time.localtime()))
        hours = int(input("Enter to-hour you want the robot to run\n"))
        minutes = int(input("Enter to-minute you want the robot to run\n"))
        seconds = int(input("Enter to-second you want the robot to run\n"))

        # current_day_seconds = int(time.strftime("%H", time.localtime()))*3600 +
        # int(time.strftime("%M", time.localtime()))*60 + int(time.strftime("%S", time.localtime()))

        current_day_seconds = (
            int(time.strftime("%H", time.localtime())) * 3600
            + int(time.strftime("%M", time.localtime())) * 60
            + int(time.strftime("%S", time.localtime()))
        )
        target_time_seconds = hours*3600 + minutes*60 + seconds
        timer = time_seconds +  (target_time_seconds - current_day_seconds)
        print("Timer set for ", hours, " hours, ", minutes, " minutes and ", seconds, " seconds.")
    threading.Thread(target=check_timer).start()
    return

def check_timer():
    """
    This function checks the timer/schedule set by the user.
    """
    global run
    global timer
    # print("CHECK TIMER ", timer)
    while True:
        time_seconds = round(time.time())
        # print(time_seconds - timer)
        while time_seconds == timer:
            run = False
            ev3.screen.clear()
            ev3.screen.print("Time is up!")
            print("Current time is " + time.strftime("%H:%M:%S", time.localtime()))
            print("Time is up!")
            # timer = None
            wait(1500)
            break

def menu():
    """
    This function handles the menu for the user to interact with the robot.
    """
    global run
    ev3.screen.clear()
    ev3.screen.print("Please see menu\n on computer")
    while True:
        print("\n------ MENU ------")
        print("1. Set/change pick-up Location")
        print("2. Calibrate colors")
        print("3. Set/change drop-off Locations")
        print("4. Set runtime")
        print("5. Check Location")
        print("9. Run program")

        choice = input("Enter your choice: ")
        if choice == "1":
            set_pickup()
        elif choice == "2":
            initialize_colors()
        elif choice == "3":
            set_location()
        elif choice == "4":
            set_timer()
        elif choice == "5":
            print("Which position do you want to check?\n")
            position = int(input("Enter position: (1-4)\n"))
            check_location(position)
        elif choice == "9":
            run = True
            break
        else:
            print("Invalid choice. Please try again.")

def emergency():
    """
    This function handles the emergency stop for the robot.
    """
    global run
    global program_running
    while True:
        if Button.CENTER in ev3.buttons.pressed():
            run = False
            program_running = False
            base_motor.hold()
            elbow_motor.hold()
            gripper_motor.hold()
            print("Emergency stop")
            ev3.screen.clear()
            ev3.screen.print("Emergency stop")
            ev3.light.on(Color.RED)
            selection = int(input("1. Reset\n2. Stop program\n"))
            if selection == 1:
                run = True
                program_running = True
                break
            if selection == 2:
                sys.exit()
            else:
                print("Invalid choice. Please try again.")

def pause():
    """
    This function handles the pause for the robot.
    """
    global run
    global not_paused
    while True:
        if Button.RIGHT in ev3.buttons.pressed():
            run = False
            not_paused = False
            base_motor.hold()
            elbow_motor.hold()
            gripper_motor.hold()
            print("Paused")
            ev3.screen.clear()
            ev3.screen.print("Paused")
            ev3.light.on(Color.YELLOW)
            selection = int(input("1. Continue\n2. Stop program\n"))
            if selection == 1:
                run = True
                not_paused = True
                # program_running = True
                break
            if selection == 2:
                sys.exit()
            else:
                print("Invalid choice. Please try again.")

def main():
    """
    This is the main function that runs the program.
    """
    global program_running
    global run
    global not_paused
    # run = True
    not_paused = True
    program_running = True
    while True:
        # program_running = True
        run = True
        # print("MAIN RUNNING")
        while program_running:
            # print("PROGRAM RUNNING")
            initialize_movement()
            menu()
            while not_paused:
                if not_paused and run:
                    # print("SORTING RUNNING")
                    sorting()
                else:
                    wait(1)
            if not program_running:
                break

if __name__ == "__main__":
    main()

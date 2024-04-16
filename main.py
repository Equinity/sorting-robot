#!/usr/bin/env pybricks-micropython

"""
Example LEGO® MINDSTORMS® EV3 Robot Arm Program
-----------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#building-core
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Color, Button
from pybricks.tools import wait
import math # används i color_distance

# Define the destinations for picking up and moving the packages.
#POSITIONS = [0, 45, 90, 145, 190]
POSITIONS = []

run = True

# COLORS = [Color.GREEN, Color.BLUE, Color.RED, Color.YELLOW]
COLORS = []

# Initialize the EV3 Brick
ev3 = EV3Brick()

# Configure the gripper motor on Port A with default settings.
gripper_motor = Motor(Port.A)

# Configure the elbow motor. It has an 8-teeth and a 40-teeth gear
# connected to it. We would like positive speed values to make the
# arm go upward. This corresponds to counterclockwise rotation
# of the motor.
elbow_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])

# Configure the motor that rotates the base. It has a 12-teeth and a
# 36-teeth gear connected to it. We would like positive speed values
# to make the arm go away from the Touch Sensor. This corresponds
# to counterclockwise rotation of the motor.
base_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])

# Limit the elbow and base accelerations. This results in
# very smooth motion. Like an industrial robot.
elbow_motor.control.limits(speed=60, acceleration=120)
base_motor.control.limits(speed=60, acceleration=120)

# Set up the Touch Sensor. It acts as an end-switch in the base
# of the robot arm. It defines the starting point of the base.
base_switch = TouchSensor(Port.S1)

# Set up the Color Sensor. This sensor detects when the elbow
# is in the starting position. This is when the sensor sees the
# white beam up close.
color_sensor = ColorSensor(Port.S2)

# Calibrate all the motors
def initialize_movment():
    # Initialize the gripper. First rotate the motor until it stalls.
    # Stalling means that it cannot move any further. This position
    # corresponds to the closed position. Then rotate the motor
    # by 90 degrees such that the gripper is open.
    gripper_motor.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
    gripper_motor.reset_angle(0)
    gripper_motor.run_target(200, -90)

    # Initialize the elbow. First make it go down for one second.
    # Then make it go upwards slowly (15 degrees per second) until
    # the Color Sensor detects the white beam. Then reset the motor
    # angle to make this the zero point. Finally, hold the motor
    # in place so it does not move.
    elbow_motor.run_time(-30, 1000)
    elbow_motor.run(15)
    while color_sensor.reflection() > 0:
        wait(10)
    elbow_motor.reset_angle(0)
    elbow_motor.hold()

    # Initialize the base. First rotate it until the Touch Sensor
    # in the base is pressed. Reset the motor angle to make this
    # the zero point. Then hold the motor in place so it does not move.
    base_motor.run(-60)
    while not base_switch.pressed():
        wait(10)
    base_motor.run_angle(10,8) # Micro adjustment (needs tweaking for every single robot)
    base_motor.hold()
    base_motor.reset_angle(0)

    # Play sound to indicate that the initialization is complete.
    ev3.speaker.play_notes(["E4/16"])
    return

def initialize_colors():
    color_complete= []
    color_rgb = []
    available_colors = [["red",Button.LEFT],["green", Button.RIGHT],["blue", Button.UP],["yellow", Button.DOWN]] # ändra på vad knapparna ska heta när de printars
    available_colors_buttons = [Button.LEFT, Button.RIGHT, Button.UP, Button.DOWN]

    while len(COLORS) < 4:
        button_pressed = []

        ev3.screen.print("Select a color")
        for i in available_colors:
                ev3.screen.print(i[0],i[1])

        while not any(ev3.buttons.pressed()):
            wait(1)

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


        ev3.screen.print("Put a 4x2 brick of\nthe selected color\nin the pick-up location \nPress the middle\nbutton when done")

        while Button.CENTER not in ev3.buttons.pressed():
            wait(1)

        ev3.screen.clear()
        robot_pick(POSITIONS[0])
        color_rgb.append(color_sensor.rgb())
        robot_release(POSITIONS[0])
        ev3.screen.print("Put a 2x2 brick of the selected color in the pick-up location \nPress the middle when done")

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
    # This function it lowers the elbow, closes the
    # gripper, and raises the elbow to pick up the package.

    base_motor.run_target(60, position[0])
    # Lower the arm.
    elbow_motor.run_target(60, position[1])
    # Close the gripper to grab the package.
    gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=75)
    # Raise the arm to lift the package.
    elbow_motor.run_target(60, 5)

def robot_release(position):
    # This function lowers the elbow, opens the gripper to
    # release the package. Then it raises its arm again.

    base_motor.run_target(60, position[0])
    # Lower the arm to put the package on the ground.
    elbow_motor.run_target(60, position[1])
    # Open the gripper to release the package.
    gripper_motor.run_target(200, -90)
    # Raise the arm.
    elbow_motor.run_target(60, 20)

def color_distance(color1rgb, color2rgb):
    color1rgbp = []
    color2rgbp = []

    for i in color1rgb:
        i = i/100*255 # round()
        color1rgbp.append(i)

    for i in color2rgb:
        i = i/100*255
        color2rgbp.append(i)

    # Extrahera RGB-komponenterna för varje färg
    r0, g0, b0 = color1rgbp
    r1, g1, b1 = color2rgbp

    # Beräkna avståndet mellan färgerna
    distance = math.sqrt((r1 - r0) ** 2 + (g1 - g0) ** 2 + (b1 - b0) ** 2)

    # print(distance) # check

    return distance

def closest_color(color):
    closest_color_name = []
    closest_color_distance = 999

    for i in COLORS:
        for j in i[1]:
            if color_distance(color,j) < closest_color_distance:
                closest_color_distance = color_distance(color, j)
                closest_color_name = i[0]

    print(closest_color_name) # check

    return closest_color_name

def color_sense():
    return closest_color(color_sensor.rgb())

def set_location():
    global POSITIONS
    POSITIONS = POSITIONS[:1]
    ev3.screen.print("Please calibrate the\ndrop-off locations and\nconfirm with center.")
    while len(POSITIONS) < 5:
        for i in COLORS:
            for j in i[0]:
                ev3.screen.print("Please set color\n" + j)
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
        POSITIONS.append((base_motor.angle(), elbow_motor.angle()))
    ev3.screen.clear()
    elbow_motor.run_target(60, 5)
    return

def set_pickup():
    ev3.screen.print("Please calibrate the\npick-up location and\nconfirm with center.")
    while len(POSITIONS) < 1:
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
        POSITIONS[0] = ((base_motor.angle(), elbow_motor.angle()))
    ev3.screen.clear()
    elbow_motor.run_target(60, 5)
    return

def check_location(position):
    robot_pick(position)
    color = color_sense()
    if color == "None":
        ev3.speaker.say("No package")
    else:
        ev3.speaker.say("Package, color:" + str(color))

def sorting():
    ev3.screen.print("HOLD CENTER\nBUTTON FOR\nSAFE STOP")
    run = True
    while True:
        # while Button.CENTER not in ev3.buttons.pressed() and run == True:
        while run == True:
            robot_pick(POSITIONS[0])
            color_sense()
            robot_release(POSITIONS[1])

            if Button.CENTER in ev3.buttons.pressed():
                run = False
                ev3.screen.clear()
                ev3.screen.print("SAFE STOP\n\nPress Left to\nenter menu")
                wait(2000)
        if Button.LEFT in ev3.buttons.pressed():
            ev3.screen.clear()
            # menu()
            return

def menu():
    ev3.screen.print("MENU\nLeft: Location set\nRight: Schedule\nDown: Return")
    wait(1000)
    time = 5000
    while True:
        if Button.LEFT in ev3.buttons.pressed():
            wait(300)
            ev3.screen.clear()
            set_location()
            return
        if Button.RIGHT in ev3.buttons.pressed():
            ev3.screen.clear()
            ev3.screen.print("The schedule is\n", time/1000, "seconds\nPress up or down\nto change\nOK with Center")
            while Button.CENTER not in ev3.buttons.pressed():
                while Button.UP in ev3.buttons.pressed():
                    time = time + 500
                    wait(500)
                    ev3.screen.clear()
                    ev3.screen.print("Schedule is now\n", time/1000, "seconds")
                while Button.DOWN in ev3.buttons.pressed():
                    time = time - 500
                    wait(500)
                    ev3.screen.clear()
                    ev3.screen.print("Schedule is now\n", time/1000, "seconds")
            ev3.screen.clear()
            return time
        if Button.DOWN in ev3.buttons.pressed():
            return

def main():
    initialize_movment()
    set_pickup()
    initialize_colors((base_motor,elbow_motor))
    set_location()
    # base_motor,elbow_motor=initialize_movment()
    # initialize_colors((base_motor,elbow_motor))
    menu()
    # wait(1500)
    sorting()

if __name__ == "__main__":
    main()
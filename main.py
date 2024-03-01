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

# Define the destinations for picking up and moving the packages.
POSITIONS = [0, 45, 90, 145, 190]

color_list = []

COLORS = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW]

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
def initialize():
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
    base_motor.reset_angle(0)
    base_motor.hold()

    # Initialize the gripper. First rotate the motor until it stalls.
    # Stalling means that it cannot move any further. This position
    # corresponds to the closed position. Then rotate the motor
    # by 90 degrees such that the gripper is open.
    gripper_motor.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
    gripper_motor.reset_angle(0)
    gripper_motor.run_target(200, -90)

    # Play sound to indicate that the initialization is complete.
    ev3.speaker.play_notes(["E4/16"])

def robot_pick():
    # This function it lowers the elbow, closes the
    # gripper, and raises the elbow to pick up the package.

    # Lower the arm.
    elbow_motor.run_target(60, -40)
    # Close the gripper to grab the package.
    gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=75)
    # Raise the arm to lift the package.
    elbow_motor.run_target(60, -10)

#TODO: Add functionality for movement based on color
def robot_move(position):
    # Rotate to the pick-up position.
    base_motor.run_target(60, position)

def robot_release():
    # This function lowers the elbow, opens the gripper to
    # release the package. Then it raises its arm again.

    # Lower the arm to put the package on the ground.
    elbow_motor.run_target(60, -40)
    # Open the gripper to release the package.
    gripper_motor.run_target(200, -90)
    # Raise the arm.
    elbow_motor.run_target(60, 0)


def color_sense():
    # function for identifying color of package
    wait(300)
    color_sensed = color_sensor.rgb()
    print(color_sensed)
    while len(color_list) < 3   :
        if color_sensed in color_list:
            return
        else:
            color_list.append(color_sensed)
    # blue = (1, 3, 23)
    print(color_list)
    # ev3.light.on(color_sensed)
    return color_sensed

def set_location():
    while Button.LEFT in ev3.buttons.pressed():
        base_motor.run(50)
    while Button.RIGHT in ev3.buttons.pressed():
        base_motor.run(-50)
    while Button.UP in ev3.buttons.pressed():
        elbow_motor.run(50)
    while Button.DOWN in ev3.buttons.pressed():
        elbow_motor.run(-50)
    while Button.CENTER in ev3.buttons.pressed():
        base_motor.hold()
        elbow_motor.hold()
        return True

# This is the main part of the program. It is a loop that repeats endlessly.
#
# First, the robot moves the object on the left towards the middle.
# Second, the robot moves the object on the right towards the left.
# Finally, the robot moves the object that is now in the middle, to the right.
#
# Now we have a wheel stack on the left and on the right as before, but they
# have switched places. Then the loop repeats to do this over and over.
initialize()
# base_motor.run_angle(10,12)
# base_motor.reset_angle(0)
# drop_off_color = {
#     "LEFT" : "0", "MIDDLE" : "1" , "RIGHT" : "2"
# }
def main():
    base_motor.run_angle(10,11)
    base_motor.reset_angle(0)

    # if Button.CENTER in ev3.buttons():
    #     run = False
    #     # POSITIONS = set_location()

    run = set_location()

    while run == True:

        robot_move(POSITIONS[0])
        robot_pick()
        color = color_sense()
        if color == COLORS[0]:
            robot_move(POSITIONS[4])
            robot_release()

        elif color == COLORS[1]:
            robot_move(POSITIONS[3])
            robot_release()

        elif color == COLORS[2]:
            robot_move(POSITIONS[2])
            robot_release()

        else:
            robot_move(POSITIONS[1])
            robot_release()

        robot_move(POSITIONS[2])
        wait(3000)
        # color_1 = color_sense()
        # drop_off_color.uptade({"LEFT" : color_1})

if __name__ == "__main__":
    main()
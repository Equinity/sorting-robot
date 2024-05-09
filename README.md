# PA1473 - Software Development: Agile Project

## Template information
This template should help your team write a good readme-file for your project. (The file is called README.md in your project directory.)
You are of course free to add more sections to your readme if you want to.

Readme-files on GitHub are formatted using Markdown. You can find information about how to format using Markdown here: https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax

Your readme-file should include the following sections:


# Introduction

This is a repository for a LEGO Mindstorms EV3 robot with code for automatically sorting different coloured packages. 
This README will guide you to the funcitionalities of the code and how to set up the robot.

# Getting started

To get started with this project, follow these steps:

1. Clone the repository to your local machine.
2. Install the necessary dependencies by running the command:

```
pip install pybricksdev
```

3. Connect the LEGO Mindstorms EV3 robot to your computer.
4. Open the project in your preferred code editor.
5. Follow the on-screen instructions to operate the robot and start the sorting process.


# Building and running

This section will guide you to managing running the program.
For more information on how to connect to the EV3 brick, please see [further documentation](https://pybricks.com/ev3-micropython/startrun.html)

## Initializing the robot

When the program is first run, the robot needs to be configured, by following the menu, this process is quite straight-forward. 
Begin with setting the pick-up location by entering 1 in the menu and calibrating the pick-up location with the buttons on the robot, confirming with the center button.

Then, you calibrate the colors by entering 2 in the menu and following the on-screen instructions.
**Please note that both sizes of the packages are required for this process.**

After the colors have been calibrated, you specify the locations for drop-off for each color. This is also done by using the buttons on the robot and following the on-screen instructions.

Finally, before the sorting can commence, the robot requires a time to run. This is set by entering 4 in the menu and following the on-screen instructions. The robot can either run for a set amount of time specified in seconds, or run to a select time based on the current time.

In the menu you can also choose to check a specific location if a package is present. This is done by entering 5 in the menu, followed by the position 1-4.

## Robot sorting process

When the program has been initialized, the program will continuously run the sorting process until the timer has run out, or the robot is paused or emergency stopped. 

If a new package has arrived, the robot will sense the color and move it to the previously configured position. The robot will regularly check the pick-up location for any new packages based on the TIME variable set in the program. The default TIME is 4 seconds. 


## Features

- [x] [US01B: As a customer, I want the robot to pick up items from a designated position.](https://github.com/users/Equinity/projects/1?pane=issue&itemId=60045277)
- [x] [US02B: As a customer, I want the robot to drop off items at a designated position.](https://github.com/Equinity/sorting-robot/issues/38)
- [x] [#39](https://github.com/users/Equinity/projects/1/views/1?pane=issue&itemId=60045869)
- [x] US04B: As a customer, I want the robot to tell me the colour of an item at a designated position.
- [x] US05: As a customer, I want the robot to drop items off at different locations based on the colour of the item.
- [x] US06: As a customer, I want the robot to be able to pick up items from elevated positions.
- [x] US08: As a customer, I want to be able to calibrate maximum of three different colours and assign them to specific drop-off zones.
- [x] US09: As a customer, I want the robot to check the pickup location periodically to see if a new item as arrived.
- [x] US10: As a customer, I want the robot to sort items at a specific time.   --
- [ ] US11: As a customer, other. I want two robots (from two teams) communicate and work together on items sorting without colliding with each
- [x] US12: As a customer, I want to be able to manually set the locations and heights of one pick-up zone and two drop-off zones. (Implemented either by manually dragging the arm to a position or using buttons) 
- [x] US13: As a customer, I want to easily reprogram the pickup and drop of zone of the robot.
- [x] US14: As a customer, I want to easily change the schedule of the robot pick up task.
- [ ] US15: As a customer, I want to have an emergency stop button, that immediately terminates the operation of the robot safely.
- [x] US16: As a customer, I want the robot to be able to pick an item up and put it in the designated drop-off location within 5 seconds.
- [ ] US17: I want the robot to pick up items form a rolling belt and put them in the designated positions based on color and shape.
- [o] US18: I want to have a pause button that pauses the robot´s operation when the button is pushed and then resumes the program from the same point when I push the button again.
- [x] US19: I want a very nice dashboard to configure the robot program and start some tasks on demand.







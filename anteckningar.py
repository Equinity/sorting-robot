from pybricks.hubs import EV3Brick as ev3
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction
from pybricks.tools import wait

# buttons()
# Check which buttons on the EV3 Brick are currently pressed.
# Returns List of pressed buttons.
# Return type List of Button

# classmethod sound.beep(frequency=500, duration=100, volume=30)
# ljud/sound

# classmethod sound.beeps(number)
# Play a number of default beeps with a brief pause in between.

# classmethod sound.file(file_name, volume=100)
    # file_name (str) – Path to the sound file, including extension.
    # volume (percentage: %) – Volume of the sound (Default: 100)

import threading as th

keep_going = True
def key_capture_thread():
    global keep_going
    input()
    keep_going = False

def do_stuff():
    th.Thread(target=key_capture_thread, args=(), name='key_capture_thread', daemon=True).start()
    while keep_going:
        print('still going...')

do_stuff()
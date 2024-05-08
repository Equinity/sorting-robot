from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Color, Button
from pybricks.tools import wait
import math
import threading
from threading import Thread

'''kladd för color_sense.rgb()'''

# def rgbp_to_hex(rgbp):
#     rgb = []
#     for i in rgbp:
#         i = round(i/100*255)
#         rgb.append(i)
#     tuple(rgb)
#     return '#%02x%02x%02x' % rgb


# test1 = (12, 12, 12)
# rgb = []
# for i in test1:
#     i = round(i/100*255)
#     rgb.append(i)
#     print(rgb)
#     if len(rgb) == 3:
#         print(rgb)
#         rgb = tuple(rgb)
#         print(rgb_to_hex(rgb))


'''multitasking'''
# import threading as th

# keep_going = True
# def key_capture_thread():
#     global keep_going
#     input()
#     keep_going = False

# def do_stuff():
#     th.Thread(target=key_capture_thread, args=(), name='key_capture_thread', daemon=True).start()
#     while keep_going:
#         print('still going...')

# do_stuff()

'''Color distance rgb'''
# import math

# def color_distance(color1, color2):
#     # Extrahera RGB-komponenterna för varje färg
#     r0, g0, b0 = color1
#     r1, g1, b1 = color2

#     # Beräkna avståndet mellan färgerna
#     distance = math.sqrt((r1 - r0) ** 2 + (g1 - g0) ** 2 + (b1 - b0) ** 2)

#     return distance

# # Exempel på användning:
# color1 = (255, 0, 0)  # Röd färg
# color2 = (0, 255, 0)  # Grön färg

# distance = color_distance(color1, color2)
# print("Avståndet mellan färgerna är:", distance)

# available_colors = [["red",Button.LEFT],["green", Button.RIGHT],["blue", Button.UP],["yellow", Button.DOWN]] # ändra på vad knapparna ska heta när de printars

# new_list = [i for i in available_colors.pop(i)]
# print(new_list)

# list = [('red', [(45, 6, 23), (10, 1, 3)]), ('yellow', [(68, 49, 30), (12, 9, 1)]), ('blue', [(5, 14, 74), (0, 2, 13)]), ('green', [(8, 35, 37), (2, 10, 8)])]
timer = threading.Timer(2.0, print, args=["Hello, World!"])
timer.start()

while timer.is_alive():
    print("Printing...")

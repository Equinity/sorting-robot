'''kladd för color_sense.rgb()'''

# def rgb_to_hex(rgb):
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
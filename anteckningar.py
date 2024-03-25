# kladd för color_sense.rgb()

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

def hex_to_int(s):
    return [int(s[i:i+2], 16) for i in range(1,7,2)]

print(hex_to_int((12,12,12)))






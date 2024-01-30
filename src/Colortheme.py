from tueplots.constants.color import rgb
from tueplots.constants.color import palettes
import numpy as np


def turn_to_np_rgb(hex_color, coloration=1):
    return (np.array( list(bytes.fromhex(hex_color)) )/ 255.0)*coloration

# #f7f7f7, #d9d9d9, #bdbdbd, #969696, #636363, #252525
NEUTRAL_COLORS = [
    rgb.tue_dark,
    turn_to_np_rgb("bdbdbd"),
    turn_to_np_rgb("969696"),
    turn_to_np_rgb("636363"),
    turn_to_np_rgb("252525"),
]

COUNTER_COLORS = [
    turn_to_np_rgb("E84A4A"), #E84A4A
    turn_to_np_rgb("4786DE"), #4786DE
    turn_to_np_rgb("EB9E46"), #EB9E46
    turn_to_np_rgb("5D3E94")  #5D3E94
]

PRIMARY_COLORS = [
    turn_to_np_rgb("253494"), #253494,
    turn_to_np_rgb("EC6634"), #EC6634
    turn_to_np_rgb("33b983"), #33b983
    turn_to_np_rgb("BB5566"), #BB5566
]


MARKER_COLORS = [
    turn_to_np_rgb("7018d3"), #7018d3
    turn_to_np_rgb("BD22AB"), #BD22AB
    turn_to_np_rgb("424470"), #424470
    turn_to_np_rgb("22826A")  #22826A
]

AREA_COLORS = [
    turn_to_np_rgb("6C76BB"), #6C76BB
    turn_to_np_rgb("f8b8d0"), #f8b8d0
    turn_to_np_rgb("7fcdbb"), #7fcdbb
]

TEMP_COLOR = turn_to_np_rgb("f98517") #f98517
RAIN_COLOR = turn_to_np_rgb("1077f3") #1077f3
SUMMER_COLOR = turn_to_np_rgb("FF4B04") #FF4B04
WINTER_COLOR = turn_to_np_rgb("57CDDC") #57CDDC

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
    # rgb.tue_red,
    # rgb.tue_orange,
    turn_to_np_rgb("E84A4A"), #E84A4A
    turn_to_np_rgb("4786DE"), #4786DE
    turn_to_np_rgb("EB9E46"), #EB9E46
    # turn_to_np_rgb("324C82"), #324C82 #B31E35
    # turn_to_np_rgb("B82828"), #B82828
    # turn_to_np_rgb("B85911"), #B85911
    turn_to_np_rgb("5D3E94")  #5D3E94
]

PRIMARY_COLORS = [
    turn_to_np_rgb("253494"), #253494,
    turn_to_np_rgb("EC6634"), #EC6634
    turn_to_np_rgb("33b983"), #33b983
    turn_to_np_rgb("BB5566"), #BB5566
]


MARKER_COLORS = [
    # rgb.tue_red,
    turn_to_np_rgb("7018d3"), #7018d3
    turn_to_np_rgb("BD22AB"), #BD22AB
    turn_to_np_rgb("424470"), #424470
    turn_to_np_rgb("22826A")  #22826A
    # turn_to_np_rgb("1077f3"), #1077f3
    # turn_to_np_rgb("41b6c4"), #41b6c4
    # turn_to_np_rgb("c7e9b4"), #c7e9b4
    # turn_to_np_rgb("e7a962"), #e7a962
    # turn_to_np_rgb("66CCEE"), #66CCEE
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

# DEPRECATED
# PRIMARY_COLORS = [
#     turn_to_np_rgb("004488"),
#     turn_to_np_rgb("BB5566"),
#     turn_to_np_rgb(rgb.tue_ocre)
# ]
# # "#004488", "#DDAA33", "#BB5566"
# # "#4477AA","#EE6677","#228833","#CCBB44","#66CCEE","#AA3377",
# # "#CC6677", "#332288", "#DDCC77", "#117733", "#88CCEE", "#882255", # "#44AA99", "#999933", "#AA4499"
# SECONDARY_COLORS = [
#     turn_to_np_rgb(c)
#     for c in palettes.bright
# ]
# SECONDARY_COLORS = [
#     turn_to_np_rgb(c)
#     for c in palettes.muted
# ]

# Steinlachallee 	BLAU
# Fahrradtunnel  	ROT (NICHT KNALLROT)
# Combi		VIOLET

# Hirschau	ORANGE / OCKER

# Temp 		HELLORANGE
# Regen		GRAUBLAU


# Summer		CORAL
# Winter		HELLBLAU
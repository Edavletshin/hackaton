import json
import os
import cv2
import numpy as np
import math
from math import sqrt, acos, degrees

cap = cv2.VideoCapture('false_sit.mov')
success, image = cap.read()
count = 0
i = 0
while success:
    cv2.imwrite("frame%d.jpg" % count, image)  # save frame as JPEG file
    if cv2.waitKey(10) == 27:  # exit if Escape is hit
        break
    count += 1
    while i < 7:
        success, image = cap.read()
        i += 1
    i = 0


 # def checkKnee(leg):
 #     i = 0

#
# def checkSitDeep(leg) :

def checkBodyDegree(leg):
    def scalar(x1, y1, x2, y2):
        return x1 * x2 + y1 * y2

    def module(x, y):
        return sqrt(x ** 2 + y ** 2)

    ax = (leg['Knee']['x']) - (leg['Butt']['x'])
    bx = (leg['Shoulder']['x']) - (leg['Butt']['x'])
    ay = (leg['Knee']['y']) - (leg['Butt']['y'])
    by = (leg['Shoulder']['y']) - (leg['Butt']['y'])
    cos = scalar(ax, ay, bx, by) / (module(ax, ay) * module(bx, by))
    ang = acos(cos)
    ang = round(math.degrees(ang), 2)

    print("Body", ang)

def checkLegsDegree(leg):
    def scalar(x1, y1, x2, y2):
        return x1 * x2 + y1 * y2

    def module(x, y):
        return sqrt(x ** 2 + y ** 2)
    ax = (leg['Foot']['x']) - (leg['Knee']['x'])
    bx = (leg['Butt']['x']) - (leg['Knee']['x'])
    ay = (leg['Foot']['y']) - (leg['Knee']['y'])
    by = (leg['Butt']['y']) - (leg['Knee']['y'])
    cos = scalar(ax, ay, bx, by) / (module(ax, ay) * module(bx, by))
    ang = acos(cos)
    ang = round(math.degrees(ang), 2)

    print("Legs", ang)


# print(degrees(acos(cos)))
def checkSit(flat):
    def RightCoord (flat_r) :
        coord = {'Butt': {'x': flat_r[16], 'y': flat_r[17]},
               'Knee': {'x': flat_r[18], 'y': flat_r[19]},
               'Foot': {'x': flat_r[20], 'y': flat_r[21]},
               'Shoulder': {'x' :flat_r[2], 'y' : flat_r[3]}}
        return coord
    def LeftCoord (flat_l) :
        coord = {'Butt': {'x': flat_l[22], 'y': flat_l[23]},
               'Knee': {'x': flat_l[24], 'y': flat_l[25]},
               'Foot': {'x': flat_l[26], 'y': flat_l[27]},
               'Shoulder': {'x' :flat_l[2], 'y' : flat_l[3]}}
        return coord
    if(flat[20] == 0 or flat[32] == 0) :
        print("left site")
        coord = LeftCoord(flat)
    elif (flat[26] == 0 or flat[34] == 0):
        print("right site")
        coord = RightCoord(flat)
    else :
        print("razvernis!!!")
    checkBodyDegree(coord)
    checkLegsDegree(coord)
    # checkSitDeep(leg)
    # checkKnee()
    #
    # if(yButt <= yKnee) :
    #         return bool(1)
    return bool(1)


with open(os.path.join('/Users/mariaugorets/Downloads/', '{0}_keypoints.json'.format(str(0).zfill(12))), 'r') as outfile:
    flat = json.load(outfile)

if checkSit(flat):
    print("nice sit")
else:
    print("prisjad' rovno bljat'")

# flat = [628, 380, #0
#         622, 616, #1
#         417, 559,#2
#         0.0, 0.0, #3
#         0.0, 0.0, #4
#         922, 616, #5 -10 11
#         1000, 814, #6
#         0.0, 0.0, #7
#         0.0, 0.0, #8
#         0.0, 0.0, #9
#         0.0, 0.0, #10 -20 21
#         0.0, 0.0, #11
#         0.0, 0.0, #12
#         0.0, 0.0, #13
#         578, 347, #14
#         672, 337, #15 -30 31
#         511, 385, #16
#         750, 380] #17

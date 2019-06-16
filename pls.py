import json
import os
import cv2
import numpy as np
import math
import subprocess
import operator
from math import sqrt, acos, degrees


# Starting parcing video to frames and gett coordinates from all frames
def startParcer() :
    frames = {}
    cap = cv2.VideoCapture('/Users/reilganpi/42/hakaton/tf-pose-estimation/kekanndos/false_2_toomuch.mov')
    success, image = cap.read()
    count = 0
    i = 0
    while success:
        cv2.imwrite("frame%d.jpg" % count, image)   # save frame as JPEG file
        while i < 10:
            success, image = cap.read()
            i += 1
        proc = subprocess.Popen("python3 /Users/reilganpi/42/hakaton/tf-pose-estimation/run.py --model=mobilenet_thin --output_json=/Users/reilganpi/42/hakaton/tf-pose-estimation/kekanndos/json/ --resize=432x368 --image=/Users/reilganpi/42/hakaton/tf-pose-estimation/frame%d.jpg" % count, shell=True, stdout=subprocess.PIPE)
        out = proc.stdout.readlines()
        with open(os.path.join('/Users/reilganpi/42/hakaton/tf-pose-estimation/kekanndos/json/', '{0}_keypoints.json'.format(str(0).zfill(12))), 'r') as outfile:
            flat = json.load(outfile)
        i = 0
        frames[count] = flat
        count += 1
    return frames, count

def checkKnee(leg):
    a = (leg['Knee']['x'] * 100 / leg['Foot']['x'])
    if a > 70 and a < 100:
        return 1
    else :
        print("Your knees too far")
        return 0

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
    if ang > 40 :
        return 1
    else :
        print("You leaned too hard")
        return 0

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

    if ang > 65  and ang < 115 :
        return 1
    else :
        print("You sat down too hard or not hard enough")
        return 0


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
    if ((flat[20] == 0 or flat[32] == 0) and (flat[2] != '0.0' and (flat[22] != '0.0' and flat[24] != '0.0' and flat[26] != '0.0')) and flat[0] < flat[22]) :
        coord = LeftCoord(flat)
    elif ((flat[26] == 0 or flat[34] == 0) and (flat[2] != '0.0' and (flat[16] != '0.0' and flat[18] != '0.0' and flat[20] != '0.0')) and flat[0] > flat[16]) :
        coord = RightCoord(flat)
    else :
        print("File is not valid, please get new video")
        return 0
    if checkBodyDegree(coord) == 1 and checkLegsDegree(coord) == 1 and checkKnee(coord) == 1:
        return 1
    else :
        return 0


frames , count = startParcer()
neck = {}
i = 0
for i in range(count):
    coord = frames[i][3]
    neck[i] = coord
sorted_n = sorted(neck.items(), key = operator.itemgetter(1), reverse = 1)
if checkSit(frames[sorted_n[0][0]]) :
    print("Success squat")
else :
    print("Try again")

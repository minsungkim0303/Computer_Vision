# -*- coding: utf-8 -*-
##############################################################################################
#     Copyrights all rights reserved.
#
# 이미지를 읽어 들이고 6개의 구멍을 구분하고
# 정상, 불량을 구분하여 따로 저장 
# 정상, 불량 구분 기준은 파일명 뒤에 있는 불량 구멍 번호 기준 
##############################################################################################

# import the necessary packages
import numpy as np
import argparse
import cv2
import os


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if os.path.isdir(path):
            pass
        else:
            raise


def detect_segment(img):
    # img gray 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = gray[0:340, 0:640]
    row = gray[90:100, 0:640]

    # 바 추출
    seg = 1
    start = []
    end = []
    onSegment = False
    for x in range(0, 639):
        if row[0, x] > 200:
            if onSegment:
                if row[0, x + 1] < 200:
                    onSegment = False
                    end.append(x)
                continue
            else:
                start.append(x)
                onSegment = True

    startArr = np.asarray(start)
    endArr = np.asarray(end)

    if len(startArr) != len(endArr):
        raise
    if len(startArr) != 3:
        raise

    bar1 = img[50:290, start[0]:end[0]]
    bar2 = img[50:290, start[1]:end[1]]
    bar3 = img[50:290, start[2]:end[2]]

    # 구멍 추출
    hole1 = bar1[0:120, 0:100]
    hole2 = bar2[0:120, 0:100]
    hole3 = bar3[0:120, 0:100]
    hole4 = cv2.flip(bar1[120:240, 0:100], 0)
    hole5 = cv2.flip(bar2[120:240, 0:100], 0)
    hole6 = cv2.flip(bar3[120:240, 0:100], 0)
    return hole1, hole2, hole3, hole4, hole5, hole6


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
                help="Path to the source image dir")
ap.add_argument("-o", "--output", required=True,
                help="Path to the target image dir")
args = vars(ap.parse_args())


if os.path.isdir(args["input"]) == False:
    print_useage()
    exit(1)

if os.path.isdir(args["output"]) == False:
    mkdir_p(args["output"])


inputpath = args["input"]
outputpath = args["output"]


for path, subdir, files in os.walk(args["input"]):
    for name in files:
        input_file = os.path.join(path, name)
        if not os.path.exists(input_file):
            print(input_file + ": file not found")
            continue
        basename, ext = os.path.splitext(name)
        if ((ext.lower() == ".jpg") and (basename[0] != '~')):
            output_path = os.path.join(
                outputpath, os.path.relpath(path, inputpath))
            mkdir_p(output_path)
            mkdir_p(os.path.join(output_path, 'ok'))
            mkdir_p(os.path.join(output_path, 'ng'))

            names = basename.split("-")
            errors = ""

            if basename.endswith("_All") == True:
                errors = ['1', '2', '3', '4', '5', '6']
            elif len(names) > 1 and names[1] != None:
                errors = names[1].split(",")

            img = cv2.imread(input_file)

            try:
                hole1, hole2, hole3, hole4, hole5, hole6 = detect_segment(img)
            except:
                print("{} Exception ".format(basename+".jpg"))
                continue

            # print(output_path)
            # print(output_path)
            # print(os.path.relpath(path, inputpath))
            # print(path, inputpath)

            if '1' in errors:
                path1 = os.path.join(output_path, "ng", basename + "_1.jpg")
            else:
                path1 = os.path.join(output_path, "ok", basename + "_1.jpg")

            if '2' in errors:
                path2 = os.path.join(output_path, "ng", basename + "_2.jpg")
            else:
                path2 = os.path.join(output_path, "ok", basename + "_2.jpg")

            if '3' in errors:
                path3 = os.path.join(output_path, "ng", basename + "_3.jpg")
            else:
                path3 = os.path.join(output_path, "ok", basename + "_3.jpg")

            if '4' in errors:
                path4 = os.path.join(output_path, "ng", basename + "_4.jpg")
            else:
                path4 = os.path.join(output_path, "ok", basename + "_4.jpg")

            if '5' in errors:
                path5 = os.path.join(output_path, "ng", basename + "_5.jpg")
            else:
                path5 = os.path.join(output_path, "ok", basename + "_5.jpg")

            if '6' in errors:
                path6 = os.path.join(output_path, "ng", basename + "_6.jpg")
            else:
                path6 = os.path.join(output_path, "ok", basename + "_6.jpg")

            cv2.imwrite(path1, hole1)
            cv2.imwrite(path2, hole2)
            cv2.imwrite(path3, hole3)
            cv2.imwrite(path4, hole4)
            cv2.imwrite(path5, hole5)
            cv2.imwrite(path6, hole6)         
            print("{}  complete".format(basename + ".jpg"))

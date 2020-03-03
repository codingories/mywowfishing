# _*_coding:utf-8_*_
# Author      :ories
# File_Name   :fishing.py
# Create_Date :2020-02-26 19:31
# Description :wow fishing script
# IDE         :PyCharm
import math
import time

import autopy as at
from pykeyboard import PyKeyboard
import pyscreenshot as ImageGrab
import cv2
import numpy as np
from collections import deque
import pyaudio
import audioop

# x = 0

k = PyKeyboard()

# import autopy
1
dev = False


def check_screen_size():
    print("Checking screen size")
    img = ImageGrab.grab()
    # img.save('temp.png')
    print('img.size')

    print(img.size)

    global screen_size
    global screen_start_point
    global screen_end_point
    # screen_size = (img.size[0] / 2, img.size[1] / 2)
    screen_size = (img.size[0], img.size[1])

    print(screen_size)
    screen_start_point = (screen_size[0] * 0.35, screen_size[1] * 0.35)
    # print(screen_start_point)
    screen_end_point = (screen_size[0] * 0.65, screen_size[1] * 0.65)
    # print(screen_end_point)
    print("Screen size is " + str(screen_size))


def send_float():
    print('Sending float')
    k.tap_key('1', 1)
    print('Float is sent, waiting animation')
    time.sleep(2)


def make_screenshot():
    print('进入make_screenshot')
    size = (int(screen_start_point[0]), int(screen_start_point[1]), int(screen_end_point[0]), int(screen_end_point[1]))
    print(size)
    screenshot = ImageGrab.grab(bbox=size)
    global x
    screenshot_name = 'var/fishing_session' + str(x) + '.png'
    screenshot.save(screenshot_name)
    return screenshot_name

def move_mouse(place):
    # print(place)
    print('进入move_mouse')
    x, y = place[0], place[1]
    print(x, y)
    # print("Moving cursor to " + str(place))
    # print(screen_start_point[0],screen_start_point[1])
    # print(x, y)
    location_x = int(screen_start_point[0]) / 2
    location_y = int(screen_start_point[1]) / 2
    print("location_x, location_y")
    print(location_x, location_y)
    lx = location_x+x/2 + 30
    ly = location_y+y/2 + 30
    print('ly, ly')
    print(lx, ly)
    at.mouse.smooth_move(lx, ly)

def jump():
    print('Jump!')
    # autopy.key.tap(u' ')
    # k.tap_key('', 1)
    time.sleep(1)

    # at.mouse.smooth_move(500,500)
def find_float(img_name):
    print('Looking for float')
    # todo: maybe make some universal float without background?
    # for x in range(0, 7):


    # 加载原始的rgb图像
    img_rgb = cv2.imread(img_name)
    # 创建一个原始图像的灰度版本，所有操作在灰度版本中处理，然后在RGB图像中使用相同坐标还原
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    # 加载将要搜索的图像模板
    template = cv2.imread('var/fishing_float.png', 0)

    height, width = template.shape[:2]
    size = (int(width*0.5), int(height*0.5))
    template = cv2.resize(template, size, interpolation=cv2.INTER_AREA)


    # 记录图像模板的尺寸
    w, h = template.shape[::-1]

    # # 查看三组图像(图像标签名称，文件名称)
    # cv2.imshow('rgb', img_rgb)
    # cv2.imshow('gray', img_gray)
    # cv2.imshow('template', template)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # # 使用matchTemplate对原始灰度图像和图像模板进行匹配
    # res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    # # 设定阈值
    # threshold = 0.7s
    # # res大于70%
    # loc = np.where(res >= threshold)
    #
    # # 使用灰度图像中的坐标对原始RGB图像进行标记
    # for pt in zip(*loc[::-1]):
    #     print(pt)
    #     cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (7, 249, 151), 2)
    # # 显示图像
    # cv2.imshow('Detected', img_rgb)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()



    res = cv2.matchTemplate(img_gray, template, cv2.TM_SQDIFF_NORMED)
    # 'cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
    # 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED'
    # cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED 是最小值

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # print(min_val, max_val, min_loc, max_loc)
    #
    #
    # print('找到的坐标')
    # print(min_loc)
    # top_left = (min_loc[0]-20,min_loc[1])  # 左上角的位置
    top_left = min_loc  # 左上角的位置

    bottom_right = (top_left[0] + w, top_left[1] + h)  # 右下角的位置
    #
    # 在原图上画矩形
    cv2.rectangle(img_rgb, top_left, bottom_right, (0, 0, 255), 2)
    # 显示原图和处理后的图像,
    cv2.imshow("template", template)
    cv2.imshow("processed", img_rgb)
    cv2.waitKey()

    # print(min_loc)
    return top_left


def listen():
    print('Well, now we are listening for loud sounds...')
    CHUNK = 1024  # CHUNKS of bytes to read each time from mic
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 18000
    THRESHOLD = 1200  # The threshold intensity that defines silence
    # and noise signal (an int. lower than THRESHOLD is silence).
    SILENCE_LIMIT = 1  # Silence limit in seconds. The max ammount of seconds where
    # only silence is recorded. When this time passes the
    # recording finishes and the file is delivered.
    # Open stream
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    cur_data = ''  # current chunk  of audio data
    rel = RATE/CHUNK
    # print(rel)
    slid_win = deque(maxlen=SILENCE_LIMIT * int(rel))

    success = False
    listening_start_time = time.time()
    while True:
        try:
            cur_data = stream.read(CHUNK)
            slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
            if(sum([x > THRESHOLD for x in slid_win]) > 0):
                print('I heart something!')
                success = True
                break
            if time.time() - listening_start_time > 20:
                print('I don\'t hear anything already 20 seconds!')
                break
        except IOError:
            break

    # print "* Done recording: " + str(time.time() - start)
    stream.close()
    p.terminate()
    return success

def snatch():
    print('Snatching!')
    at.mouse.click(at.mouse.Button.RIGHT)
    time.sleep(0.5)
    at.mouse.click(at.mouse.Button.RIGHT)


def main():
    # time.sleep(3)
    # check_screen_size()
    # while True:
        # global x
        # x += 1
        # send_float()
        # im = make_screenshot()
        # place = find_float(im)
        # move_mouse(place)
        # if not listen():
        #     print('If we didn\' hear anything, lets try again')
        # snatch()


    # 调试用
    im = 'var/fishing_session.png'
    place = find_float(im)

main()

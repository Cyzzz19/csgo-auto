import cv2
from PIL import Image, ImageGrab
from win32 import win32api, win32gui, win32print
from win32.lib import win32con
from win32.win32api import GetSystemMetrics
import os
import time
import ctypes
import math
import operator
from functools import reduce
from ultralytics import YOLO
from queue import Queue
import threading
import socket
import serial


def mouse_clamp(b):
    a = int(b)
    if a >= 127:
        a = 127
    if a <= -128:
        a = -128
    return a

def get_real_resolution():
    """获取真实的分辨率"""
    hDC = win32gui.GetDC(0)
    # 横向分辨率
    w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    # 纵向分辨率
    h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return w, h
def get_screen_size():
    """获取缩放后的分辨率"""
    w = GetSystemMetrics (0)
    h = GetSystemMetrics (1)
    return w, h
def click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.1)
def mouse_move(a,b):
    mouse_resolution = get_screen_size()
    x, y = win32api.GetCursorPos()
    x += a*mouse_resolution[0]
    y += b*mouse_resolution[1]
    win32api.SetCursorPos((int(x), int(y)))
    
def mouse_goto(a,b):
    mouse_resolution = get_screen_size()
    x = 0
    y = 0
    x += a*mouse_resolution[0]
    y += b*mouse_resolution[1]
    win32api.SetCursorPos((int(x), int(y)))
def serial_send(data,ser):
    try:
        sign = data[0]
        if data[1] <0:
            x = 256 + data[1]
        else:
            x = data[1]
        if data[2] <0:
            y = 256 + data[2]
        else:
            y = data[2]
        if data[3] <0:
            wheel = 256 + data[3]
        else:
            wheel = data[3]
        keep = data[4]
        ser.write(sign.to_bytes(length =1,byteorder='big',signed=False) + x.to_bytes(length =1,byteorder='big',signed=False) + y.to_bytes(length =1,byteorder='big',signed=False) + wheel.to_bytes(length =1,byteorder='big',signed=False) + keep.to_bytes(length =1,byteorder='big',signed=False))
    except:
        print('serial send error')

    








model = YOLO("model/best.pt")
print("yolo is begin")
#    try:
#        model.predict(source="bus.png")
#        print("yolo is ready")
#    except:
#        print("yolo faild to run")
ser = serial.Serial('com4', 115200, timeout=1)
print('serial is begin')
cap = cv2.VideoCapture(0)
print('camera process is on')
cap.set(3,1920)
cap.set(4,1080)
cap.set(5,60)


a=0
fpses=0
time_start=0
time_end=0
flag = 0
while True:
    ret, frame = cap.read()
    im1 = Image.fromarray(cv2.cvtColor(frame[300:780, 500:1420], cv2.COLOR_BGR2RGB))
    #im1.save('1.png')
    frames = []
    results = model.predict(source=im1)  # save plotted images
    for result in results:
        p = result.boxes.xyxy.cpu().numpy().tolist()
        if len(p) >= 1:
            lst = p[0]
            lst[0] = lst[0]/result.orig_shape[1]
            lst[1] = lst[1]/result.orig_shape[0]
            lst[2] = lst[2]/result.orig_shape[1]
            lst[3] = lst[3]/result.orig_shape[0]
            conf = result.boxes.conf.cpu().numpy().tolist()[0]
                #print(lst,result.names,conf)  # box with xyxy format, (N, 4)
            frames.append([lst,result.names,conf])

    target = 'yellow_man'
    for i , f in enumerate(frames):
        if f[1][i] == target and f[2] > 0.5:
            print('goto',f[0])
            d = [8,mouse_clamp(((f[0][0]+f[0][2])/2 - 0.5)*1400/4),mouse_clamp(((f[0][1]+f[0][3])/2 - 0.5)*700/4),0,0]
            serial_send(d,ser)
            break

        






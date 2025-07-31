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

while True:
    mouse_goto(100,0)
    time.sleep(1)
    mouse_goto(0,100)
    time.sleep(1)
    mouse_goto(-100,0)
    time.sleep(1)
    mouse_goto(0,-100)
    time.sleep(1)

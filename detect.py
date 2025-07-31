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
video_stream = Queue(2)
video_stream_sign = Queue(2)
frame_stream = Queue(16)
server_control_stream = Queue(8)
mouse_control_flow = Queue(16)
#try:
#    print("loading yolo")
#    model = YOLO("model/best.pt")
 #   #yolo_model.put(model)
#except:
    #print('faild to load model')
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

def server():
    try:
        socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#创建一个socket对象
        host = "192.168.6.246"
        port = 8848
        socket_server.bind((host, port))#绑定地址
        socket_server.listen(5)#设置监听
        print('server is listen on',host,port)
        while True:
            try:
                client_socket, address = socket_server.accept()# socket_server.accept()返回一个元组, 元素1为客户端的socket对象, 元素2为客户端的地址(ip地址，端口号)
                while True:#while循环是为了让对话持续
                    recvmsg = client_socket.recv(1024)#接收客户端的请求
                    strData = recvmsg.decode("utf-8")
                    server_control_stream.put(strData)
            except:
                print('connection pass')
    except:
        print('server close')
        socket_server.close()
def client_s():
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_ip = '192.168.6.121'
            server_port = 23664
            client_socket.connect((server_ip, server_port))
            client_socket.send("1".encode('ascii'))
            print("connected")
            a=0
        except:
            print("failed")
    
        while True:
            try:
                if not mouse_control_flow.empty():
                    d = mouse_control_flow.get()
                    s = str(d[0]) +';'+ str(d[1]) +';'+ str(d[2]) +';'+ str(d[3]) +';'+ str(d[4])
                    client_socket.send(s.encode('ascii'))
            except socket.error as e:
                print(f"Failed to snd data: {e}")

def capture():
    # 调用摄像头
    try:
        
        cap = cv2.VideoCapture(0)
        print('camera process is on')
        cap.set(3,1920)
        cap.set(4,1080)
        cap.set(5,60)
        
        while True:
            #if not video_stream_sign.empty():
            #video_stream_sign.get()
            ret, frame = cap.read()
            pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            video_stream.put(pil_image)
                
    except:
        cap.release()
        print('camera capture error')






model = YOLO("model/best.pt")
def yolo_predict():
#    try:
#        model.predict(source="bus.png")
#        print("yolo is ready")
#    except:
#        print("yolo faild to run")
    try:
        while True:
            if not video_stream.empty():
                frames = []
                im1 = video_stream.get()
                results = model.predict(source=im1)  # save plotted images
                for result in results:
                    p = result.boxes.xyxy.cpu().numpy().tolist()
                    if len(p) >= 1:
                        lst = p[0]
                        lst[0] = lst[0]/result.orig_shape[1]
                        lst[1] = lst[1]/result.orig_shape[0]
                        lst[2] = lst[2]/result.orig_shape[1]
                        lst[3] = lst[3]/result.orig_shape[0]
                        print(lst,result.orig_shape)
                        conf = result.boxes.conf.cpu().numpy().tolist()[0]
                        #print(lst,result.names,conf)  # box with xyxy format, (N, 4)
                        frames.append([lst,result.names,conf])
                frame_stream.put(frames)
            #video_stream_sign.put(1)
    except Exception as e:
    # Handles the exception
        print(f"predict function An error occurred: {e}")
        

camera_thread = threading.Thread(target=capture)
yolo_thread = threading.Thread(target=yolo_predict)
socket_server_thread = threading.Thread(target=server)
socket_server_send_thread = threading.Thread(target=client_s)
# Each result is composed of torch.Tensor by default,
# in which you can easily use following functionality:



camera_thread.start()
yolo_thread.start()
#socket_server_thread.start()
socket_server_send_thread.start()
fpses=0
time_start=0
time_end=0
flag = 0
    
while True:
    if not server_control_stream.empty():
        msg = server_control_stream.get()
        try:
            flag = int(msg)
            print('flag',msg)
        except:
            print(msg)
    while True:#flag == 1:
        #fps
        time_end=time.time()
        if time_end-time_start >=1:
            print('                                            fps:',fpses)
            fpses = 0
            time_start=time.time()
        fpses+=1
        #end fps
        if not server_control_stream.empty():
            msg = server_control_stream.get()
            try:
                flag = int(msg)
                print('flag',msg)
            except:
                print(msg)
        target = 'yellow_man'
        frames = frame_stream.get()

        for i , f in enumerate(frames):
            #evaluate f: [lst,results.names,conf]
            if f[1][i] == target and f[2] > 0.5:
                print('goto',f[0])
                #mouse_goto((f[0][0]+f[0][2])/2,(f[0][1]+f[0][3])/2)
                mouse_control_flow.put([8,mouse_clamp((f[0][0]+f[0][2])/2*3840),mouse_clamp((f[0][1]+f[0][3])/2*2160),0,0])



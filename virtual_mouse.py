
import os
import time
import ctypes
import math
import operator
from queue import Queue
import threading
import socket
import serial



mouse_control_flow = Queue(16)



def client():
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_ip = '127.0.0.1'
            server_port = 23664
            client_socket.connect((server_ip, server_port))
            client_socket.send("1".encode('ascii'))
            print("connected")
            a=0
        except:
            print("failed")
    
        while True:
            if True:
                try:
                    msg = client_socket.recv(1024)
                    tmp = msg.decode('utf-8').split(';')
                    tmp[0] = int(tmp[0])
                    tmp[1] = int(tmp[1])
                    tmp[2] = int(tmp[2])
                    tmp[3] = int(tmp[3])
                    tmp[4] = int(tmp[4])
                    if len(tmp) == 4:
                        mouse_control_flow.put(tmp)
                    else:
                        print('length error')
                except socket.error as e:
                    print(f"Failed to recv data: {e}")

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

def virtual_mouse():
    try:
        ser = serial.Serial('com4', 115200, timeout=1)
        serial_send([0,0,0,0,0],ser)
        print('serial is begin')
    except Exception as e:
        print('serial is dead',e)
    while True:
        if not mouse_control_flow.empty():
            try:
                data = mouse_control_flow.get()
                serial_send(data,ser)
            except:
                print('serial send error')

virtual_mouse_thread = threading.Thread(target=virtual_mouse)
virtual_mouse_thread.start()
client()

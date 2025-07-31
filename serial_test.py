import serial
import time

#-128:127
#sign_t ;x_t; y_t; wheel_t; keep_t
data = [8,0,0,0,0]
ser = serial.Serial('com4', 115200, timeout=1)
def serial_send(data,ser):
    
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
    #print(ser.read())
    #print(sign.to_bytes(length =1,byteorder='big',signed=False) + x.to_bytes(length =1,byteorder='big',signed=False) + y.to_bytes(length =1,byteorder='big',signed=False) + wheel.to_bytes(length =2,byteorder='big',signed=False))
    #time.sleep(1)


#sign:
#1:LD 2:MD 3:RD 4:LU 5:MU 6:RU 7:wheel 8:move
while True:
    serial_send(data,ser)
    time.sleep(1)

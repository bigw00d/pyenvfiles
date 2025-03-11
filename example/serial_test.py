import os
import serial
import serial.tools.list_ports
import threading

#----------------------
# データを送信
#----------------------
def serial_write():
    global Serial_Port
    
    while(1):
        if Serial_Port !='':
            data=input()+'\r\n'
            data=data.encode('utf-8')
            Serial_Port.write(data)

#----------------------
# データを受信
#----------------------
def serial_read():
    global Serial_Port
    while(1):
        if Serial_Port !='':
            #data=Serial_Port.read(1)
            data=Serial_Port.readline()
            data=data.strip()
            data=data.decode('utf-8')
            print(data)

#----------------------
# シリアルポートをOpen
#----------------------
def serial_open():
    global Serial_Port
    
    #portリストを取得
    serial_ports={}
    for i,port in enumerate(serial.tools.list_ports.comports()):
        serial_ports[str(i)]=port.device
    
    #RaspberryPiのminiUART検出できないので、/dev/ttyAMA0があれば自動的に/dev/ttyS0を追加
    if '/dev/ttyAMA0' in serial_ports.values():
        serial_ports[str(len(serial_ports))]='/dev/ttyS0'

    port_val = serial_ports[ input(f'ポート番号を選んでください。{serial_ports}:') ]
    boud_val = int(input('ボーレートbpsを数値で入力してください。:'))
    prty_val = input(f'パリティーを選んでください。[N:None, O:Odd, E:Even]:')
    
    Serial_Port=serial.Serial(port=port_val, baudrate=boud_val, parity= prty_val)
    print(f'open{port_val}/{boud_val}bps/parity:{prty_val}')


if __name__ == '__main__':

    Serial_Port=''
    
    #port open
    serial_open()
    
    thread_1 = threading.Thread(target=serial_write)
    thread_2 = threading.Thread(target=serial_read)

    thread_1.start()
    thread_2.start()
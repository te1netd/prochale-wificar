############################
# ロボットカーをWIFIでコントロールするプログラム
#  ロボットカー側
#  WIFI AP化
#  GP
############################


#
# WIFI をつかうためのモジュール
#
import network

#
# ソケット（UDPのネットワーク通信)を使うためのモジュール
#
import socket

#
# PICOのピンやLEDを使うためのモジュール
#
import machine

#
# time.sleep()を使うためのモジュール
#
import time



############################
# 設定
############################

#
# ロボットカーをWIFI APにします。WIFI　AP　のSIDとパスワードを設定。
# SSIDは自分だけの名前
# パスワードは秘密にします。
#
SSID:str = 'robot_lufy'  # 任意のアクセスポイント名を指定可能
PASSWORD:str = 'roborobonomi'  # 任意のパスワードを指定可能

#
# UDP port for robot communication
#
UDP_PORT = 80

#
# led for pico W internal LED
#
led= machine.Pin('LED', machine.Pin.OUT)

#
# Pins for Motor control
#
GP0 = machine.Pin(0, machine.Pin.OUT)
GP1 = machine.Pin(1, machine.Pin.OUT)
GP2 = machine.Pin(2, machine.Pin.OUT)
GP3 = machine.Pin(3, machine.Pin.OUT)


############################
# MAIN
############################

#
# LEDを３回点滅
# 起動したことを明示する
#
led.off()
for i in range(6):
  led.toggle()
  time.sleep(0.05)



#
# アクセスポイントを作成し、access_pointを返す
#
access_point = network.WLAN(network.AP_IF)  
access_point.config(essid=SSID, password=PASSWORD)

#
# アクセスポイントとして検知されるようになる
#
access_point.active(True)  

#
# IP address, netmask, gateway, DNSを固定IPで設定 
# gateway, DNSは使いません。 active(True)の後に設定必要。
#
access_point.ifconfig(('192.168.100.1', '255.255.255.0', '192.168.100.1', '192.168.100.1'))

ip = access_point.ifconfig()[0]

    

#
# 接続が成功した場合、(IPアドレス、ネットマスク、ゲートウェイ、DNS)を表示
#
print("Please connection access_point by other device...")
print("IP Address:{}\nNet Mask:{}\nGateway:{}\nDNS:{}".format(*access_point.ifconfig()))

#
# Open UDP port
#
if not 'connection' in globals():
    # Open a socket
    address = (ip, UDP_PORT)
    connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(('0.0.0.0', UDP_PORT))
    print('UDP Bound...')

#
# デバッグ用　IPアドレスが代っていない場合LEDを消す
#
if ip == '192.168.4.1':
    led.off()
else:
    led.on()

while True:
    try:
        #
        # recvfrom で、送信された文字を受け取る。文字を受け取るまで停止します。
        #
        print ("recving...")
        data, addr = connection.recvfrom(1024) # receive up to 1024 bytes

        #
        # 文字を受け取った。
        # 文字を受け取ったことがわかるように、本体LEDを１回点滅させる。
        #
        print(f"Received packet from {addr}: {data.decode()}")
        
        led.toggle()
        time.sleep(0.05)
        led.toggle()

        #
        # 受け取った文字に　”s”　が入っていたら。。。停止する
        #
        if "s" in data :
            GP0.off()
            GP1.off() 
            GP2.off()
            GP3.off() 


        #
        # 受け取った文字に　”f”　が入っていたら。。。前進する
        #
        if "f" in data :
            GP0.on()
            GP1.off() 
            GP2.on()
            GP3.off() 

        #
        # 受け取った文字に　”b”　が入っていたら。。。バックする
        #
        if "b" in data :
            GP0.off()
            GP1.on() 
            GP2.off()
            GP3.on() 
            
        #
        # 受け取った文字に　”r”　が入っていたら。。。右回転する
        #
        if "r" in data :
            GP0.on()
            GP1.off() 
            GP2.off()
            GP3.on() 

        #
        # 受け取った文字に　”l”　が入っていたら。。。左回転する
        #
        if "l" in data :
            GP0.off()
            GP1.on() 
            GP2.on()
            GP3.off() 

    #
    #　Thonnyのストップ押下時やエラー発生時にUDP connectionをクローズ。
    #   (非同期動作しているsocketコンポーネント側でUDPが開きっぱなししならないように)
    #
    except OSError as e:
#       connection.close()
        print('stopped recvfrom()')





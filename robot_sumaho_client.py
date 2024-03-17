#########################################
# wifi-remotecarをコントロールするリモコン側のプログラム
# スマホ上のpydroidで動かせる。
#########################################

#
# ソケット（UDP通信を使うためのモジュール）
#
import socket

#
# ソケット（通信する元）を作成する
#
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#
# アドレスは車側に割り当てられたアドレスに変更する。
#
serv_address = ('192.168.100.1', 80)

while True:
  #
  # 入力したメッセージを、ロボットへ送信する。
  #
  message = input()
  sock.sendto(message.encode('utf-8'), serv_address)
 
import socket  
import RPi.GPIO as GPIO  
import time  
  
# 设置GPIO模式为BCM  
GPIO.setmode(GPIO.BCM)  
# 选择一个可用的GPIO引脚，比如GPIO 18  
BEEP_PIN = 18  
# 设置GPIO引脚为输出模式  
GPIO.setup(BEEP_PIN, GPIO.OUT)  
  
# 创建socket对象  
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
# 获取本地主机名  
host_name = socket.gethostname()  
port = 12345  # 选择一个未被占用的端口  
  
# 绑定端口号  
server_socket.bind((host_name, port))  
  
# 设置最大连接数，超过后排队  
server_socket.listen(5)  
  
while True:  
    # 建立客户端连接  
    client_socket, addr = server_socket.accept()  
    print("连接地址: %s" % str(addr))  
      
    try:  
        while True:  
            # 接收来自客户端的数据  
            data = client_socket.recv(1024).decode()  
            if data == 'beep on':  
                GPIO.output(BEEP_PIN, GPIO.LOW)  # 设置GPIO为低电平  
                print("蜂鸣器开启")  
            elif data == 'beep off':  
                GPIO.output(BEEP_PIN, GPIO.HIGH)  # 设置GPIO为高电平  
                print("蜂鸣器关闭")  
            else:  
                print("未知命令")  
    except Exception as e:  
        print(e)  
    finally:  
        # 关闭连接  
        client_socket.close()
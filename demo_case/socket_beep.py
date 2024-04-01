import socket  
import RPi.GPIO as GPIO  
import time  
  
# ����GPIOģʽΪBCM  
GPIO.setmode(GPIO.BCM)  
# ѡ��һ�����õ�GPIO���ţ�����GPIO 18  
BEEP_PIN = 18  
# ����GPIO����Ϊ���ģʽ  
GPIO.setup(BEEP_PIN, GPIO.OUT)  
  
# ����socket����  
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
# ��ȡ����������  
host_name = socket.gethostname()  
port = 12345  # ѡ��һ��δ��ռ�õĶ˿�  
  
# �󶨶˿ں�  
server_socket.bind((host_name, port))  
  
# ����������������������Ŷ�  
server_socket.listen(5)  
  
while True:  
    # �����ͻ�������  
    client_socket, addr = server_socket.accept()  
    print("���ӵ�ַ: %s" % str(addr))  
      
    try:  
        while True:  
            # �������Կͻ��˵�����  
            data = client_socket.recv(1024).decode()  
            if data == 'beep on':  
                GPIO.output(BEEP_PIN, GPIO.LOW)  # ����GPIOΪ�͵�ƽ  
                print("����������")  
            elif data == 'beep off':  
                GPIO.output(BEEP_PIN, GPIO.HIGH)  # ����GPIOΪ�ߵ�ƽ  
                print("�������ر�")  
            else:  
                print("δ֪����")  
    except Exception as e:  
        print(e)  
    finally:  
        # �ر�����  
        client_socket.close()
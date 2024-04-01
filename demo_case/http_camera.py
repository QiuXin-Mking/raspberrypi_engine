# -*- coding: utf-8 -*-
import cv2  
import socketserver  
from http.server import SimpleHTTPRequestHandler  
import threading  
  
# 设置摄像头  
cap = cv2.VideoCapture(0)  
  
# 设置HTTP服务器  
PORT = 8000  
  
class StreamingHTTPRequestHandler(SimpleHTTPRequestHandler):  
    def do_GET(self):  
        if self.path.endswith('.mjpg'):  
            self.send_response(200)  
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')  
            self.end_headers()  
            return self.serve_mjpeg()  
        return super().do_GET()  
  
    def serve_mjpeg(self):  
        try:  
            while True:  
                ret, frame = cap.read()  
                if not ret:  
                    break  
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
                j, img_encoded = cv2.imencode('.jpg', rgbImage)  
                self.wfile.write("--jpgboundary\r\n".encode())  
                self.send_header('Content-type', 'image/jpeg')  
                self.send_header('Content-length', str(len(img_encoded)))  
                self.end_headers()  
                self.wfile.write(img_encoded.tobytes())  
        except Exception as e:  
            print(e)  
        finally:  
            cap.release()  
  
with socketserver.TCPServer(("", PORT), StreamingHTTPRequestHandler) as httpd:  
    print("serving at port", PORT)  
    httpd.serve_forever()
import cv2
import socket

def send_frame():
    camera = cv2.VideoCapture(0)
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.1.5', 8000))

    while True:
        ret, frame = camera.read()
        if not ret:
            continue
        
        _, img_encoded = cv2.imencode('.jpg', frame)
        client_socket.sendall(img_encoded.tobytes())

import cv2
import numpy as np
import socket
import json
import RPi.GPIO as GPIO
import time
from threading import Thread
from utils import setup_gpio

class CarController:
    def __init__(self, host='0.0.0.0', port=5000):
        # Initialize GPIO pins for motor control
        self.setup_gpio()
        
        # Initialize camera
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Initialize socket server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(1)
        
        # Motor control pins (adjust these based on your wiring)
        self.left_motor_forward = 17
        self.left_motor_backward = 27
        self.right_motor_forward = 22
        self.right_motor_backward = 23
        
        # Initialize connection
        self.client_socket = None
        self.connected = False

    def setup_gpio(self):
        """Setup GPIO pins for motor control"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Setup motor control pins as output
        pins = [17, 27, 22, 23]  # Adjust these based on your wiring
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
    
    def connect(self):
        """Wait for connection from laptop"""
        print("Waiting for connection...")
        self.client_socket, addr = self.server_socket.accept()
        self.connected = True
        print(f"Connected to {addr}")
    
    def send_image(self, image):
        """Send image to laptop"""
        if self.connected:
            # Encode image as JPEG
            _, img_encoded = cv2.imencode('.jpg', image)
            # Send image size first
            self.client_socket.send(len(img_encoded).to_bytes(4, 'big'))
            # Send image data
            self.client_socket.send(img_encoded.tobytes())
    
    def receive_command(self):
        """Receive command from laptop"""
        if self.connected:
            try:
                data = self.client_socket.recv(1024).decode()
                if data:
                    return json.loads(data)['command']
            except:
                return None
        return None
    
    def execute_command(self, command):
        """Execute driving command"""
        if command == 'forward':
            self.move_forward()
        elif command == 'backward':
            self.move_backward()
        elif command == 'left':
            self.turn_left()
        elif command == 'right':
            self.turn_right()
        elif command == 'stop':
            self.stop()
    
    def move_forward(self):
        """Move car forward"""
        GPIO.output(self.left_motor_forward, GPIO.HIGH)
        GPIO.output(self.left_motor_backward, GPIO.LOW)
        GPIO.output(self.right_motor_forward, GPIO.HIGH)
        GPIO.output(self.right_motor_backward, GPIO.LOW)
    
    def move_backward(self):
        """Move car backward"""
        GPIO.output(self.left_motor_forward, GPIO.LOW)
        GPIO.output(self.left_motor_backward, GPIO.HIGH)
        GPIO.output(self.right_motor_forward, GPIO.LOW)
        GPIO.output(self.right_motor_backward, GPIO.HIGH)
    
    def turn_left(self):
        """Turn car left"""
        GPIO.output(self.left_motor_forward, GPIO.LOW)
        GPIO.output(self.left_motor_backward, GPIO.HIGH)
        GPIO.output(self.right_motor_forward, GPIO.HIGH)
        GPIO.output(self.right_motor_backward, GPIO.LOW)
    
    def turn_right(self):
        """Turn car right"""
        GPIO.output(self.left_motor_forward, GPIO.HIGH)
        GPIO.output(self.left_motor_backward, GPIO.LOW)
        GPIO.output(self.right_motor_forward, GPIO.LOW)
        GPIO.output(self.right_motor_backward, GPIO.HIGH)
    
    def stop(self):
        """Stop car"""
        GPIO.output(self.left_motor_forward, GPIO.LOW)
        GPIO.output(self.left_motor_backward, GPIO.LOW)
        GPIO.output(self.right_motor_forward, GPIO.LOW)
        GPIO.output(self.right_motor_backward, GPIO.LOW)
    
    def run(self):
        """Main loop for car control"""
        try:
            self.connect()
            
            while True:
                # Capture frame from camera
                ret, frame = self.camera.read()
                if ret:
                    # Send frame to laptop
                    self.send_image(frame)
                    
                    # Receive and execute command
                    command = self.receive_command()
                    if command:
                        self.execute_command(command)
                
                time.sleep(0.1)  # Small delay to prevent overwhelming the system
                
        except KeyboardInterrupt:
            print("Stopping car controller...")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        self.stop()
        GPIO.cleanup()
        self.camera.release()
        if self.client_socket:
            self.client_socket.close()
        self.server_socket.close()

if __name__ == "__main__":
    controller = CarController()
    controller.run()

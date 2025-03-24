import torch
from transformers import Blip2Processor, Blip2ForConditionalGeneration
import cv2
import numpy as np
import socket
import json
import time

class VLMController:
    def __init__(self, host='localhost', port=5000):
        # Initialize BLIP-2 model and processor
        self.processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
        self.model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b")
        
        # Initialize socket connection to Raspberry Pi
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        
        # Define driving commands
        self.commands = {
            'forward': 'move forward',
            'left': 'turn left',
            'right': 'turn right',
            'stop': 'stop the car'
        }
        
    def process_image(self, image):
        """Process image through BLIP-2 and generate driving command"""
        # Preprocess image
        inputs = self.processor(image, return_tensors="pt")
        
        # Generate description
        outputs = self.model.generate(**inputs, max_length=50)
        scene_description = self.processor.decode(outputs[0], skip_special_tokens=True)
        
        # Analyze scene description to determine command
        command = self._analyze_scene(scene_description)
        return command
    
    def _analyze_scene(self, description):
        """Analyze scene description to determine appropriate driving command"""
        description = description.lower()
        
        # Simple rule-based decision making
        if 'obstacle' in description or 'stop' in description:
            return 'stop'
        elif 'left' in description or 'turn left' in description:
            return 'left'
        elif 'right' in description or 'turn right' in description:
            return 'right'
        else:
            return 'forward'
    
    def send_command(self, command):
        """Send command to Raspberry Pi"""
        data = {'command': command}
        self.socket.send(json.dumps(data).encode())
    
    def run(self):
        """Main loop for processing camera feed and sending commands"""
        try:
            while True:
                # Receive image from Raspberry Pi
                # Note: This part needs to be implemented based on your image transfer protocol
                # For now, we'll use a placeholder
                image = self._receive_image()
                
                # Process image and get command
                command = self.process_image(image)
                
                # Send command
                self.send_command(command)
                
                # Small delay to prevent overwhelming the system
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("Stopping VLM controller...")
        finally:
            self.socket.close()
    
    def _receive_image(self):
        """Placeholder for image receiving logic"""
        # This needs to be implemented based on your image transfer protocol
        # For now, return a dummy image
        return np.zeros((480, 640, 3), dtype=np.uint8)

if __name__ == "__main__":
    controller = VLMController()
    controller.run() 
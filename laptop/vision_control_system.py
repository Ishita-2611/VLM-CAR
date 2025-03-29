import torch
from transformers import CLIPProcessor, CLIPModel
import cv2
import numpy as np
from typing import Dict, List
import time

class VisionControlSystem:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(self.device)
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        self.camera = None
        self.is_running = False
        
        # Define control commands and their descriptions
        self.control_commands = {
            "move_forward": "a clear path ahead with no obstacles",
            "stop": "a pedestrian, vehicle, or obstacle in the path",
            "turn_left": "a clear path to the left",
            "turn_right": "a clear path to the right",
            "slow_down": "a narrow space or potential hazard ahead",
            "maintain_current": "no significant changes in the environment"
        }
        
    def initialize_camera(self):
        """Initialize the camera for visual input"""
        self.camera = cv2.VideoCapture(0)  # Use default camera
        if not self.camera.isOpened():
            raise RuntimeError("Failed to initialize camera")
            
    def get_camera_frame(self) -> np.ndarray:
        """Capture and return a frame from the camera"""
        if self.camera is None:
            raise RuntimeError("Camera not initialized")
        ret, frame = self.camera.read()
        if not ret:
            raise RuntimeError("Failed to capture frame")
        return frame
        
    def analyze_scene(self, image: np.ndarray) -> Dict[str, float]:
        """
        Analyze the visual scene using CLIP model
        Args:
            image: Input image array
        Returns:
            Dictionary of scene elements and their confidence scores
        """
        # Preprocess image
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)
        
        # Define scene elements to detect
        scene_elements = [
            "road", "pedestrian", "car", "traffic light", "stop sign",
            "obstacle", "clear path", "narrow space", "intersection",
            "left turn", "right turn", "straight path"
        ]
        
        # Get text inputs
        text_inputs = self.processor(text=scene_elements, return_tensors="pt", padding=True).to(self.device)
        
        # Get image and text features
        image_features = self.model.get_image_features(**inputs)
        text_features = self.model.get_text_features(**text_inputs)
        
        # Calculate similarity scores
        similarity = torch.nn.functional.cosine_similarity(
            image_features.unsqueeze(1),
            text_features.unsqueeze(0),
            dim=2
        )
        
        # Convert to confidence scores
        confidence_scores = torch.softmax(similarity, dim=1)
        
        # Create result dictionary
        results = {element: score.item() for element, score in zip(scene_elements, confidence_scores[0])}
        return results
    
    def determine_command(self, scene_analysis: Dict[str, float]) -> str:
        """
        Determine the appropriate command based on scene analysis
        Args:
            scene_analysis: Dictionary of scene elements and their confidence scores
        Returns:
            Command to execute
        """
        # Safety check
        if scene_analysis["pedestrian"] > 0.3 or scene_analysis["car"] > 0.3 or scene_analysis["obstacle"] > 0.3:
            return "stop"
            
        # Traffic signal check
        if scene_analysis["traffic light"] > 0.5:
            return "stop"
        if scene_analysis["stop sign"] > 0.5:
            return "stop"
            
        # Path analysis
        if scene_analysis["narrow space"] > 0.5:
            return "slow_down"
        elif scene_analysis["clear path"] > 0.7:
            return "move_forward"
            
        # Turn analysis
        if scene_analysis["left turn"] > 0.6:
            return "turn_left"
        elif scene_analysis["right turn"] > 0.6:
            return "turn_right"
            
        return "maintain_current"
        
    def generate_motor_commands(self, command: str) -> Dict[str, float]:
        """
        Generate motor commands based on the determined command
        Args:
            command: Determined command
        Returns:
            Dictionary of motor commands
        """
        commands = {
            "speed": 0.0,
            "steering": 0.0,
            "brake": 0.0
        }
        
        if command == "move_forward":
            commands["speed"] = 0.5
            commands["steering"] = 0.0
        elif command == "stop":
            commands["brake"] = 1.0
            commands["speed"] = 0.0
        elif command == "turn_left":
            commands["speed"] = 0.3
            commands["steering"] = -0.5
        elif command == "turn_right":
            commands["speed"] = 0.3
            commands["steering"] = 0.5
        elif command == "slow_down":
            commands["speed"] = 0.2
            commands["steering"] = 0.0
        else:  # maintain_current
            commands["speed"] = 0.3
            commands["steering"] = 0.0
            
        return commands
        
    def run_control_loop(self):
        """Main control loop for the robotic system"""
        self.is_running = True
        self.initialize_camera()
        
        try:
            while self.is_running:
                # 1. Capture and analyze visual scene
                frame = self.get_camera_frame()
                scene_analysis = self.analyze_scene(frame)
                
                # 2. Determine command based on scene analysis
                command = self.determine_command(scene_analysis)
                
                # 3. Generate and execute motor commands
                commands = self.generate_motor_commands(command)
                self.execute_commands(commands)
                
                # 4. Display feedback
                self.display_feedback(frame, commands, command, scene_analysis)
                
                # 5. Small delay to prevent overwhelming the system
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("Control loop interrupted by user")
        finally:
            self.cleanup()
            
    def execute_commands(self, commands: Dict[str, float]):
        """
        Execute motor commands
        Args:
            commands: Dictionary of motor commands
        """
        # TODO: Implement actual motor control interface
        print(f"Executing commands: {commands}")
        
    def display_feedback(self, frame: np.ndarray, commands: Dict[str, float], 
                        command: str, scene_analysis: Dict[str, float]):
        """
        Display system feedback on the frame
        Args:
            frame: Camera frame
            commands: Current motor commands
            command: Current command
            scene_analysis: Scene analysis results
        """
        # Add text overlays
        cv2.putText(frame, f"Command: {command}", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Speed: {commands['speed']:.2f}", 
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Steering: {commands['steering']:.2f}", 
                    (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Display the frame
        cv2.imshow("Vision Control System", frame)
        cv2.waitKey(1)
        
    def cleanup(self):
        """Clean up resources"""
        if self.camera is not None:
            self.camera.release()
        cv2.destroyAllWindows()
        self.is_running = False 
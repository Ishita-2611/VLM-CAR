import torch
from transformers import CLIPProcessor, CLIPModel
import cv2
import numpy as np
from typing import List, Tuple, Dict

class VisionLanguageProcessor:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(self.device)
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        
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
        
        # Define potential scene elements to detect
        scene_elements = [
            "road", "pedestrian", "car", "traffic light", "stop sign",
            "obstacle", "clear path", "narrow space", "intersection"
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
    
    def interpret_environment(self, scene_analysis: Dict[str, float]) -> Dict[str, str]:
        """
        Interpret the environment based on scene analysis
        Args:
            scene_analysis: Dictionary of scene elements and their confidence scores
        Returns:
            Dictionary of environment interpretations and recommendations
        """
        interpretations = {}
        
        # Safety assessment
        if scene_analysis["pedestrian"] > 0.3 or scene_analysis["car"] > 0.3:
            interpretations["safety_status"] = "high_risk"
        elif scene_analysis["clear_path"] > 0.7:
            interpretations["safety_status"] = "safe"
        else:
            interpretations["safety_status"] = "moderate_risk"
            
        # Path assessment
        if scene_analysis["narrow_space"] > 0.5:
            interpretations["path_status"] = "narrow"
        elif scene_analysis["clear_path"] > 0.7:
            interpretations["path_status"] = "clear"
        else:
            interpretations["path_status"] = "moderate"
            
        # Traffic assessment
        if scene_analysis["traffic light"] > 0.5:
            interpretations["traffic_status"] = "regulated"
        elif scene_analysis["stop sign"] > 0.5:
            interpretations["traffic_status"] = "stop_required"
        else:
            interpretations["traffic_status"] = "unregulated"
            
        return interpretations
    
    def get_safety_recommendations(self, interpretations: Dict[str, str]) -> List[str]:
        """
        Generate safety recommendations based on environment interpretations
        Args:
            interpretations: Dictionary of environment interpretations
        Returns:
            List of safety recommendations
        """
        recommendations = []
        
        if interpretations["safety_status"] == "high_risk":
            recommendations.append("Immediate stop required")
            recommendations.append("Maintain safe distance")
        elif interpretations["safety_status"] == "moderate_risk":
            recommendations.append("Proceed with caution")
            recommendations.append("Reduce speed")
            
        if interpretations["path_status"] == "narrow":
            recommendations.append("Slow down for narrow passage")
        elif interpretations["path_status"] == "clear":
            recommendations.append("Clear path ahead")
            
        if interpretations["traffic_status"] == "regulated":
            recommendations.append("Follow traffic signals")
        elif interpretations["traffic_status"] == "stop_required":
            recommendations.append("Stop and check surroundings")
            
        return recommendations 
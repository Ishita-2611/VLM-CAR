import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# Initialize BLIP-2 model (for example)
processor = BlipProcessor.from_pretrained("Salesforce/blip2-flan-t5-xl")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip2-flan-t5-xl").to("cuda" if torch.cuda.is_available() else "cpu")

def predict_command(image_path):
    image = Image.open(image_path)
    
    # Define prompt for the VLM
    prompt = "What is the next driving action? Choose one: forward, left, right, stop."

    # Preprocess
    inputs = processor(image, prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")

    # Get output
    out = model.generate(**inputs)
    response = processor.decode(out[0], skip_special_tokens=True)
    
    print(f"Predicted Command: {response}")
    return response.strip().lower()

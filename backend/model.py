import torch
from torchvision import models, transforms
from torchvision.models import ResNet18_Weights
from PIL import Image
from transformers import ViTForImageClassification, ViTImageProcessor
import json

## FINE-TUNED VIT MODEL ON LOCAL SPECIES DATASET


# Class names (adjust if saved separately)
with open("backend/class_names.json", "r") as f:
    class_names = json.load(f)

num_classes = len(class_names)
# Load processor and model
processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224-in21k")
model = ViTForImageClassification.from_pretrained("google/vit-base-patch16-224-in21k", num_labels=num_classes)

# Load fine-tuned weights
model.load_state_dict(torch.load("backend/mod/best_model.pth", map_location=torch.device("cpu")))
model.eval()


def predict_image(image_path: str) -> str:
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()
    
    return class_names[predicted_class]



## RESNET18 MODEL


# # Load model (you can adjust this to the model of your choice)
# model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
# model.eval()

# # Define a transform to match what the model expects
# transform = transforms.Compose([
#     transforms.Resize((224, 224)),
#     transforms.ToTensor(),
#     transforms.Normalize(
#         mean=[0.485, 0.456, 0.406],
#         std=[0.229, 0.224, 0.225]
#     ),
# ])

# imagenet_labels = ResNet18_Weights.DEFAULT.meta["categories"]

# def predict_image(file_path: str) -> str:
#     image = Image.open(file_path).convert("RGB")
#     input_tensor = transform(image).unsqueeze(0)
    
#     with torch.no_grad():
#         outputs = model(input_tensor)
#         _, predicted = torch.max(outputs, 1)
    
#     return imagenet_labels[predicted.item()]

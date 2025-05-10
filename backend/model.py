import torch
from torchvision import models, transforms
from torchvision.models import ResNet18_Weights
from PIL import Image

# Load model (you can adjust this to the model of your choice)
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
model.eval()

# Define a transform to match what the model expects
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
])

imagenet_labels = ResNet18_Weights.DEFAULT.meta["categories"]

def predict_image(file_path: str) -> str:
    image = Image.open(file_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0)
    
    with torch.no_grad():
        outputs = model(input_tensor)
        _, predicted = torch.max(outputs, 1)
    
    return imagenet_labels[predicted.item()]

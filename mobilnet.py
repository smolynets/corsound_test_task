from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import requests
import torch

url = "https://sheplis.com.ua/typo3temp/fl_realurl_image/bilka3-66.jpg"
image = Image.open(requests.get(url, stream=True).raw)

preprocessor = AutoImageProcessor.from_pretrained("google/mobilenet_v2_1.0_224")
model = AutoModelForImageClassification.from_pretrained("google/mobilenet_v2_1.0_224")

inputs = preprocessor(images=image, return_tensors="pt")

outputs = model(**inputs)
logits = outputs.logits

top_k = 3
probabilities = torch.nn.functional.softmax(logits, dim=-1)
top_k_probs, top_k_indices = torch.topk(probabilities, top_k)

for i in range(top_k):
    predicted_class_idx = top_k_indices[0, i].item()
    probability = top_k_probs[0, i].item()
    predicted_class_label = model.config.id2label[predicted_class_idx]
    print(f"Predicted class {i + 1}: {predicted_class_label} (Probability: {probability:.4f})")


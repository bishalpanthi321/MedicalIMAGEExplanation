from typing import Dict
import torch
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image
import numpy as np
import os

_model = models.resnet18(pretrained=True)
_model.eval()

# Grad-CAM implementation
class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        self.hook_handles = []
        self._register_hooks()

    def _register_hooks(self):
        def forward_hook(module, input, output):
            self.activations = output.detach()
        def backward_hook(module, grad_in, grad_out):
            self.gradients = grad_out[0].detach()
        self.hook_handles.append(self.target_layer.register_forward_hook(forward_hook))
        self.hook_handles.append(self.target_layer.register_backward_hook(backward_hook))

    def __del__(self):
        for handle in self.hook_handles:
            handle.remove()

    def generate(self, input_tensor, class_idx=None):
        output = self.model(input_tensor)
        if class_idx is None:
            class_idx = output.argmax().item()
        self.model.zero_grad()
        loss = output[0, class_idx]
        loss.backward()
        gradients = self.gradients[0]
        activations = self.activations[0]
        weights = gradients.mean(dim=[1, 2], keepdim=True)
        cam = (weights * activations).sum(0)
        cam = F.relu(cam)
        cam = cam - cam.min()
        cam = cam / (cam.max() + 1e-8)
        cam = cam.cpu().numpy()
        return cam

def preprocess_image(image_path: str):
    preprocess = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    img = Image.open(image_path).convert('RGB')
    return preprocess(img).unsqueeze(0)

def save_heatmap(cam: np.ndarray, image_path: str, output_path: str, alpha: float = 0.5):
    import matplotlib.pyplot as plt
    img = Image.open(image_path).resize((224, 224))
    plt.figure(figsize=(3, 3))
    plt.axis('off')
    plt.imshow(img)
    plt.imshow(cam, cmap='jet', alpha=alpha)
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close()

def generate_gradcam(image_path: str) -> Dict:
    # Use the last conv layer for Grad-CAM
    target_layer = _model.layer4[1].conv2
    gradcam = GradCAM(_model, target_layer)
    input_tensor = preprocess_image(image_path)
    cam = gradcam.generate(input_tensor)
    # Save heatmap
    output_dir = os.path.join(os.path.dirname(image_path), 'gradcam')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, os.path.basename(image_path) + '_gradcam.png')
    save_heatmap(cam, image_path, output_path)
    # Return relative path for frontend
    rel_path = output_path.split('static', 1)[-1] if 'static' in output_path else output_path
    return {"heatmap_url": f"/static{rel_path}", "alpha": 0.5}

def generate_shap(image_path: str, class_idx: int = None, num_regions: int = 8) -> Dict:
    """
    Returns the most important regions/features.
    """
    img = Image.open(image_path).convert('RGB').resize((224, 224))
    input_tensor = preprocess_image(image_path)
    with torch.no_grad():
        base_probs = torch.softmax(_model(input_tensor), dim=1).cpu().numpy()[0]
    if class_idx is None:
        class_idx = int(base_probs.argmax())
    base_prob = base_probs[class_idx]

    # Divide image into a grid of regions
    w, h = img.size
    region_size = w // num_regions
    import copy
    import random

    region_importances = []
    for i in range(num_regions):
        for j in range(num_regions):
            masked_img = img.copy()
            # Mask region (i, j) with gray
            x0, y0 = i * region_size, j * region_size
            x1, y1 = min((i+1) * region_size, w), min((j+1) * region_size, h)
            for x in range(x0, x1):
                for y in range(y0, y1):
                    masked_img.putpixel((x, y), (128, 128, 128))
            # Predict with masked image
            masked_tensor = transforms.ToTensor()(masked_img).unsqueeze(0)
            masked_tensor = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])(masked_tensor[0]).unsqueeze(0)
            with torch.no_grad():
                masked_probs = torch.softmax(_model(masked_tensor), dim=1).cpu().numpy()[0]
            masked_prob = masked_probs[class_idx]
            importance = base_prob - masked_prob
            region_importances.append({
                "region": (i, j),
                "importance": float(importance)
            })

    # Sort by importance
    region_importances.sort(key=lambda x: abs(x["importance"]), reverse=True)
    # Return top 5 regions as 'features'
    top_features = [
        {"name": f"region_{r['region']}", "value": r["importance"]}
        for r in region_importances[:5]
    ]
    return {"top_features": top_features}

def generate_counterfactual(image_path: str, target_class: int = None, num_regions: int = 8) -> Dict:
    """
    Returns the region(s) whose change would alter the prediction.
    """
    img = Image.open(image_path).convert('RGB').resize((224, 224))
    input_tensor = preprocess_image(image_path)
    with torch.no_grad():
        base_probs = torch.softmax(_model(input_tensor), dim=1).cpu().numpy()[0]
    base_class = int(base_probs.argmax())
    base_prob = base_probs[base_class]

    if target_class is None:
        # Pick the second most likely class as the counterfactual target
        sorted_indices = np.argsort(base_probs)[::-1]
        target_class = int(sorted_indices[1])

    w, h = img.size
    region_size = w // num_regions

    for i in range(num_regions):
        for j in range(num_regions):
            masked_img = img.copy()
            # Mask region (i, j) with gray
            x0, y0 = i * region_size, j * region_size
            x1, y1 = min((i+1) * region_size, w), min((j+1) * region_size, h)
            for x in range(x0, x1):
                for y in range(y0, y1):
                    masked_img.putpixel((x, y), (128, 128, 128))
            # Predict with masked image
            masked_tensor = transforms.ToTensor()(masked_img).unsqueeze(0)
            masked_tensor = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])(masked_tensor[0]).unsqueeze(0)
            with torch.no_grad():
                masked_probs = torch.softmax(_model(masked_tensor), dim=1).cpu().numpy()[0]
            masked_class = int(masked_probs.argmax())
            if masked_class == target_class:
                return {
                    "description": (
                        f"Masking region ({i},{j}) changes prediction from class {base_class} "
                        f"to class {target_class} (counterfactual)."
                    ),
                    "region": (i, j),
                    "from_class": base_class,
                    "to_class": target_class,
                    "base_prob": float(base_prob),
                    "counterfactual_prob": float(masked_probs[target_class])
                }
    return {
        "description": "No single region found that flips the prediction. Try increasing num_regions or using more advanced methods.",
        "from_class": base_class,
        "to_class": target_class
    }
from typing import Dict

def generate_gradcam_stub(image_path: str) -> Dict:
    return {"heatmap_url": "/static/uploads/gradcam_placeholder.png", "alpha": 0.5}

def generate_shap_stub() -> Dict:
    return {"top_features": [{"name": "opacity", "value": 0.42}, {"name": "edge_density", "value": 0.30}]}

def generate_counterfactual_stub() -> Dict:
    return {"description": "If the opacity area were removed, prediction would shift to 'normal'."}
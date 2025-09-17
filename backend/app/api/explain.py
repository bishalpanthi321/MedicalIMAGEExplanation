from fastapi import APIRouter

router = APIRouter(prefix="/explain", tags=["Explainability"])

@router.get("/gradcam/{scan_id}")
async def gradcam_stub(scan_id: int):
    # Placeholder for Grad-CAM
    return {"scan_id": scan_id, "heatmap": "base64-encoded-image (stub)"}

@router.get("/shap/{scan_id}")
async def shap_stub(scan_id: int):
    # Placeholder for SHAP
    return {"scan_id": scan_id, "shap_values": [0.1, 0.2, 0.3]}

@router.get("/counterfactual/{scan_id}")
async def counterfactual_stub(scan_id: int):
    # Placeholder for counterfactual
    return {"scan_id": scan_id, "counterfactual": "If this opacity wasn’t present... (stub)"}

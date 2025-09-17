from fastapi import APIRouter, UploadFile, File, Form
from app.schemas.predict import PredictRequest, PredictResponse

router = APIRouter(prefix="/predict", tags=["Predict"])

@router.post("/")
async def predict_stub(request: PredictRequest):
    # Placeholder for model inference logic
    return PredictResponse(
        diagnosis="Pneumonia (stub)",
        confidence=0.85,
        explanation="Grad-CAM heatmap (stub)",
        uncertainty=0.12,
        natural_language_report="The scan shows signs of pneumonia. (stub)"
    )

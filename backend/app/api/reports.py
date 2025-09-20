from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Patient, Scan, Prediction
from app.services.nlp import generate_nl_report
from app.services.xai import generate_gradcam, generate_shap, generate_counterfactual

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/{patient_id}")
async def get_report(patient_id: str, db: Session = Depends(get_db)):
    # Lookup patient
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Get latest scan for patient
    scan = db.query(Scan).filter(Scan.patient_id == patient_id).order_by(Scan.created_at.desc()).first()
    if not scan:
        raise HTTPException(status_code=404, detail="No scans found for patient")

    # Get latest prediction for scan
    prediction_obj = db.query(Prediction).filter(Prediction.scan_id == scan.id).order_by(Prediction.created_at.desc()).first()
    if not prediction_obj:
        raise HTTPException(status_code=404, detail="No predictions found for latest scan")

    prediction = prediction_obj.label
    confidence = None
    if prediction_obj.probabilities and isinstance(prediction_obj.probabilities, dict):
        confidence = prediction_obj.probabilities.get(prediction, None)
    if confidence is None:
        confidence = 0.85  # fallback

    # XAI explanations (regenerate for latest scan image)
    image_path = scan.image_path
    gradcam = generate_gradcam(image_path) if image_path else None
    shap = generate_shap(image_path) if image_path else None
    counterfactual = generate_counterfactual(image_path) if image_path else None

    # Patient info
    patient_info = {
        "name": patient.name,
        "age": patient.date_of_birth,
        "sex": patient.sex
    }

    report = generate_nl_report(
        prediction=prediction,
        confidence=confidence,
        gradcam=gradcam,
        shap=shap,
        counterfactual=counterfactual,
        patient_info=patient_info
    )
    return {"patient_id": patient_id, "report": report}
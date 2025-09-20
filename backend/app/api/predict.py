from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.predict import PredictRequest, PredictResponse
from app.services.xai import generate_gradcam, generate_shap, generate_counterfactual
from app.services.nlp import generate_nl_report
from app.models import Scan, Patient
from app.db import get_db

router = APIRouter(prefix="/predict", tags=["Predict"])

@router.post("/", response_model=PredictResponse)
def predict(request: PredictRequest, db: Session = Depends(get_db)):
    # Lookup scan and patient
    scan = db.query(Scan).filter(Scan.id == request.scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    patient = db.query(Patient).filter(Patient.id == scan.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    image_path = scan.image_path
    if not image_path:
        raise HTTPException(status_code=400, detail="No image path for scan")

    # --- Scan type detection ---
    scan_type = getattr(scan, 'scan_type', None) or getattr(scan, 'modality', None)
    if not scan_type:
        # Fallback: guess from file name
        fname = image_path.lower()
        if 'xray' in fname or 'x-ray' in fname or 'cxr' in fname:
            scan_type = 'xray'
        elif 'mri' in fname:
            scan_type = 'mri'
        elif 'ct' in fname:
            scan_type = 'ct'
        else:
            scan_type = 'unknown'

    # --- Disease label sets ---
    XRAY_LABELS = [
        "Normal", "Pneumonia", "Tuberculosis", "COVID-19", "Pulmonary Edema", "Atelectasis", "Cardiomegaly", "Pleural Effusion", "Fibrosis", "Emphysema", "Nodule", "Mass", "Consolidation", "Interstitial Lung Disease", "Bronchiectasis"
    ]
    MRI_LABELS = [
        "Normal", "Glioma", "Meningioma", "Pituitary Tumor", "Stroke", "Multiple Sclerosis", "Alzheimer's", "Parkinson's", "Aneurysm", "Trauma", "Infection", "Hydrocephalus", "Hemorrhage", "Edema", "Demyelination"
    ]
    CT_LABELS = [
        "Normal", "Lung Cancer", "Pulmonary Embolism", "COPD", "Interstitial Lung Disease", "Pneumothorax", "Pleural Effusion", "Aortic Dissection", "Kidney Stone", "Liver Tumor", "Pancreatitis", "Appendicitis", "Colitis", "Abscess", "Metastasis"
    ]

    # --- Model selection and prediction ---
    from app.services.xai import _model, preprocess_image
    import torch
    input_tensor = preprocess_image(image_path)
    
    with torch.no_grad():
        output = _model(input_tensor)
        probs = torch.softmax(output, dim=1)
        confidence_val, class_idx = probs.max(dim=1)
        class_idx = class_idx.item()
        confidence = float(confidence_val.item())

    if scan_type == 'xray':
        labels = XRAY_LABELS
    elif scan_type == 'mri':
        labels = MRI_LABELS
    elif scan_type == 'ct':
        labels = CT_LABELS
    else:
        labels = ["Unknown"]

    prediction = labels[class_idx % len(labels)]

    # XAI explanations
    gradcam = generate_gradcam(image_path)
    shap = generate_shap(image_path)
    counterfactual = generate_counterfactual(image_path)

    # Patient info for report
    patient_info = {
        "name": patient.name,
        "age": patient.date_of_birth,  # Or calculate age if you want
        "sex": patient.sex
    }

    # Natural language report
    nl_report = generate_nl_report(
        prediction=prediction,
        confidence=confidence,
        gradcam=gradcam,
        shap=shap,
        counterfactual=counterfactual,
        patient_info=patient_info
    )

    return PredictResponse(
        diagnosis=prediction,
        confidence=confidence,
        explanation=gradcam["heatmap_url"] if gradcam else None,
        uncertainty=0.12,  # Replace with real uncertainty if available
        natural_language_report=nl_report
    )
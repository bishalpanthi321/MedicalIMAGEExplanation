import uuid as uuid_pkg
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db import get_db
from ... import models, schemas
from ...services import xai as xai_service
from ...services import nlp as nlp_service
from ...auth.deps import require_role

router = APIRouter()

def route_model(body_part: str, modality: str) -> str:
    return f"{modality.lower()}_{body_part.lower()}_model"


@router.post("/predict", response_model=schemas.PredictResponse, dependencies=[Depends(require_role(["clinician","admin","researcher"]))])
def predict(payload: schemas.PredictRequest, db: Session = Depends(get_db)):
    if not payload.scan_id and not payload.image_path:
        raise HTTPException(status_code=400, detail="Provide scan_id or image_path")
    if payload.scan_id:
        scan = db.get(models.Scan, payload.scan_id)
        if not scan:
            raise HTTPException(status_code=404, detail="Scan not found")
        body_part = scan.body_part
        modality = scan.modality
        image_path = scan.image_path or ""
    else:
        body_part = payload.body_part
        modality = payload.modality
        image_path = payload.image_path or ""

    _model_name = route_model(body_part, modality)

    label = "normal"
    probabilities = {"normal": 0.72, "pneumonia": 0.18, "other": 0.10}
    uncertainty = {"softmax_confidence": probabilities.get(label, 0.0), "entropy": 0.85}
    nl_explanation = nlp_service.generate_natural_language_explanation(label)
    xai = {
        "gradcam": xai_service.generate_gradcam_stub(image_path),
        "shap": xai_service.generate_shap_stub(),
        "counterfactual": xai_service.generate_counterfactual_stub(),
    }
    
    
    scan_id = payload.scan_id
    if not scan_id:
        tmp_patient_id = payload.patient_id
        if not tmp_patient_id:
            raise HTTPException(status_code=400, detail="patient_id required when creating scan from image_path")
        scan = models.Scan(
            patient_id=tmp_patient_id,
            body_part=body_part,
            modality=modality,
            image_path=image_path,
        )
        db.add(scan)
        db.commit()
        db.refresh(scan)
        scan_id = scan.id

    pred = models.Prediction(
        scan_id=scan_id,
        label=label,
        probabilities=probabilities,
        uncertainty=uncertainty,
        nl_explanation=nl_explanation,
        xai=xai,
    )
    db.add(pred)
    db.commit()
    db.refresh(pred)

    return {"prediction": schemas.PredictionRead.model_validate(pred)}
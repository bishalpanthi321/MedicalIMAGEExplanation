from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db import get_db
from ... import models
from ...auth.deps import require_role

router = APIRouter()

@router.get("/reports/{patient_id}", dependencies=[Depends(require_role(["clinician","admin","researcher"]))])
def get_report(patient_id: str, db: Session = Depends(get_db)):
    patient = db.get(models.Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {
        "patient": {"id": str(patient.id), "name": patient.name},
        "summary": "Report placeholder. Include predictions and explanations here.",
    }
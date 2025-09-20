from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.patient import PatientCreate, PatientResponse
from app.models import Patient
from app.db import get_db

router = APIRouter(prefix="/patient", tags=["Patient"])

@router.post("/", response_model=PatientResponse)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    db_patient = Patient(
        name=patient.name,
        date_of_birth=getattr(patient, "date_of_birth", None),
        sex=getattr(patient, "sex", None),
        notes=getattr(patient, "notes", None)
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return PatientResponse(
        id=str(db_patient.id),
        name=db_patient.name,
        age=getattr(db_patient, "date_of_birth", None), 
        gender=db_patient.sex
    )

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return PatientResponse(
        id=str(patient.id),
        name=patient.name,
        age=getattr(patient, "date_of_birth", None), 
        gender=patient.sex
    )
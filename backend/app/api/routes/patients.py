from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...db import get_db
from ... import models, schemas
from ...auth.deps import require_role

router = APIRouter()

@router.post("/", response_model=schemas.PatientRead, dependencies=[Depends(require_role(["clinician","admin"]))])
def create_patient(payload: schemas.PatientCreate, db: Session = Depends(get_db)):
    patient = models.Patient(**payload.dict())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

@router.get("/", response_model=List[schemas.PatientRead], dependencies=[Depends(require_role(["clinician","admin","researcher"]))])
def list_patients(db: Session = Depends(get_db)):
    return db.query(models.Patient).order_by(models.Patient.created_at.desc()).all()

@router.get("/{patient_id}", response_model=schemas.PatientRead, dependencies=[Depends(require_role(["clinician","admin","researcher"]))])
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = db.get(models.Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.post("/{patient_id}/scans", response_model=schemas.ScanRead, dependencies=[Depends(require_role(["clinician","admin"]))])
def add_scan(patient_id: str, payload: schemas.ScanCreate, db: Session = Depends(get_db)):
    if not db.get(models.Patient, patient_id):
        raise HTTPException(status_code=404, detail="Patient not found")
    scan = models.Scan(patient_id=patient_id, **payload.dict())
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return scan

@router.get("/{patient_id}/scans", response_model=List[schemas.ScanRead], dependencies=[Depends(require_role(["clinician","admin","researcher"]))])
def list_scans(patient_id: str, db: Session = Depends(get_db)):
    return db.query(models.Scan).filter(models.Scan.patient_id == patient_id).all()
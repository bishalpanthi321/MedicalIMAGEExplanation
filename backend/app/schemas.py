from __future__ import annotations
import uuid
from typing import Dict, Optional
from pydantic import BaseModel

class PatientBase(BaseModel):
    name: str
    date_of_birth: Optional[str] = None
    sex: Optional[str] = None
    notes: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientRead(PatientBase):
    id: uuid.UUID
    class Config:
        from_attributes = True
        
class ScanBase(BaseModel):
    body_part: str
    modality: str
    image_path: Optional[str] = None
    metadata: Optional[dict] = None

class ScanCreate(ScanBase):
    pass

class ScanRead(ScanBase):
    id: uuid.UUID
    patient_id: uuid.UUID
    class Config:
        from_attributes = True

class PredictionBase(BaseModel):
    label: str
    probabilities: Optional[Dict[str, float]] = None
    uncertainty: Optional[Dict[str, float]] = None
    nl_explanation: Optional[str] = None
    xai: Optional[dict] = None
    
class PredictionCreate(PredictionBase):
    scan_id: uuid.UUID

class PredictionRead(PredictionBase):
    id: uuid.UUID
    scan_id: uuid.UUID
    class Config:
        from_attributes = True

class PredictRequest(BaseModel):
    scan_id: Optional[uuid.UUID] = None
    patient_id: Optional[uuid.UUID] = None
    body_part: str
    modality: str
    image_path: Optional[str] = None

class PredictResponse(BaseModel):
    prediction: PredictionRead
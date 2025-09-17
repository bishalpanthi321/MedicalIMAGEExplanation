from pydantic import BaseModel

class PredictRequest(BaseModel):
    patient_id: int
    body_part: str
    modality: str
    image_id: int

class PredictResponse(BaseModel):
    diagnosis: str
    confidence: float
    explanation: str
    uncertainty: float
    natural_language_report: str

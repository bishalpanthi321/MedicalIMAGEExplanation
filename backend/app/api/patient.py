from fastapi import APIRouter
from app.schemas.patient import PatientCreate, PatientResponse

router = APIRouter(prefix="/patient", tags=["Patient"])

@router.post("/")
async def create_patient_stub(patient: PatientCreate):
    # Placeholder for patient creation
    return PatientResponse(id=1, **patient.dict())

@router.get("/{patient_id}")
async def get_patient_stub(patient_id: int):
    # Placeholder for patient retrieval
    return PatientResponse(id=patient_id, name="John Doe", age=40, gender="M")

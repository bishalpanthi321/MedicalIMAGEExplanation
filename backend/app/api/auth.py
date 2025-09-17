from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login_stub():
    # Placeholder for login
    return {"access_token": "fake-jwt-token", "role": "clinician"}

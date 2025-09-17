from fastapi import APIRouter, UploadFile, File

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/image")
async def upload_image_stub(file: UploadFile = File(...)):
    # Placeholder for image upload logic
    return {"filename": file.filename, "status": "uploaded (stub)"}

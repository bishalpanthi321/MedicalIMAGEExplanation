import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

UPLOAD_DIR = "/workspace/backend/app/static/uploads"

@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = os.path.splitext(file.filename)[1]
    if ext.lower() not in [".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".gif", ""]:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    new_name = f"{uuid.uuid4()}{ext if ext else '.png'}"
    saved_path = os.path.join(UPLOAD_DIR, new_name)
    with open(saved_path, "wb") as f:
        f.write(await file.read())
    return JSONResponse({"image_path": saved_path})
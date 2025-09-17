from fastapi import FastAPI
from app.api import predict, patient, upload, explain, auth

app = FastAPI(title="Explainable Medical AI Platform")

app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(predict.router)
app.include_router(patient.router)
app.include_router(explain.router)

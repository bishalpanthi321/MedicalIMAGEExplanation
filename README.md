# README.md
# MedxAI (Scaffold)
## Dev
- Backend: `pip install -r backend/requirements.txt && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` (from backend/)
- Frontend: `npm install && npm run dev` (from frontend/)
- Compose: `docker compose up --build`

## Endpoints
- POST /upload/image
- POST /predict
- Patients CRUD: /patients
- Reports: /reports/{patient_id}

## Notes
- Explainability outputs are placeholders (Grad-CAM, SHAP, counterfactual, NL explanation).
- Role-based access is a simple dependency stub.
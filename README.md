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



This shows the Image upload portal where we can upload the image for X-RAY, CT-SCAN, MRI.
![alt text](<Screenshot 2025-09-19 164629.png>)

Recent Studies
The Recent Studies section lists dummy patient studies with icons, study types, patient names, and dates:

1) Chest X-Ray (Lungs icon): Patient John Doe, Date: 10 Nov 2023.
2) Head MRI (Brain icon): Patient Sarah Wilson, Date: 8 Nov 2023.
3) Cardiac CT (Heart icon): Patient Robert Brown, Date: 5 Nov 2023.

![alt text](<Screenshot 2025-09-19 164645.png>)


AI Analysis Results
The AI Analysis Results page displays pathology confidence scores for various conditions detected in the medical image, with an overall accuracy of 94.3%. The scores are visualized as horizontal bar charts:

- Pneumonia: 92% confidence (longest bar, indicating high likelihood).
- Pulmonary Nodules: 87% confidence.
- Cardiomegaly: 45% confidence.
- Edema: 23% confidence.
- Atelectasis: 15% confidence.
![alt text](<Screenshot 2025-09-19 164737-1.png>)


AI Diagnostic Report
The AI Diagnostic Report summarizes findings, explanations, and recommendations based on the analysis:

    1) Findings: The AI analysis has detected abnormalities consistent with bacterial pneumonia in the right lower lung zone. There are also minor pulmonary nodules present in the upper left lobe that require follow-up.
    2) Explanation: The Grad-CAM heatmap highlights areas of high clinical significance, showing strong activation in the right lower lung field, which correlates with the pneumonia diagnosis. The segmentation model has accurately outlined the lung boundaries and identified the consolidated region.
![alt text](<Screenshot 2025-09-19 164750.png>)

from typing import Dict, Optional

def generate_nl_report(
    prediction: str,
    confidence: float,
    gradcam: Optional[Dict] = None,
    shap: Optional[Dict] = None,
    counterfactual: Optional[Dict] = None,
    patient_info: Optional[Dict] = None
) -> str:
    """
    Generate a natural language report for a model prediction, using XAI outputs.
    """
    report = []

    # Patient context
    if patient_info:
        name = patient_info.get("name", "The patient")
        age = patient_info.get("age", "unknown age")
        sex = patient_info.get("sex", "unknown sex")
        report.append(f"{name}, a {age}-year-old {sex}, underwent imaging analysis.")

    # Main prediction
    report.append(
        f"The model predicts: {prediction} with a confidence of {confidence:.2%}."
    )

    # Grad-CAM explanation
    if gradcam and "heatmap_url" in gradcam:
        report.append(
            "The Grad-CAM heatmap highlights regions in the image that most influenced the model's decision."
        )

    # SHAP explanation
    if shap and "top_features" in shap:
        features = ", ".join(
            f"{f['name']} ({f['value']:.2f})" for f in shap["top_features"]
        )
        report.append(
            f"Key image features contributing to the prediction: {features}."
        )

    # Counterfactual explanation
    if counterfactual and "description" in counterfactual:
        report.append(
            f"Counterfactual analysis: {counterfactual['description']}"
        )

    # Clinical recommendation (template)
    if prediction.lower() in ["pneumonia", "abnormal", "disease"]:
        report.append(
            "Clinical recommendation: Further diagnostic evaluation and clinical correlation are advised."
        )
    else:
        report.append(
            "Clinical recommendation: No immediate abnormal findings detected."
        )

    return " ".join(report)
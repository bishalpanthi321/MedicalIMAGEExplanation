import React from 'react';

export default function ExplainabilityPanel() {
  return (
    <div className="bg-white rounded-card shadow p-6 mt-6">
      <h2 className="text-xl font-semibold mb-2">Explainability</h2>
      <div className="mb-2">Grad-CAM Heatmap (placeholder)</div>
      <div className="mb-2">SHAP Feature Importance (placeholder)</div>
      <div>Counterfactual Explanation (placeholder)</div>
    </div>
  );
}

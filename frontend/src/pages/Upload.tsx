import React from "react";
import * as Tabs from "@radix-ui/react-tabs";
import { uploadImage, predict, addScan, createPatient } from "../api/client";
import FusionPanel from "../components/xai/FusionPanel";

const BODY_PARTS = ["head", "chest", "lungs", "legs", "ribs"];
const MODALITIES = ["X-ray", "MRI", "CT"];

export default function Upload() {
    const [bodyPart, setBodyPart] = React.useState("chest");
    const [modality, setModality] = React.useState("X-ray");
    const [selectedFile, setSelectedFile] = React.useState<File | null>(null);
    const [imagePath, setImagePath] = React.useState<string | null>(null);
    const [result, setResult] = React.useState<any>(null);

    async function handleUploadAndPredict() {
        if (!selectedFile) return;
        const { image_path } = await uploadImage(selectedFile);
        setImagePath(image_path);
        const patient = await createPatient({ name: "Demo Patient" });
        const scan = await addScan(patient.id, { body_part: bodyPart, modality, image_path });
        const res = await predict({ scan_id: scan.id, body_part: bodyPart, modality, image_path });
        setResult(res.prediction);
    }

    return (
        <div className="space-y-6">
            <div className="card p-4">
                <h2 className="font-semibold text-lg mb-3">Upload Scan</h2>
                <div className="mb-4">
                    <Tabs.Root value={bodyPart} onValueChange={setBodyPart}>
                        <Tabs.List className="flex gap-2 mb-3">
                            {BODY_PARTS.map((bp) => (
                                <Tabs.Trigger key={bp} value={bp} className={`px-3 py-1 rounded-md border ${bodyPart === bp ? "bg-primary text-white" : "bg-white"}`}>{bp}</Tabs.Trigger>
                            ))}
                        </Tabs.List>
                    </Tabs.Root>
                    <div className="flex items-center gap-3">
                        <select className="border rounded-md px-2 py-1" value={modality} onChange={(e) => setModality(e.target.value)}>
                            {MODALITIES.map((m) => <option key={m}>{m}</option>)}
                        </select>
                        <input type="file" accept="image/*" onChange={(e) => setSelectedFile(e.target.files?.[0] || null)} />
                        <button className="btn" onClick={handleUploadAndPredict}>Predict</button>
                    </div>
                </div>
                {imagePath && <img src={`http://localhost:8000${imagePath.replace("/workspace/backend/app", "")}`} className="w-64 border rounded-md" />}
            </div>

            {result && (
                <div className="card p-4">
                    <h2 className="font-semibold text-lg mb-3">Results</h2>
                    <div className="mb-3">
                        <div className="text-slate-800">Label: <strong>{result.label}</strong></div>
                        <div className="text-slate-500 text-sm">Confidence: {result.uncertainty?.softmax_confidence?.toFixed(2)}</div>
                    </div>
                    <FusionPanel
                        imageUrl={`http://localhost:8000${(imagePath || "").replace("/workspace/backend/app", "")}`}
                        gradcam={{ heatmapUrl: `http://localhost:8000/static/uploads/gradcam_placeholder.png` }}
                        shap={result.xai?.shap}
                        counterfactual={result.xai?.counterfactual}
                        nl={result.nl_explanation}
                    />
                </div>
            )}
        </div>
    );
}
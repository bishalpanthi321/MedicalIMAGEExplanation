import React from "react";
import GradCamOverlay from "./GradCamOverlay";
import ShapBarPlot from "./ShapBarPlot";
import CounterfactualCard from "./CounterfactualCard";

export default function FusionPanel({
    imageUrl,
    gradcam,
    shap,
    counterfactual,
    nl
}: {
    imageUrl: string;
    gradcam?: { heatmapUrl: string };
    shap?: { top_features: { name: string; value: number }[] };
    counterfactual?: { description: string };
    nl?: string;
}) {
    return (
        <div className="grid md:grid-cols-2 gap-4">
            <div className="space-y-3">
                <GradCamOverlay imageUrl={imageUrl} heatmapUrl={gradcam?.heatmapUrl || imageUrl} />
                <CounterfactualCard description={counterfactual?.description || "N/A"} />
            </div>
            <div className="space-y-3">
                <div className="card p-3">
                    <div className="text-sm text-slate-500 mb-1">Natural Language</div>
                    <div className="text-slate-800">{nl || "No explanation"}</div>
                </div>
                <div className="card p-3">
                    <div className="text-sm text-slate-500 mb-1">SHAP</div>
                    <ShapBarPlot features={shap?.top_features || []} />
                </div>
            </div>
        </div>
    );
}
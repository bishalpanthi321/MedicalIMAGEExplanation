import React from "react";

export default function CounterfactualCard({ description }: { description: string; }) {
    return (
        <div className="card p-3">
            <div className="text-sm text-slate-500 mb-1">Counterfactual</div>
            <div className="text-slate-800">{description}</div>
        </div>
    );
}
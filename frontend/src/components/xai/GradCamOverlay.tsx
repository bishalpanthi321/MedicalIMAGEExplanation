import React from "react";

export default function GradCamOverlay({ imageUrl, heatmapUrl }: { imageUrl: string; heatmapUrl: string; }) {
    return (
        <div className="relative w-full max-w-md">
            <img src={imageUrl} className="w-full rounded-md border" />
            <img src={heatmapUrl} className="w-full absolute inset-0 mix-blend-multiply opacity-60 rounded-md" />
        </div>
    );
}
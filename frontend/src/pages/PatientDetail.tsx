import React from "react";
import { useParams } from "react-router-dom";
import { getReport } from "../api/client";

export default function PatientDetail() {
    const { id } = useParams();
    const [report, setReport] = React.useState<any>(null);

    React.useEffect(() => {
        if (id) getReport(id).then(setReport).catch(() => setReport(null));
    }, [id]);

    return (
        <div className="space-y-4">
            <div className="card p-4">
                <h2 className="font-semibold text-lg mb-2">Patient</h2>
                <div>{report?.patient?.name || "Unknown"}</div>
            </div>
            <div className="card p-4">
                <h2 className="font-semibold text-lg mb-2">Report</h2>
                <pre className="text-sm text-slate-700 whitespace-pre-wrap">{JSON.stringify(report, null, 2)}</pre>
            </div>
        </div>
    );
}
import React from "react";
import { Link } from "react-router-dom";
import { listPatients } from "../api/client";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

export default function Dashboard() {
    const [patients, setPatients] = React.useState<any[]>([]);
    React.useEffect(() => {
        listPatients().then(setPatients).catch(() => setPatients([]));
    }, []);

    const uncertaintyData = [
        { name: "Scan1", entropy: 0.8, confidence: 0.7 },
        { name: "Scan2", entropy: 0.6, confidence: 0.8 },
        { name: "Scan3", entropy: 0.9, confidence: 0.6 }
    ];

    return (
        <div className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
                <div className="card p-4">
                    <h2 className="font-semibold text-lg mb-3">Patients</h2>
                    <ul className="divide-y">
                        {patients.map((p) => (
                            <li key={p.id} className="py-2 flex items-center justify-between">
                                <div>
                                    <div className="font-medium">{p.name}</div>
                                    <div className="text-sm text-slate-500">{p.sex || "Unknown"}</div>
                                </div>
                                <Link to={`/patients/${p.id}`} className="btn">Open</Link>
                            </li>
                        ))}
                        {patients.length === 0 && <li className="py-2 text-slate-500">No patients yet.</li>}
                    </ul>
                </div>
                <div className="card p-4">
                    <h2 className="font-semibold text-lg mb-3">Uncertainty Overview</h2>
                    <div className="h-56">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={uncertaintyData}>
                                <defs>
                                    <linearGradient id="colA" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#1e40af" stopOpacity={0.8} />
                                        <stop offset="95%" stopColor="#1e40af" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="name" />
                                <YAxis domain={[0, 1]} />
                                <Tooltip />
                                <Area type="monotone" dataKey="entropy" stroke="#1e40af" fillOpacity={1} fill="url(#colA)" />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>
        </div>
    );
}
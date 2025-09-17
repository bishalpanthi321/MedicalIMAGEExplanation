import React from 'react';

export default function Dashboard() {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-4">Medical xAI Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="rounded-card bg-white shadow p-6">Patient Management (placeholder)</div>
        <div className="rounded-card bg-white shadow p-6">Bias & Audit Dashboard (placeholder)</div>
      </div>
    </div>
  );
}

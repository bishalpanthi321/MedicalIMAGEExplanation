import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Upload from './pages/Upload';
import Patient from './pages/Patient';
import BiasAudit from './pages/BiasAudit';

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/dashboard" />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/upload" element={<Upload />} />
      <Route path="/patient/:id" element={<Patient />} />
      <Route path="/bias-audit" element={<BiasAudit />} />
    </Routes>
  );
}

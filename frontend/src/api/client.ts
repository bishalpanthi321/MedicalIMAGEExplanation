import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export const api = axios.create({ baseURL: API_BASE });

export async function uploadImage(file: File): Promise<{ image_path: string }> {
    const form = new FormData();
    form.append("file", file);
    const { data } = await api.post("/upload/image", form, { headers: { "Content-Type": "multipart/form-data" } });
    return data;
}

export async function createPatient(payload: { name: string; date_of_birth?: string; sex?: string; notes?: string; }) {
    const { data } = await api.post("/patients/", payload);
    return data;
}

export async function listPatients() {
    const { data } = await api.get("/patients/");
    return data;
}

export async function addScan(patientId: string, payload: { body_part: string; modality: string; image_path?: string; metadata?: Record<string, unknown>; }) {
    const { data } = await api.post(`/patients/${patientId}/scans`, payload);
    return data;
}

export async function predict(payload: { scan_id?: string; patient_id?: string; body_part: string; modality: string; image_path?: string; }) {
    const { data } = await api.post("/predict", payload);
    return data;
}

export async function getReport(patientId: string) {
    const { data } = await api.get(`/reports/${patientId}`);
    return data;
}
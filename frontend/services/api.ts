import axios from "axios";
import type {
  UploadResponse,
  FullAnalysisResponse,
} from "@/types/api";

const api = axios.create({
  baseURL:
    process.env.NEXT_PUBLIC_API_URL ||
    "https://abdelsalam-1-ai-data-dashboard-api.hf.space",
});

export async function uploadDataset(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const res = await api.post<UploadResponse>("/api/upload_dataset", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
}

export async function runFullAnalysis(): Promise<FullAnalysisResponse> {
  const res = await api.post<FullAnalysisResponse>("/api/full_analysis");
  return res.data;
}


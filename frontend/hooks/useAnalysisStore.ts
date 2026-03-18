"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";
import type {
  FullAnalysisResponse,
  DatasetSummary,
  CorrelationResponse,
  AnomalyResponse,
  AIInsightsResponse,
  HistogramBin,
} from "@/types/api";

interface AnalysisState {
  datasetName: string | null;
  summary: DatasetSummary | null;
  correlation: CorrelationResponse | null;
  anomalies: AnomalyResponse | null;
  insights: AIInsightsResponse | null;
  distributions: Record<string, HistogramBin[]> | null;
  loading: boolean;
  uploading: boolean;
  error: string | null;
  darkMode: boolean;

  setDatasetName: (name: string | null) => void;
  setLoading: (v: boolean) => void;
  setUploading: (v: boolean) => void;
  setError: (msg: string | null) => void;
  applyAnalysis: (payload: FullAnalysisResponse) => void;
  setDarkMode: (v: boolean) => void;
  clear: () => void;
}

export const useAnalysisStore = create<AnalysisState>()(
  persist(
    (set) => ({
      datasetName: null,
      summary: null,
      correlation: null,
      anomalies: null,
      insights: null,
      distributions: null,
      loading: false,
      uploading: false,
      error: null,
      darkMode: false,

      setDatasetName: (name) => set({ datasetName: name }),
      setLoading: (v) => set({ loading: v }),
      setUploading: (v) => set({ uploading: v }),
      setError: (msg) => set({ error: msg }),
      applyAnalysis: (payload) =>
        set({
          summary: payload.summary,
          correlation: payload.correlation,
          anomalies: payload.anomalies,
          insights: payload.insights,
          distributions: payload.distributions ?? null,
        }),
      setDarkMode: (v) => set({ darkMode: v }),
      clear: () =>
        set({
          datasetName: null,
          summary: null,
          correlation: null,
          anomalies: null,
          insights: null,
          distributions: null,
          error: null,
        }),
    }),
    {
      name: "ai-data-analysis-store",
      partialize: (state) => ({
        datasetName: state.datasetName,
        summary: state.summary,
        correlation: state.correlation,
        anomalies: state.anomalies,
        insights: state.insights,
        distributions: state.distributions,
        darkMode: state.darkMode,
      }),
    }
  )
);


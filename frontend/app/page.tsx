"use client";

import { useState } from "react";
import { SummaryCard } from "@/components/dashboard/SummaryCard";
import { CorrelationCard } from "@/components/dashboard/CorrelationCard";
import { DistributionCard } from "@/components/dashboard/DistributionCard";
import { AnomalyCard } from "@/components/dashboard/AnomalyCard";
import { AIInsightsPanel } from "@/components/dashboard/AIInsightsPanel";
import { useAnalysisStore } from "@/hooks/useAnalysisStore";
import { uploadDataset, runFullAnalysis } from "@/services/api";
import { DownloadReportButton } from "@/components/dashboard/DownloadReportButton";

export default function HomePage() {
  const [file, setFile] = useState<File | null>(null);
  const {
    datasetName,
    summary,
    correlation,
    anomalies,
    insights,
    loading,
    uploading,
    error,
    setDatasetName,
    setLoading,
    setUploading,
    setError,
    applyAnalysis,
  } = useAnalysisStore();

  const handleUpload = async () => {
    if (!file) return;
    setError(null);
    setUploading(true);
    try {
      const res = await uploadDataset(file);
      setDatasetName(res.filename);
    } catch (e: any) {
      const msg = e.response?.data?.detail ?? "Failed to upload dataset.";
      setError(msg);
    } finally {
      setUploading(false);
    }
  };

  const handleAnalyze = async () => {
    setError(null);
    setLoading(true);
    try {
      const result = await runFullAnalysis();
      applyAnalysis(result);
      if (result.dataset_name) {
        setDatasetName(result.dataset_name);
      }
    } catch (e: any) {
      const msg = e.response?.data?.detail ?? "Failed to run full analysis.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container mx-auto max-w-6xl p-4 sm:p-6 lg:p-8">
      <header className="mb-8 flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">
            AI Data Analysis Dashboard
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Upload a CSV or Excel file to get started.
          </p>
        </div>
        <DownloadReportButton />
      </header>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Left column: Upload and Summary */}
        <div className="space-y-6 lg:col-span-1">
          <section
            id="upload-section"
            className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900"
          >
            <h2 className="mb-4 text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
              Dataset upload
            </h2>
            <div className="space-y-4">
              <div>
                <input
                  type="file"
                  accept=".csv,.xlsx,.xls"
                  onChange={(e) => setFile(e.target.files?.[0] ?? null)}
                  className="w-full text-sm text-slate-500 file:mr-4 file:rounded-md file:border-0 file:bg-slate-100 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-slate-700 hover:file:bg-slate-200 dark:text-slate-400 dark:file:bg-slate-800 dark:file:text-slate-300"
                />
              </div>
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={handleUpload}
                  disabled={!file || uploading}
                  className="flex-1 rounded-md bg-slate-900 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-slate-50 dark:text-slate-900 dark:hover:bg-slate-200"
                >
                  {uploading ? "Uploading..." : "Upload"}
                </button>
                <button
                  type="button"
                  onClick={handleAnalyze}
                  disabled={loading || !datasetName}
                  className="flex-1 rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {loading ? "Analyzing..." : "Run analysis"}
                </button>
              </div>

              {error && (
                <p className="text-xs font-medium text-red-600 dark:text-red-400">
                  {error}
                </p>
              )}

              {datasetName && !error && (
                <p className="text-xs font-medium text-emerald-600 dark:text-emerald-400">
                  Active dataset: {datasetName}
                </p>
              )}
            </div>
          </section>

          <SummaryCard summary={summary} datasetName={datasetName} />

          <AnomalyCard anomalies={anomalies} />
        </div>

        {/* Right column: Charts and Insights */}
        <div className="space-y-6 lg:col-span-2">
          <CorrelationCard correlation={correlation} />

          <DistributionCard summary={summary} distributions={undefined} />

          <AIInsightsPanel insights={insights} />
        </div>
      </div>
    </main>
  );
}

"use client";

import { useState } from "react";
import { useAnalysisStore } from "@/hooks/useAnalysisStore";
import { downloadJSONReport, downloadPDFReport } from "@/services/reportService";

export function DownloadReportButton() {
  const { summary, correlation, anomalies, insights, datasetName } =
    useAnalysisStore();
  const [open, setOpen] = useState(false);
  const [generating, setGenerating] = useState<"json" | "pdf" | null>(null);
  const hasAnalysis = !!(summary && correlation && anomalies && insights);

  const handleDownloadJson = async () => {
    if (!hasAnalysis) return;
    setGenerating("json");
    try {
      downloadJSONReport({
        dataset_name: datasetName || "dataset",
        summary: summary!,
        correlation: correlation!,
        anomalies: anomalies!,
        insights: insights!,
      } as Parameters<typeof downloadJSONReport>[0]);
    } finally {
      setGenerating(null);
      setOpen(false);
    }
  };

  const handleDownloadPdf = async () => {
    if (!hasAnalysis) return;
    setGenerating("pdf");
    try {
      await downloadPDFReport({
        dataset_name: datasetName || "dataset",
        summary: summary!,
        correlation: correlation!,
        anomalies: anomalies!,
        insights: insights!,
      } as Parameters<typeof downloadPDFReport>[0]);
    } finally {
      setGenerating(null);
      setOpen(false);
    }
  };

  return (
    <div className="relative inline-block text-left">
      <button
        type="button"
        disabled={!hasAnalysis || !!generating}
        onClick={() => setOpen((v) => !v)}
        className="inline-flex items-center gap-1 rounded-md border border-slate-300 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 shadow-sm hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:hover:bg-slate-800"
      >
        {generating ? "Generating report..." : "Download report"}
        <span className="text-[10px]">▾</span>
      </button>
      {open && (
        <div className="absolute right-0 z-20 mt-1 w-40 rounded-md border border-slate-200 bg-white py-1 text-xs shadow-lg dark:border-slate-700 dark:bg-slate-900">
          <button
            type="button"
            onClick={handleDownloadJson}
            disabled={!!generating}
            className="flex w-full items-center justify-between px-3 py-1.5 text-left text-slate-700 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60 dark:text-slate-100 dark:hover:bg-slate-800"
          >
            <span>JSON</span>
          </button>
          <button
            type="button"
            onClick={handleDownloadPdf}
            disabled={!!generating}
            className="flex w-full items-center justify-between px-3 py-1.5 text-left text-slate-700 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60 dark:text-slate-100 dark:hover:bg-slate-800"
          >
            <span>PDF</span>
          </button>
        </div>
      )}
    </div>
  );
}


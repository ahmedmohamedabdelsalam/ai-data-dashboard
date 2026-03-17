import type { FullAnalysisResponse } from "@/types/api";
import { generatePdfReport } from "@/utils/pdfReportGenerator";

function getSafeDatasetName(data: FullAnalysisResponse | null): string {
  const base = data?.dataset_name || "dataset";
  return base.replace(/[^a-z0-9-_]+/gi, "_").toLowerCase();
}

export function downloadJSONReport(data: FullAnalysisResponse | null): void {
  if (!data) {
    return;
  }

  const safeName = getSafeDatasetName(data);
  const json = JSON.stringify(data, null, 2);
  const blob = new Blob([json], { type: "application/json" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = `analysis-report-${safeName}.json`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

export async function downloadPDFReport(
  data: FullAnalysisResponse | null
): Promise<void> {
  if (!data) return;
  await generatePdfReport(data);
}


import jsPDF from "jspdf";
import html2canvas from "html2canvas";
import type { FullAnalysisResponse } from "@/types/api";

const PAGE_MARGIN = 20;

async function captureElement(id: string): Promise<HTMLCanvasElement | null> {
  const el = document.getElementById(id);
  if (!el) return null;
  try {
    return await html2canvas(el, {
      backgroundColor: null,
      scale: 2,
      useCORS: true,
    });
  } catch {
    return null;
  }
}

export async function generatePdfReport(
  data: FullAnalysisResponse
): Promise<void> {
  const doc = new jsPDF({
    orientation: "portrait",
    unit: "pt",
    format: "a4",
  });

  const pageWidth = doc.internal.pageSize.getWidth();
  const pageHeight = doc.internal.pageSize.getHeight();

  const datasetName = data.dataset_name || "Dataset";
  const createdAt = new Date().toLocaleString();

  // Title page
  doc.setFont("helvetica", "bold");
  doc.setFontSize(22);
  doc.text("AI Data Analysis Report", pageWidth / 2, 150, {
    align: "center",
  });

  doc.setFontSize(14);
  doc.setFont("helvetica", "normal");
  doc.text(`Dataset: ${datasetName}`, pageWidth / 2, 190, {
    align: "center",
  });

  doc.setFontSize(11);
  doc.text(`Generated: ${createdAt}`, pageWidth / 2, 215, {
    align: "center",
  });

  // Section 1 — Dataset summary
  doc.addPage();
  let y = PAGE_MARGIN;
  doc.setFont("helvetica", "bold");
  doc.setFontSize(16);
  doc.text("Section 1 — Dataset Summary", PAGE_MARGIN, y);
  y += 24;

  doc.setFont("helvetica", "normal");
  doc.setFontSize(11);
  const { summary } = data;
  const missingTotal =
    summary.column_info.reduce((acc, c) => acc + c.missing_count, 0) || 0;
  const lines = [
    `Rows: ${summary.rows}`,
    `Columns: ${summary.columns}`,
    `Total missing values: ${missingTotal}`,
    `Memory usage (MB): ${
      summary.memory_usage_mb != null
        ? summary.memory_usage_mb.toFixed(2)
        : "n/a"
    }`,
  ];
  lines.forEach((line) => {
    doc.text(line, PAGE_MARGIN, y);
    y += 16;
  });

  // Section 2 — Correlation analysis
  doc.addPage();
  y = PAGE_MARGIN;
  doc.setFont("helvetica", "bold");
  doc.setFontSize(16);
  doc.text("Section 2 — Correlation Analysis", PAGE_MARGIN, y);
  y += 20;

  const corrCanvas = await captureElement("correlation-card");
  if (corrCanvas) {
    const imgData = corrCanvas.toDataURL("image/png");
    const imgWidth = pageWidth - PAGE_MARGIN * 2;
    const imgHeight = (corrCanvas.height * imgWidth) / corrCanvas.width;
    doc.addImage(
      imgData,
      "PNG",
      PAGE_MARGIN,
      y,
      imgWidth,
      Math.min(imgHeight, pageHeight - PAGE_MARGIN - y)
    );
  } else {
    doc.setFontSize(11);
    doc.text(
      "Correlation heatmap not available (component not rendered).",
      PAGE_MARGIN,
      y
    );
  }

  // Section 3 — Distribution analysis
  doc.addPage();
  y = PAGE_MARGIN;
  doc.setFont("helvetica", "bold");
  doc.setFontSize(16);
  doc.text("Section 3 — Distribution Analysis", PAGE_MARGIN, y);
  y += 20;

  const distCanvas = await captureElement("distribution-card");
  if (distCanvas) {
    const imgData = distCanvas.toDataURL("image/png");
    const imgWidth = pageWidth - PAGE_MARGIN * 2;
    const imgHeight = (distCanvas.height * imgWidth) / distCanvas.width;
    doc.addImage(
      imgData,
      "PNG",
      PAGE_MARGIN,
      y,
      imgWidth,
      Math.min(imgHeight, pageHeight - PAGE_MARGIN - y)
    );
  } else {
    doc.setFontSize(11);
    doc.text(
      "Distribution chart not available (component not rendered).",
      PAGE_MARGIN,
      y
    );
  }

  // Section 4 — Anomaly detection
  doc.addPage();
  y = PAGE_MARGIN;
  doc.setFont("helvetica", "bold");
  doc.setFontSize(16);
  doc.text("Section 4 — Anomaly Detection", PAGE_MARGIN, y);
  y += 22;

  const { anomalies } = data;
  doc.setFont("helvetica", "normal");
  doc.setFontSize(11);

  const rate =
    anomalies.n_total > 0
      ? ((anomalies.n_anomalies / anomalies.n_total) * 100).toFixed(2)
      : "0.00";

  const anomalyLines = [
    `Total records: ${anomalies.n_total}`,
    `Anomalies: ${anomalies.n_anomalies}`,
    `Anomaly rate: ${rate}%`,
  ];
  anomalyLines.forEach((line) => {
    doc.text(line, PAGE_MARGIN, y);
    y += 16;
  });

  y += 8;
  doc.setFont("helvetica", "bold");
  doc.text("Top anomalies (index, score)", PAGE_MARGIN, y);
  y += 16;

  doc.setFont("helvetica", "normal");
  const top = anomalies.records?.slice(0, 10) || [];
  top.forEach((r) => {
    const line = `Index: ${r.index}, Score: ${r.score.toFixed(3)}`;
    if (y > pageHeight - PAGE_MARGIN) {
      doc.addPage();
      y = PAGE_MARGIN;
    }
    doc.text(line, PAGE_MARGIN, y);
    y += 14;
  });

  // Section 5 — AI Insights
  doc.addPage();
  y = PAGE_MARGIN;
  doc.setFont("helvetica", "bold");
  doc.setFontSize(16);
  doc.text("Section 5 — AI Insights", PAGE_MARGIN, y);
  y += 22;

  doc.setFont("helvetica", "normal");
  doc.setFontSize(11);
  const { insights } = data;

  if (!insights) {
    doc.text("No AI insights available.", PAGE_MARGIN, y);
  } else {
    const text = insights.report || insights.summary;
    const paragraphs = text.split(/\n{2,}/);

    paragraphs.forEach((p) => {
      const wrapped = doc.splitTextToSize(p, pageWidth - PAGE_MARGIN * 2);
      if (y + wrapped.length * 14 > pageHeight - PAGE_MARGIN) {
        doc.addPage();
        y = PAGE_MARGIN;
      }
      doc.text(wrapped, PAGE_MARGIN, y);
      y += wrapped.length * 14 + 8;
    });
  }

  const safeName = (data.dataset_name || "dataset")
    .replace(/[^a-z0-9-_]+/gi, "_")
    .toLowerCase();
  doc.save(`analysis-report-${safeName}.pdf`);
}


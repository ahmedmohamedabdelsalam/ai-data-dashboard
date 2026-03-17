"use client";

import type { DatasetSummary } from "@/types/api";
import { Card } from "@/components/ui/Card";

interface SummaryCardProps {
  summary: DatasetSummary | null;
  datasetName: string | null;
}

export function SummaryCard({ summary, datasetName }: SummaryCardProps) {
  return (
    <div id="summary-card">
      <Card title="Dataset summary">
      {!summary ? (
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Upload a dataset and run analysis to see summary statistics.
        </p>
      ) : (
        <div className="space-y-3 text-sm">
          {datasetName && (
            <p className="truncate text-xs text-slate-500 dark:text-slate-400">
              <span className="font-medium text-slate-700 dark:text-slate-200">
                File:
              </span>{" "}
              {datasetName}
            </p>
          )}
          <div className="grid grid-cols-3 gap-3">
            <div className="rounded-lg bg-slate-50 p-3 text-center dark:bg-slate-950/60">
              <p className="text-[11px] uppercase tracking-wide text-slate-500 dark:text-slate-400">
                Rows
              </p>
              <p className="mt-1 text-lg font-semibold">{summary.rows}</p>
            </div>
            <div className="rounded-lg bg-slate-50 p-3 text-center dark:bg-slate-950/60">
              <p className="text-[11px] uppercase tracking-wide text-slate-500 dark:text-slate-400">
                Columns
              </p>
              <p className="mt-1 text-lg font-semibold">{summary.columns}</p>
            </div>
            <div className="rounded-lg bg-slate-50 p-3 text-center dark:bg-slate-950/60">
              <p className="text-[11px] uppercase tracking-wide text-slate-500 dark:text-slate-400">
                Memory (MB)
              </p>
              <p className="mt-1 text-lg font-semibold">
                {summary.memory_usage_mb?.toFixed(2) ?? "-"}
              </p>
            </div>
          </div>
        </div>
      )}
    </Card>
    </div>
  );
}

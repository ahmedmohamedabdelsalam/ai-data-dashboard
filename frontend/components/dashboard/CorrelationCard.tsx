"use client";

import React, { useMemo } from "react";
import { Card } from "@/components/ui/Card";
import type { CorrelationResponse } from "@/types/api";

interface CorrelationCardProps {
  correlation: CorrelationResponse | null;
}

function getColor(value: number): string {
  // value in [-1, 1] → blue (negative) to white to red (positive)
  if (Number.isNaN(value)) return "bg-slate-200 dark:bg-slate-700";
  const v = Math.max(-1, Math.min(1, value));
  if (v > 0) {
    const intensity = Math.round(v * 500);
    if (intensity > 350) return "bg-red-600";
    if (intensity > 200) return "bg-red-500";
    return "bg-red-400";
  }
  if (v < 0) {
    const intensity = Math.round(-v * 500);
    if (intensity > 350) return "bg-blue-700";
    if (intensity > 200) return "bg-blue-600";
    return "bg-blue-500";
  }
  return "bg-slate-200 dark:bg-slate-700";
}

export function CorrelationCard({ correlation }: CorrelationCardProps) {
  const { matrix, cols } = useMemo(() => {
    if (!correlation || !correlation.numeric_columns.length) {
      return { matrix: [] as number[][], cols: [] as string[] };
    }
    const cols = correlation.numeric_columns;
    const matrix = cols.map((row) =>
      cols.map((col) => correlation.correlation_matrix[row]?.[col] ?? 0)
    );
    return { matrix, cols };
  }, [correlation]);

  return (
    <div id="correlation-card">
      <Card title="Correlation heatmap">
      {!cols.length || !matrix.length ? (
        <p className="text-sm text-slate-500 dark:text-slate-400">
          No numeric columns or correlation matrix is empty.
        </p>
      ) : (
        <div className="space-y-3">
          <div className="overflow-auto">
            <div
              className="inline-grid border border-slate-200 dark:border-slate-700"
              style={{
                gridTemplateColumns: `max-content repeat(${cols.length}, minmax(2rem, 1fr))`,
              }}
            >
              <div className="sticky left-0 z-10 bg-slate-50 px-2 py-1 text-xs font-medium text-slate-500 dark:bg-slate-900 dark:text-slate-400">
                {/* corner */}
              </div>
              {cols.map((col) => (
                <div
                  key={col}
                  className="px-2 py-1 text-xs font-medium text-slate-600 dark:text-slate-300"
                >
                  {col}
                </div>
              ))}

              {cols.map((rowName, i) => (
                <React.Fragment key={rowName}>
                  <div className="sticky left-0 z-10 bg-slate-50 px-2 py-1 text-xs font-medium text-slate-600 dark:bg-slate-900 dark:text-slate-300">
                    {rowName}
                  </div>
                  {matrix[i].map((value, j) => (
                    <div
                      key={`${rowName}-${cols[j]}`}
                      className={`flex items-center justify-center px-1 py-1 text-[10px] font-medium text-white ${getColor(
                        value
                      )}`}
                    >
                      {value.toFixed(2)}
                    </div>
                  ))}
                </React.Fragment>
              ))}
            </div>
          </div>
          <p className="text-[11px] text-slate-500 dark:text-slate-400">
            Strong positive correlations are shown in red, negative in blue.
          </p>
        </div>
      )}
    </Card>
    </div>
  );
}

"use client";

import React, { useMemo, useState } from "react";

import type { DatasetSummary, HistogramBin } from "@/types/api";
import { Card } from "@/components/ui/Card";

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";

interface DistributionCardProps {
  summary: DatasetSummary | null;
  distributions?: Record<string, HistogramBin[]> | null;
}



export function DistributionCard({ summary, distributions }: DistributionCardProps) {
  const numericColumns = useMemo(() => {
    if (!summary?.column_info?.length) return [] as string[];
    return summary.column_info
      .filter((c) => c.dtype.startsWith("int") || c.dtype.startsWith("float"))
      .map((c) => c.name);
  }, [summary]);

  const [selected, setSelected] = useState<string | null>(
    () => numericColumns[0] ?? null
  );

  const histogramData: HistogramBin[] = useMemo(() => {
    if (!selected || !distributions) return [];
    return distributions[selected] ?? [];
  }, [selected, distributions]);

  const handleSelect = (value: string) => {
    setSelected(value);
  };

  return (
    <div id="distribution-card">
      <Card title="Distribution (numeric column)">
      {!numericColumns.length ? (
        <p className="text-sm text-slate-500 dark:text-slate-400">
          No numeric columns detected in the summary.
        </p>
      ) : (
        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <label className="text-xs font-medium text-slate-600 dark:text-slate-300">
              Column
            </label>
            <select
              value={selected ?? numericColumns[0]}
              onChange={(e) => handleSelect(e.target.value)}
              className="rounded-md border border-slate-300 bg-white px-2 py-1 text-xs text-slate-800 shadow-sm focus:border-slate-500 focus:outline-none focus:ring-1 focus:ring-slate-500 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100"
            >
              {numericColumns.map((col) => (
                <option key={col} value={col}>
                  {col}
                </option>
              ))}
            </select>
          </div>

          {!histogramData.length ? (
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Histogram data will appear here once raw values are wired from
              the backend or a client-side fetch. The component is ready for
              integration with Recharts.
            </p>
          ) : (
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={histogramData}>
                  <XAxis dataKey="bin" hide />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="count" fill="#0f172a" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>
      )}
    </Card>
    </div>
  );
}

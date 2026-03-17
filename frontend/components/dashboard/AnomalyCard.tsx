"use client";

import type { AnomalyResponse } from "@/types/api";
import { Card } from "@/components/ui/Card";

interface AnomalyCardProps {
  anomalies: AnomalyResponse | null;
}

export function AnomalyCard({ anomalies }: AnomalyCardProps) {
  if (!anomalies) {
    return (
      <div id="anomaly-card">
        <Card title="Anomaly detection">
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Anomalies will appear here after analysis.
        </p>
      </Card>
      </div>
    );
  }

  const rate =
    anomalies.n_total > 0
      ? ((anomalies.n_anomalies / anomalies.n_total) * 100).toFixed(2)
      : "0.00";

  const topRecords = anomalies.records?.slice(0, 5) ?? [];

  return (
    <div id="anomaly-card">
      <Card title="Anomaly detection">
      <div className="space-y-3 text-sm">
        <div className="flex items-center justify-between gap-4">
          <div>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Total records
            </p>
            <p className="text-lg font-semibold">{anomalies.n_total}</p>
          </div>
          <div>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Anomalies
            </p>
            <p className="text-lg font-semibold text-red-600 dark:text-red-400">
              {anomalies.n_anomalies}
            </p>
          </div>
          <div>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Rate
            </p>
            <p className="text-lg font-semibold">{rate}%</p>
          </div>
        </div>

        {topRecords.length > 0 && (
          <div className="mt-2 rounded-lg border border-red-100 bg-red-50/50 p-2 text-xs dark:border-red-900/60 dark:bg-red-950/40">
            <p className="mb-1 font-medium text-red-700 dark:text-red-200">
              Top anomalies
            </p>
            <div className="max-h-40 overflow-auto">
              <table className="w-full text-xs">
                <thead>
                  <tr className="text-left text-[11px] uppercase tracking-wide text-red-700/80 dark:text-red-200/80">
                    <th className="px-1 py-1">Index</th>
                    <th className="px-1 py-1">Score</th>
                  </tr>
                </thead>
                <tbody>
                  {topRecords.map((r) => (
                    <tr
                      key={r.index}
                      className="border-t border-red-100/70 bg-red-50/60 last:border-b dark:border-red-900/60 dark:bg-red-950/40"
                    >
                      <td className="px-1 py-1">{r.index}</td>
                      <td className="px-1 py-1">{r.score.toFixed(3)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </Card>
    </div>
  );
}

"use client";

import { useState } from "react";
import type { AIInsightsResponse } from "@/types/api";
import { Card } from "@/components/ui/Card";

interface AIInsightsPanelProps {
  insights: AIInsightsResponse | null;
}

export function AIInsightsPanel({ insights }: AIInsightsPanelProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    if (!insights) return;
    try {
      await navigator.clipboard.writeText(insights.report);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      // ignore
    }
  };

  return (
    <div id="insights-panel">
      <Card
        title="AI insights"
        headerRight={
        <button
          type="button"
          disabled={!insights}
          onClick={handleCopy}
          className="text-xs font-medium text-slate-600 underline-offset-2 hover:underline disabled:cursor-not-allowed disabled:text-slate-400 dark:text-slate-300 dark:disabled:text-slate-500"
        >
          {copied ? "Copied" : "Copy to clipboard"}
        </button>
      }
    >
      {!insights ? (
        <p className="text-sm text-slate-500 dark:text-slate-400">
          AI-generated narrative report will appear here after full analysis
          (requires backend LLM configuration).
        </p>
      ) : (
        <div className="space-y-3 text-sm">
          <p className="font-semibold text-slate-900 dark:text-slate-50">
            {insights.summary}
          </p>
          <div className="space-y-2">
            {insights.report.split(/\n{2,}/).map((block, idx) => (
              <p key={idx} className="whitespace-pre-wrap text-sm leading-relaxed">
                {block}
              </p>
            ))}
          </div>
        </div>
      )}
    </Card>
    </div>
  );
}

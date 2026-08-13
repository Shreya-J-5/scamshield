import React from 'react';
import RiskScoreGauge from './RiskScoreGauge';
import RiskBadge from './RiskBadge';
import { ArrowLeft, Clock } from 'lucide-react';

export default function ResultCard({ result, onReset }) {
  if (!result) return null;

  const { risk_score, risk_level, verdict, red_flags, recommendation, processing_time_ms } = result;

  return (
    <div className="bg-[#121215] rounded-xl p-6 border border-zinc-800 space-y-6">
      {/* Header & Gauge */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6 pb-6 border-b border-zinc-800/80">
        <div className="space-y-2 max-w-lg">
          <div className="flex items-center space-x-2.5">
            <RiskBadge level={risk_level} />
            <span className="text-[11px] text-zinc-500 font-mono flex items-center gap-1">
              <Clock className="w-3 h-3" /> {processing_time_ms} ms
            </span>
          </div>
          <h2 className="text-xl sm:text-2xl font-semibold text-white tracking-tight">
            Verdict: <span className="text-zinc-200">{verdict}</span>
          </h2>
          <p className="text-xs text-zinc-400 leading-relaxed">
            {recommendation}
          </p>
        </div>

        <div className="flex-shrink-0 self-center sm:self-auto">
          <RiskScoreGauge score={risk_score} level={risk_level} />
        </div>
      </div>

      {/* Red Flags / Risk Indicators */}
      <div className="space-y-3">
        <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-400">
          Detected Red Flags ({red_flags.length})
        </h3>

        {red_flags.length === 0 ? (
          <div className="p-4 rounded-lg bg-zinc-900/50 border border-zinc-800 text-emerald-400 text-xs font-medium">
            No suspicious patterns or indicators were detected.
          </div>
        ) : (
          <div className="space-y-2">
            {red_flags.map((flag, idx) => (
              <div
                key={idx}
                className="p-3.5 rounded-lg bg-zinc-900/60 border border-zinc-800/80 space-y-1.5"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-zinc-200">
                    {flag.rule}
                  </span>
                  <span className="text-[10px] font-mono text-rose-400 bg-rose-950/40 px-2 py-0.5 rounded border border-rose-900/40">
                    +{flag.points} pts
                  </span>
                </div>
                <p className="text-xs text-zinc-400">{flag.explanation}</p>
                {flag.evidence && (
                  <div className="text-[11px] font-mono text-zinc-500 bg-zinc-950/80 px-2.5 py-1 rounded border border-zinc-900">
                    Evidence: {flag.evidence}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer Disclaimer & Reset */}
      <div className="pt-4 border-t border-zinc-800/80 flex flex-col sm:flex-row items-center justify-between gap-3">
        <p className="text-[11px] text-zinc-500">
          * ScamShield provides risk indicators and cannot guarantee 100% detection.
        </p>
        <button
          onClick={onReset}
          className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-zinc-900 hover:bg-zinc-800 text-zinc-300 border border-zinc-700 text-xs font-medium transition-all"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Analyze Another Message</span>
        </button>
      </div>
    </div>
  );
}

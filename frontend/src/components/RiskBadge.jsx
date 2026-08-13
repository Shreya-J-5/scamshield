import React from 'react';

export default function RiskBadge({ level }) {
  const styles = {
    Low: 'bg-emerald-950/60 text-emerald-400 border-emerald-800/50',
    Suspicious: 'bg-amber-950/60 text-amber-400 border-amber-800/50',
    High: 'bg-orange-950/60 text-orange-400 border-orange-800/50',
    Critical: 'bg-rose-950/60 text-rose-400 border-rose-800/50',
  };

  const badgeStyle = styles[level] || 'bg-zinc-900 text-zinc-400 border-zinc-800';

  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium border ${badgeStyle}`}>
      {level || 'Unknown'}
    </span>
  );
}

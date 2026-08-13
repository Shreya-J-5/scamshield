import React from 'react';

export default function RiskScoreGauge({ score, level }) {
  const radius = 42;
  const circumference = 2 * Math.PI * radius;
  const progress = Math.min(100, Math.max(0, score));
  const strokeDashoffset = circumference - (progress / 100) * circumference;

  const colorMap = {
    Low: '#34d399',        // emerald
    Suspicious: '#fbbf24', // amber
    High: '#fb923c',       // orange
    Critical: '#f87171',   // rose
  };

  const strokeColor = colorMap[level] || '#a1a1aa';

  return (
    <div className="relative inline-flex items-center justify-center">
      <svg className="w-28 h-28 transform -rotate-90">
        <circle
          cx="56"
          cy="56"
          r={radius}
          stroke="#27272a"
          strokeWidth="6"
          fill="transparent"
        />
        <circle
          cx="56"
          cy="56"
          r={radius}
          stroke={strokeColor}
          strokeWidth="6"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          fill="transparent"
          className="transition-all duration-700 ease-out"
        />
      </svg>
      <div className="absolute flex flex-col items-center justify-center text-center">
        <span className="text-2xl font-bold tracking-tight text-white">{score}</span>
        <span className="text-[9px] uppercase tracking-wider font-medium text-zinc-500">Risk Score</span>
      </div>
    </div>
  );
}

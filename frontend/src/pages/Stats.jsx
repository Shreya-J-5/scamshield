import React, { useEffect, useState } from 'react';
import { getScans } from '../services/api';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, BarChart, Bar, XAxis, YAxis } from 'recharts';

export default function Stats() {
  const [scans, setScans] = useState([]);

  useEffect(() => {
    getScans().then(setScans).catch(() => {});
  }, []);

  const total = scans.length;
  const lowCount = scans.filter((s) => s.risk_level === 'Low').length;
  const suspiciousCount = scans.filter((s) => s.risk_level === 'Suspicious').length;
  const highCount = scans.filter((s) => s.risk_level === 'High').length;
  const criticalCount = scans.filter((s) => s.risk_level === 'Critical').length;

  const chartData = [
    { name: 'Low', value: lowCount, color: '#34d399' },
    { name: 'Suspicious', value: suspiciousCount, color: '#fbbf24' },
    { name: 'High', value: highCount, color: '#fb923c' },
    { name: 'Critical', value: criticalCount, color: '#f87171' },
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-6 py-4">
      <div className="space-y-1">
        <h2 className="text-xl font-semibold text-white tracking-tight">
          Analytics Overview
        </h2>
        <p className="text-xs text-zinc-400">
          Risk distribution breakdown across all recorded scans.
        </p>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
        <div className="bg-[#121215] rounded-xl p-3.5 border border-zinc-800 space-y-0.5">
          <span className="text-[11px] text-zinc-500 font-medium">Total Scans</span>
          <p className="text-xl font-bold text-white">{total}</p>
        </div>

        <div className="bg-[#121215] rounded-xl p-3.5 border border-zinc-800 space-y-0.5">
          <span className="text-[11px] text-emerald-400 font-medium">Low Risk</span>
          <p className="text-xl font-bold text-emerald-400">{lowCount}</p>
        </div>

        <div className="bg-[#121215] rounded-xl p-3.5 border border-zinc-800 space-y-0.5">
          <span className="text-[11px] text-amber-400 font-medium">Suspicious</span>
          <p className="text-xl font-bold text-amber-400">{suspiciousCount}</p>
        </div>

        <div className="bg-[#121215] rounded-xl p-3.5 border border-zinc-800 space-y-0.5">
          <span className="text-[11px] text-orange-400 font-medium">High Risk</span>
          <p className="text-xl font-bold text-orange-400">{highCount}</p>
        </div>

        <div className="bg-[#121215] rounded-xl p-3.5 border border-zinc-800 space-y-0.5 col-span-2 sm:col-span-1">
          <span className="text-[11px] text-rose-400 font-medium">Critical</span>
          <p className="text-xl font-bold text-rose-400">{criticalCount}</p>
        </div>
      </div>

      {/* Analytics Charts */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-[#121215] rounded-xl p-5 border border-zinc-800 space-y-3">
          <h3 className="text-xs font-medium text-zinc-300">Risk Ratio Breakdown</h3>
          <div className="h-52">
            {total === 0 ? (
              <div className="h-full flex items-center justify-center text-xs text-zinc-500">
                No logs recorded yet
              </div>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={chartData}
                    cx="50%"
                    cy="50%"
                    innerRadius={45}
                    outerRadius={70}
                    paddingAngle={3}
                    dataKey="value"
                  >
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{ backgroundColor: '#09090b', borderColor: '#27272a', borderRadius: '8px', color: '#fff', fontSize: '12px' }}
                  />
                </PieChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

        <div className="bg-[#121215] rounded-xl p-5 border border-zinc-800 space-y-3">
          <h3 className="text-xs font-medium text-zinc-300">Threat Volume</h3>
          <div className="h-52">
            {total === 0 ? (
              <div className="h-full flex items-center justify-center text-xs text-zinc-500">
                No logs recorded yet
              </div>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData}>
                  <XAxis dataKey="name" stroke="#71717a" fontSize={11} />
                  <YAxis stroke="#71717a" fontSize={11} allowDecimals={false} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#09090b', borderColor: '#27272a', borderRadius: '8px', color: '#fff', fontSize: '12px' }}
                  />
                  <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-bar-${index}`} fill={entry.color} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

import React, { useEffect, useState } from 'react';
import { getScans, deleteScan } from '../services/api';
import RiskBadge from '../components/RiskBadge';
import { Trash2, RefreshCw, Clock } from 'lucide-react';

export default function History() {
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchScans = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getScans();
      setScans(data);
    } catch (err) {
      setError(err.message || 'Failed to load scan logs');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchScans();
  }, []);

  const handleDelete = async (id) => {
    try {
      await deleteScan(id);
      setScans(scans.filter((s) => s.id !== id));
    } catch (err) {
      alert('Failed to delete log entry');
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 py-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold text-white tracking-tight">
            Security Logs
          </h2>
          <p className="text-xs text-zinc-400">
            History of previously evaluated messages and page scans.
          </p>
        </div>

        <button
          onClick={fetchScans}
          disabled={loading}
          className="px-2.5 py-1.5 rounded-lg bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 text-zinc-300 text-xs font-medium transition-all flex items-center gap-1.5"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh</span>
        </button>
      </div>

      {error && (
        <div className="p-3 rounded-lg bg-rose-950/40 border border-rose-800/40 text-rose-300 text-xs">
          {error}
        </div>
      )}

      {loading ? (
        <div className="text-center py-12 text-zinc-500 text-xs">
          Loading logs...
        </div>
      ) : scans.length === 0 ? (
        <div className="p-8 text-center bg-[#121215] rounded-xl border border-zinc-800 space-y-2 text-xs text-zinc-400">
          No security logs recorded yet. Run your first analysis to see results here.
        </div>
      ) : (
        <div className="space-y-2">
          {scans.map((scan) => (
            <div
              key={scan.id}
              className="bg-[#121215] rounded-xl p-4 border border-zinc-800/80 flex flex-col sm:flex-row sm:items-center justify-between gap-3"
            >
              <div className="space-y-1.5 flex-1 min-w-0">
                <div className="flex items-center space-x-2.5">
                  <RiskBadge level={scan.risk_level} />
                  <span className="text-[11px] font-mono text-zinc-400">
                    Score: {scan.risk_score}/100
                  </span>
                  <span className="text-[11px] text-zinc-500 flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {scan.created_at ? new Date(scan.created_at).toLocaleTimeString() : 'Just now'}
                  </span>
                </div>

                <p className="text-xs text-zinc-300 truncate font-mono bg-zinc-950/60 p-2 rounded border border-zinc-900">
                  {scan.message_text}
                </p>
              </div>

              <button
                onClick={() => handleDelete(scan.id)}
                title="Delete entry"
                className="p-1.5 rounded-lg bg-zinc-900 hover:bg-rose-950/40 hover:text-rose-400 text-zinc-500 border border-zinc-800 transition-all self-end sm:self-center"
              >
                <Trash2 className="w-3.5 h-3.5" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

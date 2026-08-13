import React from 'react';
import { Shield, ShieldAlert, History, BarChart2, Home } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab }) {
  const navItems = [
    { id: 'home', label: 'Overview', icon: Home },
    { id: 'analyzer', label: 'Analyzer', icon: ShieldAlert },
    { id: 'history', label: 'Logs', icon: History },
    { id: 'stats', label: 'Analytics', icon: BarChart2 },
  ];

  return (
    <header className="border-b border-zinc-800/80 bg-[#09090b]/90 backdrop-blur sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">
        <div className="flex items-center space-x-2.5 cursor-pointer" onClick={() => setActiveTab('home')}>
          <div className="p-1.5 rounded-lg bg-zinc-900 border border-zinc-800 text-zinc-100">
            <Shield className="w-4 h-4" />
          </div>
          <span className="text-sm font-semibold tracking-tight text-white">
            ScamShield
          </span>
        </div>

        <nav className="flex items-center space-x-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center space-x-2 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
                  isActive
                    ? 'bg-zinc-800/90 text-white border border-zinc-700/60'
                    : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900/60'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>
    </header>
  );
}

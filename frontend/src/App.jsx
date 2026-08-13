import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Analyzer from './pages/Analyzer';
import History from './pages/History';
import Stats from './pages/Stats';

export default function App() {
  const [activeTab, setActiveTab] = useState('home');

  return (
    <div className="min-h-screen bg-[#09090b] text-zinc-100 flex flex-col selection:bg-zinc-800 selection:text-white">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      <main className="flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 py-6">
        {activeTab === 'home' && <Home onStartAnalysis={() => setActiveTab('analyzer')} />}
        {activeTab === 'analyzer' && <Analyzer />}
        {activeTab === 'history' && <History />}
        {activeTab === 'stats' && <Stats />}
      </main>

      <footer className="border-t border-zinc-800/60 bg-[#09090b] py-4 text-center text-[11px] text-zinc-500">
        <p>ScamShield Security Tool — Real-time Explainable Risk Indicator Engine</p>
      </footer>
    </div>
  );
}

import React from 'react';
import { ArrowRight, ShieldCheck, Lock, Eye, Chrome } from 'lucide-react';

export default function Home({ onStartAnalysis }) {
  return (
    <div className="space-y-12 py-8 max-w-4xl mx-auto">
      {/* Minimal Hero */}
      <div className="space-y-4 text-left">
        <h1 className="text-3xl sm:text-4xl font-bold text-white tracking-tight">
          Explainable Scam & Phishing Detection
        </h1>
        <p className="text-sm sm:text-base text-zinc-400 max-w-2xl leading-relaxed">
          Analyze suspicious SMS messages, WhatsApp text, email content, URLs, and active web pages in real-time with transparent rule heuristics and multi-provider verification.
        </p>

        <div className="pt-2">
          <button
            onClick={onStartAnalysis}
            className="inline-flex items-center space-x-2 px-4 py-2.5 rounded-lg bg-zinc-100 hover:bg-white text-zinc-950 text-xs font-semibold transition-all"
          >
            <span>Analyze a Message</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Feature Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 border-t border-zinc-800/80 pt-8">
        <div className="p-4 rounded-xl bg-[#121215] border border-zinc-800/80 space-y-2">
          <div className="p-2 w-fit rounded-md bg-zinc-900 text-zinc-300 border border-zinc-800">
            <Eye className="w-4 h-4" />
          </div>
          <h3 className="text-xs font-semibold text-white">Transparent Scoring</h3>
          <p className="text-xs text-zinc-400 leading-relaxed">
            Every risk level includes human-readable explanations and explicit evidence for each triggered rule.
          </p>
        </div>

        <div className="p-4 rounded-xl bg-[#121215] border border-zinc-800/80 space-y-2">
          <div className="p-2 w-fit rounded-md bg-zinc-900 text-zinc-300 border border-zinc-800">
            <Lock className="w-4 h-4" />
          </div>
          <h3 className="text-xs font-semibold text-white">Privacy Standard</h3>
          <p className="text-xs text-zinc-400 leading-relaxed">
            Sensitive OTPs, PINs, and card numbers are automatically sanitized before storage or processing.
          </p>
        </div>

        <div className="p-4 rounded-xl bg-[#121215] border border-zinc-800/80 space-y-2">
          <div className="p-2 w-fit rounded-md bg-zinc-900 text-zinc-300 border border-zinc-800">
            <Chrome className="w-4 h-4" />
          </div>
          <h3 className="text-xs font-semibold text-white">Chrome Extension</h3>
          <p className="text-xs text-zinc-400 leading-relaxed">
            Inspect live web page content and anchor links directly from your Chrome popup in one click.
          </p>
        </div>
      </div>

      {/* Disclaimer */}
      <div className="p-4 rounded-xl bg-zinc-900/40 border border-zinc-800 text-zinc-400 text-xs leading-relaxed">
        <span className="font-semibold text-zinc-300">Disclaimer:</span> ScamShield provides risk indicators and rule heuristics. It is an auxiliary assessment tool and cannot guarantee 100% detection of all threats.
      </div>
    </div>
  );
}

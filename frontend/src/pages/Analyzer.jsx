import React, { useState } from 'react';
import { analyzeMessage } from '../services/api';
import ResultCard from '../components/ResultCard';
import { Loader2, ArrowRight } from 'lucide-react';

const PRESET_TEST_CASES = [
  {
    title: 'Bank KYC (Scam)',
    message: 'URGENT: Your HDFC Bank account will be blocked today due to pending KYC. Click http://192.168.1.50/verify-kyc to update your OTP and PIN immediately.',
    sender: 'HDFC Alert',
    sender_contact: 'kyc-update@suspicious.com',
  },
  {
    title: 'Courier Fee (Scam)',
    message: 'FedEx: Your parcel delivery is on hold due to unpaid fee of $2.50. Pay now at https://bit.ly/fedex-fee-pay or package will be returned.',
    sender: 'FedEx Delivery',
    sender_contact: 'notice@courier-fee.xyz',
  },
  {
    title: 'Lottery (Scam)',
    message: 'CONGRATULATIONS! You have won $50,000 in the International Tech Lottery! Claim your reward now by paying registration fee at http://win-prize-claim.top/reward',
    sender: 'Lottery Winner',
    sender_contact: 'prize@win-lottery.info',
  },
  {
    title: 'Normal Notice (Safe)',
    message: 'Hi team, reminder that our monthly hackathon presentation starts at 4 PM in Room 302. Please review the shared slide deck beforehand.',
    sender: 'Sarah (Team Lead)',
    sender_contact: 'sarah.dev@company.com',
  },
];

export default function Analyzer() {
  const [messageText, setMessageText] = useState('');
  const [sender, setSender] = useState('');
  const [senderContact, setSenderContact] = useState('');
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!messageText.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const data = await analyzeMessage({
        message_text: messageText,
        sender: sender || null,
        sender_contact: senderContact || null,
        url: url ? url : null,
      });
      setResult(data);
    } catch (err) {
      setError(err.message || 'An error occurred while analyzing');
    } finally {
      setLoading(false);
    }
  };

  const handleLoadPreset = (preset) => {
    setMessageText(preset.message);
    setSender(preset.sender);
    setSenderContact(preset.sender_contact);
    setUrl('');
    setResult(null);
    setError(null);
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6 py-4">
      <div className="space-y-1">
        <h2 className="text-xl font-semibold text-white tracking-tight">
          Message & Link Security Analyzer
        </h2>
        <p className="text-xs text-zinc-400">
          Analyze suspicious text messages, emails, senders, or web URLs.
        </p>
      </div>

      {/* Preset Test Buttons */}
      <div className="space-y-1.5">
        <span className="text-[11px] font-medium text-zinc-500 uppercase tracking-wider">
          Sample Presets:
        </span>
        <div className="flex flex-wrap gap-1.5">
          {PRESET_TEST_CASES.map((preset, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleLoadPreset(preset)}
              className="text-xs px-2.5 py-1 rounded bg-zinc-900 hover:bg-zinc-800 text-zinc-300 border border-zinc-800 transition-all"
            >
              {preset.title}
            </button>
          ))}
        </div>
      </div>

      {result ? (
        <ResultCard result={result} onReset={() => setResult(null)} />
      ) : (
        <form onSubmit={handleSubmit} className="bg-[#121215] rounded-xl p-5 border border-zinc-800 space-y-5">
          {error && (
            <div className="p-3 rounded-lg bg-rose-950/40 border border-rose-800/40 text-rose-300 text-xs">
              {error}
            </div>
          )}

          <div className="space-y-1.5">
            <label className="block text-xs font-medium text-zinc-300">
              Message Content <span className="text-rose-400">*</span>
            </label>
            <textarea
              rows={4}
              value={messageText}
              onChange={(e) => setMessageText(e.target.value)}
              placeholder="Paste SMS, WhatsApp message, or email body..."
              required
              className="w-full rounded-lg bg-[#09090b] border border-zinc-800 p-3 text-white placeholder-zinc-600 focus:outline-none focus:border-zinc-500 text-xs resize-y"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div className="space-y-1.5">
              <label className="block text-xs font-medium text-zinc-300">
                Claimed Sender
              </label>
              <input
                type="text"
                value={sender}
                onChange={(e) => setSender(e.target.value)}
                placeholder="e.g. HDFC Bank, FedEx"
                className="w-full rounded-lg bg-[#09090b] border border-zinc-800 p-2.5 text-white placeholder-zinc-600 focus:outline-none focus:border-zinc-500 text-xs"
              />
            </div>

            <div className="space-y-1.5">
              <label className="block text-xs font-medium text-zinc-300">
                Sender Email / Phone
              </label>
              <input
                type="text"
                value={senderContact}
                onChange={(e) => setSenderContact(e.target.value)}
                placeholder="e.g. alert@verify.com"
                className="w-full rounded-lg bg-[#09090b] border border-zinc-800 p-2.5 text-white placeholder-zinc-600 focus:outline-none focus:border-zinc-500 text-xs"
              />
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="block text-xs font-medium text-zinc-300">
              Optional Direct URL
            </label>
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="e.g. https://suspicious-link.com"
              className="w-full rounded-lg bg-[#09090b] border border-zinc-800 p-2.5 text-white placeholder-zinc-600 focus:outline-none focus:border-zinc-500 text-xs"
            />
          </div>

          <button
            type="submit"
            disabled={loading || !messageText.trim()}
            className="w-full py-2.5 rounded-lg bg-zinc-100 hover:bg-white text-zinc-950 text-xs font-semibold disabled:opacity-50 transition-all flex items-center justify-center space-x-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Running Analysis...</span>
              </>
            ) : (
              <>
                <span>Analyze Message</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </>
            )}
          </button>
        </form>
      )}
    </div>
  );
}

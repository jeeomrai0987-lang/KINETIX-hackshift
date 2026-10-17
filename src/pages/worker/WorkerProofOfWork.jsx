import React from 'react';
import { useAuth } from '../../context/AuthContext';

export const WorkerProofOfWork = () => {
  const { user, showToast } = useAuth();

  const handleCopyMerkle = () => {
    navigator.clipboard.writeText('0x7F2A83B49CD1019A82BEE9481CFA42099C4E');
    showToast('Merkle Root Hash copied to clipboard');
  };

  const reports = [
    {
      sprint: 'Sprint #3: MicroVM Concurrency & Adversarial Simulation',
      date: 'Completed Oct 16, 2025',
      score: '96.4 / 100',
      standing: 'Rank #2 in Cohort',
      hash: '0x8f9c7e2b34a189fcde7701fae2985172081d0092c',
      tests: '50,000 / 50,000 Passed',
      latency: '3.8ms p99',
      memoryLeaks: '0 bytes',
      reviewerVerdict: '3/3 Unanimous Blind Pass',
    },
    {
      sprint: 'Sprint #2: Distributed Consensus & Partition Healing',
      date: 'Completed Oct 02, 2025',
      score: '94.0 / 100',
      standing: 'Rank #4 in Cohort',
      hash: '0x3f7a11de9921ab45ca80182feec9103810a99120',
      tests: '25,000 / 25,000 Passed',
      latency: '5.2ms p99',
      memoryLeaks: '0 bytes',
      reviewerVerdict: '3/3 Unanimous Blind Pass',
    },
    {
      sprint: 'Sprint #1: Zero-Copy Serialization & Socket Buffer I/O',
      date: 'Completed Sep 18, 2025',
      score: '95.8 / 100',
      standing: 'Rank #3 in Cohort',
      hash: '0x12bb88ac019481cfa42099c4e5512b90214a189f',
      tests: '10,000 / 10,000 Passed',
      latency: '1.2ms p99',
      memoryLeaks: '0 bytes',
      reviewerVerdict: '3/3 Unanimous Blind Pass',
    },
  ];

  return (
    <div className="px-space-lg py-space-md flex flex-col gap-space-lg max-w-[1520px] mx-auto w-full">
      {/* Header and Cryptographic Badges */}
      <div className="flex flex-col xl:flex-row xl:items-end justify-between gap-space-md">
        <div className="flex flex-col gap-space-xs">
          <nav className="flex items-center gap-2 font-body-sm text-body-sm text-on-surface-variant mb-1">
            <span>Cohort Alpha '25</span>
            <span className="material-symbols-outlined text-[14px]">chevron_right</span>
            <span>Worker Portal</span>
            <span className="material-symbols-outlined text-[14px]">chevron_right</span>
            <span className="text-on-surface font-semibold">Proof-of-Work Ledger</span>
          </nav>
          <h1 className="font-headline-lg text-headline-lg text-on-surface tracking-tight font-bold">
            Proof-of-Work Reports &amp; Attestation Ledger
          </h1>
          <p className="font-body-md text-body-md text-on-surface-variant max-w-3xl">
            Cryptographically verified sprint reports, blind evaluation scorecards, and portable merit credentials for{' '}
            <span className="font-semibold text-on-surface">{user?.name || 'Alex Mercer'}</span>{' '}
            <span className="font-code-sm text-code-sm text-secondary bg-surface-container px-1.5 py-0.5 rounded">
              #{user?.nodeId || 'TX-5512B'}
            </span>.
          </p>

          <div className="flex flex-wrap items-center gap-space-xs mt-1">
            <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-surface-container text-on-surface font-code-sm text-code-sm border-0">
              <span className="w-2 h-2 rounded-full bg-secondary animate-pulse"></span>
              <span className="text-on-surface-variant">SHA-256 Merkle Root:</span>
              <span className="font-semibold tracking-wide">0x7F2A...9C4E</span>
              <button
                type="button"
                onClick={handleCopyMerkle}
                className="hover:text-secondary flex items-center ml-1"
                title="Copy Root Hash"
              >
                <span className="material-symbols-outlined text-[14px]">content_copy</span>
              </button>
            </div>
            <div className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-secondary-container text-on-secondary-container font-label-sm text-label-sm font-semibold">
              <span className="material-symbols-outlined text-[15px]">verified</span>
              Arbitrum &amp; Solana Anchored
            </div>
            <div className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-primary-container text-on-primary font-label-sm text-label-sm">
              <span className="material-symbols-outlined text-[15px] text-secondary-fixed">workspace_premium</span>
              Cohort Standing: Top 4% (Sprint Alpha)
            </div>
          </div>
        </div>

        <div className="flex items-center gap-space-sm shrink-0">
          <button
            type="button"
            onClick={() => showToast('Full cryptographic proof ledger downloaded (JSON + Signature)')}
            className="px-4 py-2 rounded-lg bg-surface-container hover:bg-surface-container-high text-on-surface font-label-md text-label-md font-semibold transition-all flex items-center gap-1.5 shadow-sm"
          >
            <span className="material-symbols-outlined text-[18px]">download</span>
            <span>Download Ledger</span>
          </button>
          <button
            type="button"
            onClick={() => showToast('Verifiable credential added to wallet')}
            className="px-4 py-2 rounded-lg bg-secondary text-on-secondary font-label-md text-label-md font-semibold hover:opacity-90 transition-all flex items-center gap-1.5 shadow-sm"
          >
            <span className="material-symbols-outlined text-[18px]">qr_code</span>
            <span>Share Verifiable Credential</span>
          </button>
        </div>
      </div>

      {/* Reports List */}
      <div className="space-y-space-md">
        {reports.map((r, idx) => (
          <div
            key={idx}
            className="bg-surface-container-lowest rounded-xl p-6 shadow-sm hover:shadow-md transition-all flex flex-col gap-4 border border-surface-container"
          >
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-surface-container">
              <div>
                <h2 className="font-headline-sm text-headline-sm font-bold text-on-surface">{r.sprint}</h2>
                <span className="font-body-sm text-xs text-on-surface-variant">{r.date} • {r.reviewerVerdict}</span>
              </div>
              <div className="flex items-center gap-3">
                <div className="text-right">
                  <span className="font-headline-md text-headline-md font-bold text-secondary block">{r.score}</span>
                  <span className="font-label-sm text-xs text-on-surface-variant font-semibold">{r.standing}</span>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 p-4 rounded-xl bg-surface-container-low/60 text-xs">
              <div>
                <span className="text-on-surface-variant block">Observed Latency:</span>
                <span className="font-bold text-on-surface text-sm">{r.latency}</span>
              </div>
              <div>
                <span className="text-on-surface-variant block">Test Cases Passed:</span>
                <span className="font-bold text-on-surface text-sm">{r.tests}</span>
              </div>
              <div>
                <span className="text-on-surface-variant block">Memory Leak Check:</span>
                <span className="font-bold text-emerald-600 text-sm">{r.memoryLeaks}</span>
              </div>
              <div>
                <span className="text-on-surface-variant block">Audit Hash:</span>
                <span className="font-mono text-secondary font-semibold truncate block">{r.hash.slice(0, 16)}...</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

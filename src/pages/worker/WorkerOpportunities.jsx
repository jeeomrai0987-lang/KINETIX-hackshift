import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';

export const WorkerOpportunities = () => {
  const { showToast } = useAuth();
  const [isRefreshing, setIsRefreshing] = useState(false);

  const opportunities = [
    {
      id: 'opp_1',
      squad: 'Synthetix AI',
      role: 'Lead Distributed Systems Architect',
      matchPct: '98% Algorithmic Fit',
      equity: '15.0% Equity Grant',
      stage: 'Seed Stage ($500k SAFE)',
      thesis: 'Autonomous agentic simulation pipeline for multi-agent LLM systems in enterprise fintech.',
      requirements: ['Rust or Go', 'Distributed Consensus', 'Low-Latency Networking'],
      founder: 'Elena Vance (CEO)',
    },
    {
      id: 'opp_2',
      squad: 'PolyMatrix AI',
      role: 'High-Throughput Core Engineer',
      matchPct: '92% Algorithmic Fit',
      equity: '12.0% Equity Grant',
      stage: 'Seed Stage ($350k Raised)',
      thesis: 'Synthetic data engines for continuous banking and credit compliance stress testing.',
      requirements: ['Distributed Systems', 'Data Pipelines', 'Python/Go'],
      founder: 'Dr. Aaron Meyer (CEO)',
    },
    {
      id: 'opp_3',
      squad: 'ChronoDB',
      role: 'Storage Engine Lead Architect',
      matchPct: '90% Algorithmic Fit',
      equity: '14.0% Equity Grant',
      stage: 'Pre-Seed ($300k Raised)',
      thesis: 'Zero-copy temporal vector storage engine for LLM memory caches.',
      requirements: ['Rust Core', 'Memory Layouts', 'Zero-Copy IO'],
      founder: 'Vikram Joshi (CEO)',
    },
    {
      id: 'opp_4',
      squad: 'Aether Labs',
      role: 'Wasm Sandbox Infrastructure Lead',
      matchPct: '88% Algorithmic Fit',
      equity: '10.0% Equity Grant',
      stage: 'Pre-Seed ($400k)',
      thesis: 'Deterministic agent sandboxing and ZK state transition execution.',
      requirements: ['Wasmtime', 'eBPF', 'Rust'],
      founder: 'Marcus Chen (CTO)',
    },
  ];

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => {
      setIsRefreshing(false);
      showToast('AI Matched Opportunities refreshed against updated challenge telemetry!');
    }, 800);
  };

  const handleApply = (opp) => {
    showToast(`Blind application token dispatched to ${opp.squad}! Identity remains cloaked.`);
  };

  return (
    <div className="px-space-lg py-space-md max-w-[1400px] mx-auto w-full space-y-space-lg">
      {/* Breadcrumb Hierarchy */}
      <nav className="flex items-center gap-space-xs text-on-surface-variant font-label-md text-label-md">
        <span>Cohort Alpha '25</span>
        <span className="material-symbols-outlined text-[14px]">chevron_right</span>
        <span>Worker Portal</span>
        <span className="material-symbols-outlined text-[14px]">chevron_right</span>
        <span className="text-secondary font-semibold">Squad Opportunities</span>
      </nav>

      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-space-md">
        <div>
          <div className="flex items-center gap-space-sm mb-1">
            <h1 className="font-headline-lg text-headline-lg text-on-surface tracking-tight font-bold">
              Matched Opportunities &amp; Squad Openings
            </h1>
            <span className="px-2.5 py-0.5 rounded-full bg-secondary-container text-on-secondary-container font-label-sm text-label-sm font-semibold tracking-wide flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-secondary animate-pulse"></span>
              Algorithmic Fit
            </span>
          </div>
          <p className="font-body-md text-body-md text-on-surface-variant max-w-3xl">
            AI-curated venture roles matched against your verified Sprint #1–#3 proof-of-work telemetry, code benchmarks,
            and architectural review logs.
          </p>
        </div>

        <div className="flex items-center gap-space-sm shrink-0">
          <button
            type="button"
            onClick={handleRefresh}
            disabled={isRefreshing}
            className="flex items-center gap-space-xs px-space-md h-10 rounded-lg bg-surface-container-lowest text-on-surface hover:bg-surface-container-low transition-all shadow-sm font-title-md text-title-md font-semibold"
          >
            <span className={`material-symbols-outlined text-[18px] text-secondary ${isRefreshing ? 'animate-spin' : ''}`}>
              sync
            </span>
            <span>Refresh AI Matches</span>
          </button>
        </div>
      </div>

      {/* Opportunities List */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-space-md">
        {opportunities.map((opp) => (
          <div
            key={opp.id}
            className="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm hover:shadow-md transition-all flex flex-col justify-between border border-surface-container"
          >
            <div>
              <div className="flex items-start justify-between gap-2 pb-3 border-b border-surface-container">
                <div>
                  <h2 className="font-title-md text-title-md font-bold text-on-surface">{opp.squad}</h2>
                  <span className="font-body-md text-body-md text-secondary font-semibold">{opp.role}</span>
                </div>
                <div className="flex flex-col items-end">
                  <span className="px-2.5 py-1 rounded-full bg-secondary-container text-on-secondary-container font-label-sm text-label-sm font-bold">
                    {opp.matchPct}
                  </span>
                  <span className="font-code-sm text-xs font-bold text-on-surface mt-1">{opp.equity}</span>
                </div>
              </div>

              <p className="font-body-sm text-body-sm text-on-surface-variant my-3 leading-relaxed">{opp.thesis}</p>

              <div className="flex flex-wrap gap-1.5 mb-4">
                {opp.requirements.map((req) => (
                  <span
                    key={req}
                    className="px-2 py-0.5 rounded bg-surface-container-high text-on-surface font-code-sm text-xs"
                  >
                    {req}
                  </span>
                ))}
              </div>
            </div>

            <div className="flex items-center justify-between pt-3 border-t border-surface-container">
              <span className="font-label-sm text-xs text-on-surface-variant">{opp.stage}</span>
              <button
                type="button"
                onClick={() => handleApply(opp)}
                className="px-4 py-2 rounded-lg bg-primary-container text-on-primary font-label-md text-label-md font-semibold hover:bg-primary transition-all flex items-center gap-1.5 shadow-xs"
              >
                <span>Apply with Blind Token</span>
                <span className="material-symbols-outlined text-[16px]">arrow_forward</span>
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

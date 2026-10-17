import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';

export const InvestorDiscoverStartups = () => {
  const { showToast } = useAuth();
  const [activeFilter, setActiveFilter] = useState('all');

  const startups = [
    {
      id: 'aether',
      name: 'Aether Labs',
      logoChar: 'Æ',
      sector: 'Autonomous Agent Infrastructure',
      score: 88,
      tier: 'Tier A',
      targetRaise: '$400k Pre-Seed',
      valCap: '$6,000,000',
      committed: '$180,000',
      description: 'Zero-knowledge verifiable agent runtime providing deterministic state sandboxing for enterprise workflows.',
      tags: ['YC Bound', 'Blind Evaluated', 'Rust / Wasm'],
      fastTrack: true,
    },
    {
      id: 'synthetix',
      name: 'Synthetix AI',
      logoChar: 'SX',
      sector: 'Enterprise AI & Fintech Stress-Testing',
      score: 96,
      tier: 'Tier A+',
      targetRaise: '$500k SAFE',
      valCap: '$10,000,000',
      committed: '$350,000',
      description: 'Ultra-low latency multi-agent simulation pipeline stress testing LLM systems before enterprise banking deployment.',
      tags: ['YC Bound', 'Blind Evaluated', 'WhatsApp Fast-Track'],
      fastTrack: true,
    },
    {
      id: 'chronodb',
      name: 'ChronoDB',
      logoChar: 'CD',
      sector: 'High-Throughput Vector Storage',
      score: 91,
      tier: 'Tier A',
      targetRaise: '$300k Pre-Seed',
      valCap: '$5,000,000',
      committed: '$120,000',
      description: 'Zero-copy temporal vector database specifically engineered for multi-modal agent memory caches.',
      tags: ['Blind Evaluated', 'Database', 'Deep Tech'],
      fastTrack: false,
    },
    {
      id: 'neuromesh',
      name: 'NeuroMesh',
      logoChar: 'NM',
      sector: 'Edge Neural Compilation',
      score: 84,
      tier: 'Tier B+',
      targetRaise: '$250k SAFE',
      valCap: '$4,500,000',
      committed: '$90,000',
      description: 'Distributed micro-model compiler enabling local real-time inference on low-power IoT chips.',
      tags: ['Edge AI', 'Hardware Accel'],
      fastTrack: false,
    },
    {
      id: 'valis',
      name: 'Valis Bio',
      logoChar: 'VB',
      sector: 'Generative Protein Formulation',
      score: 89,
      tier: 'Tier A',
      targetRaise: '$450k Seed',
      valCap: '$8,000,000',
      committed: '$200,000',
      description: 'Algorithmic binder prediction pipeline leveraging closed-loop synthetic biology lab robotics.',
      tags: ['BioTech', 'NSF Backed'],
      fastTrack: true,
    },
    {
      id: 'orbitex',
      name: 'Orbitex Security',
      logoChar: 'OX',
      sector: 'Zero-Knowledge Identity Vault',
      score: 86,
      tier: 'Tier B+',
      targetRaise: '$350k SAFE',
      valCap: '$5,500,000',
      committed: '$110,000',
      description: 'Cryptographic identity layer preserving worker anonymity across enterprise procurement audits.',
      tags: ['ZK Proofs', 'Security'],
      fastTrack: false,
    },
  ];

  const handleSyndicateLead = (st) => {
    showToast(`Syndicate allocation request dispatched to ${st.name}! Term sheet draft generated.`);
  };

  return (
    <div className="flex flex-col w-full space-y-space-lg">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-space-xs text-on-surface-variant font-label-sm text-label-sm uppercase tracking-wider mb-1">
            <span>Investor Portal</span>
            <span className="material-symbols-outlined text-[14px]">chevron_right</span>
            <span className="text-secondary font-semibold">Cohort Discovery</span>
          </div>
          <h1 className="font-headline-lg text-headline-lg text-primary tracking-tight font-bold">
            Discover Startups &amp; Formation Pipelines
          </h1>
          <p className="font-body-md text-body-md text-on-surface-variant">
            Explore verified startup squads synthesized from live 48h Sprint Cohort evaluations.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-secondary-container text-on-secondary-container font-label-sm text-label-sm font-semibold">
            <span className="w-2 h-2 rounded-full bg-secondary animate-pulse"></span>
            6 Vetted Squads Live
          </span>
        </div>
      </div>

      {/* Quick Filters */}
      <div className="flex flex-wrap items-center gap-2 p-3 bg-surface-container-lowest rounded-xl shadow-sm">
        <span className="font-label-sm text-label-sm text-on-surface-variant font-semibold uppercase tracking-wider mr-1">
          Filter:
        </span>
        {[
          { id: 'all', label: 'All Startups (6)' },
          { id: 'yc', label: 'YC Bound (2)' },
          { id: 'fast', label: 'Fast-Track (3)' },
        ].map((btn) => (
          <button
            key={btn.id}
            onClick={() => setActiveFilter(btn.id)}
            className={`h-8 px-3 rounded-full font-label-sm text-label-sm font-semibold transition-all ${
              activeFilter === btn.id
                ? 'bg-primary-container text-on-primary'
                : 'bg-surface-container hover:bg-surface-container-high text-on-surface'
            }`}
          >
            {btn.label}
          </button>
        ))}
      </div>

      {/* Startups Grid (3x2 Desktop Layout) */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        {startups
          .filter((st) => {
            if (activeFilter === 'yc' && !st.tags.includes('YC Bound')) return false;
            if (activeFilter === 'fast' && !st.fastTrack) return false;
            return true;
          })
          .map((st) => (
            <div
              key={st.id}
              className="bg-surface-container-lowest rounded-xl p-6 shadow-sm hover:shadow-md transition-all flex flex-col justify-between border border-surface-container group"
            >
              <div>
                <div className="flex items-start justify-between gap-3 mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-xl bg-primary-container text-on-primary flex items-center justify-center font-headline-sm text-headline-sm font-bold shadow-sm">
                      <span className="text-secondary-fixed">{st.logoChar}</span>
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <h3 className="font-headline-sm text-headline-sm text-on-surface group-hover:text-secondary transition-colors font-bold">
                          {st.name}
                        </h3>
                        <span className="material-symbols-outlined text-secondary text-[16px]">verified</span>
                      </div>
                      <div className="font-label-sm text-xs text-on-surface-variant font-medium">{st.sector}</div>
                    </div>
                  </div>

                  <div className="flex flex-col items-end shrink-0">
                    <div className="flex items-center gap-1 px-2.5 py-1 rounded-lg bg-surface-container text-on-surface font-title-md text-title-md font-bold">
                      <span className="text-secondary font-code-sm text-code-sm">{st.score}</span>
                      <span className="text-outline text-[11px] font-normal">/100</span>
                    </div>
                    <span className="font-label-sm text-xs text-secondary font-semibold uppercase tracking-wider mt-0.5">
                      {st.tier}
                    </span>
                  </div>
                </div>

                <p className="font-body-sm text-body-sm text-on-surface-variant leading-relaxed mb-4">
                  {st.description}
                </p>

                {/* Round terms */}
                <div className="grid grid-cols-2 gap-2 p-3 rounded-lg bg-surface-container-low mb-4 text-xs">
                  <div>
                    <span className="text-on-surface-variant block">Seeking / Round:</span>
                    <span className="font-bold text-on-surface">{st.targetRaise}</span>
                  </div>
                  <div>
                    <span className="text-on-surface-variant block">Valuation Cap:</span>
                    <span className="font-bold text-on-surface">{st.valCap}</span>
                  </div>
                </div>

                <div className="flex flex-wrap gap-1 mb-4">
                  {st.tags.map((t) => (
                    <span
                      key={t}
                      className="px-2 py-0.5 rounded bg-surface-container-high text-on-surface font-code-sm text-xs font-medium"
                    >
                      {t}
                    </span>
                  ))}
                </div>
              </div>

              <div className="pt-3 border-t border-surface-container">
                <button
                  type="button"
                  onClick={() => handleSyndicateLead(st)}
                  className="w-full py-2.5 rounded-lg bg-primary-container text-on-primary font-label-md text-label-md font-semibold hover:bg-primary transition-all flex items-center justify-center gap-1.5 shadow-xs"
                >
                  <span className="material-symbols-outlined text-[16px]">add_circle</span>
                  <span>Participate in Syndicate</span>
                </button>
              </div>
            </div>
          ))}
      </div>
    </div>
  );
};

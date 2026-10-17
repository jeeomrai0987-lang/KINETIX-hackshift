import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export const InvestorPortfolio = () => {
  const { showToast } = useAuth();
  const [activeTab, setActiveTab] = useState('all');
  const [filterText, setFilterText] = useState('');

  const holdings = [
    {
      id: 'synthetix',
      name: 'Synthetix AI',
      stage: 'Seed Stage',
      instrument: 'Post-Money SAFE',
      principal: '$200,000',
      valCap: '$10,000,000',
      discount: '20%',
      equityPct: '2.0%',
      runway: '16.4 Months',
      mrr: '$8,500',
      score: '96.4/100',
      founder: 'Elena Vance (CEO)',
      thesis: 'Autonomous agentic simulation pipeline for multi-agent LLM systems in enterprise banking.',
      tags: ['Enterprise AI', 'Fintech Infrastructure', 'MicroVM'],
    },
    {
      id: 'polymatrix',
      name: 'PolyMatrix AI',
      stage: 'Seed Stage',
      instrument: 'SAFE Note with MFN',
      principal: '$150,000',
      valCap: '$8,000,000',
      discount: '20%',
      equityPct: '1.87%',
      runway: '14.2 Months',
      mrr: '$6,200',
      score: '92.1/100',
      founder: 'Dr. Aaron Meyer (CEO)',
      thesis: 'High-throughput synthetic data engine for regulatory stress test suites.',
      tags: ['Data Synthesis', 'RegTech', 'Enterprise'],
    },
    {
      id: 'kauri',
      name: 'Kauri Health',
      stage: 'Pre-Seed',
      instrument: 'Grant & Warrant',
      principal: '$75,000',
      valCap: '$5,000,000',
      discount: '15%',
      equityPct: '1.5%',
      runway: '12.0 Months',
      mrr: '$3,400',
      score: '89.0/100',
      founder: 'Dr. Maya Lin (CEO)',
      thesis: 'Verifiable clinical reasoning agents with deterministic safety gates.',
      tags: ['BioTech', 'Health AI', 'NSF Backed'],
    },
  ];

  const filteredHoldings = holdings.filter((h) => {
    if (activeTab === 'seed' && h.stage !== 'Seed Stage') return false;
    if (activeTab === 'pre-seed' && h.stage !== 'Pre-Seed') return false;
    if (filterText && !h.name.toLowerCase().includes(filterText.toLowerCase())) return false;
    return true;
  });

  return (
    <div className="flex flex-col w-full space-y-space-lg">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="font-headline-lg text-headline-lg text-primary tracking-tight font-bold">
            Portfolio Holdings &amp; Stakes
          </h1>
          <p className="font-body-md text-body-md text-on-surface-variant">
            Verified cap table positions, safe notes, and continuous financial telemetry.
          </p>
        </div>
        <button
          type="button"
          onClick={() => showToast('Full portfolio attestation ledger exported')}
          className="h-10 px-4 rounded-lg bg-primary-container text-on-primary font-title-md text-title-md font-semibold hover:bg-primary transition-all shadow-sm flex items-center gap-2 self-start sm:self-auto"
        >
          <span className="material-symbols-outlined text-[18px]">download</span>
          <span>Download Audit Pack</span>
        </button>
      </div>

      {/* Tabs and Search Bar */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4 bg-surface-container-lowest p-4 rounded-xl shadow-sm">
        <div className="inline-flex p-1 rounded-lg bg-surface-container-high text-on-surface-variant self-start">
          {[
            { id: 'all', label: 'All Holdings (3)' },
            { id: 'seed', label: 'Seed Stage (2)' },
            { id: 'pre-seed', label: 'Pre-Seed (1)' },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-3.5 py-1.5 rounded-md font-label-md text-label-md font-semibold transition-all ${
                activeTab === tab.id
                  ? 'bg-surface-container-lowest text-on-surface shadow-sm'
                  : 'text-on-surface-variant hover:text-on-surface'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        <div className="relative w-full sm:w-64">
          <span className="material-symbols-outlined absolute left-2.5 top-2.5 text-outline text-[16px]">
            search
          </span>
          <input
            value={filterText}
            onChange={(e) => setFilterText(e.target.value)}
            className="w-full h-9 pl-8 pr-3 rounded-lg bg-surface-container-low font-body-sm text-body-sm text-on-surface placeholder:text-outline focus:outline-none focus:ring-1 focus:ring-secondary/40"
            placeholder="Filter holdings by name..."
            type="text"
          />
        </div>
      </div>

      {/* Primary Workspace: 2-Column Split */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Column (8 cols): Ventures Detailed Cards */}
        <div className="lg:col-span-8 flex flex-col gap-6">
          {filteredHoldings.map((venture) => (
            <div
              key={venture.id}
              className="rounded-xl bg-surface-container-lowest p-6 shadow-sm hover:shadow-md transition-all flex flex-col gap-5 border border-surface-container"
            >
              <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
                <div className="flex items-start gap-3.5">
                  <div className="w-12 h-12 rounded-xl bg-primary-container text-on-primary flex items-center justify-center font-bold text-lg shrink-0 shadow-sm">
                    {venture.name.slice(0, 2).toUpperCase()}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h2 className="font-headline-sm text-headline-sm font-bold text-on-surface">{venture.name}</h2>
                      <span className="px-2.5 py-0.5 rounded-full bg-secondary-container text-on-secondary-container font-label-sm text-label-sm font-semibold">
                        {venture.stage}
                      </span>
                    </div>
                    <p className="font-body-sm text-body-sm text-on-surface-variant mt-0.5">
                      {venture.founder} • {venture.instrument}
                    </p>
                  </div>
                </div>

                <div className="flex items-baseline gap-1 bg-surface-container px-3 py-1 rounded-xl self-start sm:self-auto">
                  <span className="font-code-sm text-code-sm font-bold text-secondary">{venture.score}</span>
                  <span className="font-label-sm text-xs text-on-surface-variant">Rubric</span>
                </div>
              </div>

              <p className="font-body-md text-body-md text-on-surface leading-relaxed">{venture.thesis}</p>

              {/* Financial Metrics Strip */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 p-4 rounded-xl bg-surface-container-low/60">
                <div>
                  <span className="font-label-sm text-xs text-on-surface-variant block">Invested Principal</span>
                  <span className="font-title-md text-body-md font-bold text-on-surface">{venture.principal}</span>
                </div>
                <div>
                  <span className="font-label-sm text-xs text-on-surface-variant block">Valuation Cap</span>
                  <span className="font-title-md text-body-md font-bold text-on-surface">{venture.valCap}</span>
                </div>
                <div>
                  <span className="font-label-sm text-xs text-on-surface-variant block">Ownership Stake</span>
                  <span className="font-title-md text-body-md font-bold text-secondary">{venture.equityPct}</span>
                </div>
                <div>
                  <span className="font-label-sm text-xs text-on-surface-variant block">Audited Runway</span>
                  <span className="font-title-md text-body-md font-bold text-on-surface">{venture.runway}</span>
                </div>
              </div>

              <div className="flex flex-wrap items-center justify-between gap-4 pt-2 border-t border-surface-container">
                <div className="flex flex-wrap gap-1.5">
                  {venture.tags.map((t) => (
                    <span
                      key={t}
                      className="px-2 py-0.5 rounded bg-surface-container text-on-surface font-code-sm text-xs"
                    >
                      {t}
                    </span>
                  ))}
                </div>
                <div className="flex items-center gap-2">
                  <Link
                    to="/investor/financial-report"
                    className="px-3.5 py-1.5 rounded-lg bg-surface-container-low hover:bg-surface-container-high text-on-surface font-label-md text-label-md font-semibold transition-colors"
                  >
                    Financial Report
                  </Link>
                  <Link
                    to="/investor/investment-terms"
                    className="px-3.5 py-1.5 rounded-lg bg-secondary text-on-secondary hover:opacity-90 font-label-md text-label-md font-semibold transition-all shadow-xs"
                  >
                    View Terms
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Right Column (4 cols): Syndicate Summary */}
        <div className="lg:col-span-4 flex flex-col gap-6">
          <div className="bg-surface-container-lowest rounded-xl p-6 shadow-sm flex flex-col gap-4 border border-surface-container">
            <h3 className="font-title-md text-title-md font-bold text-on-surface flex items-center gap-2">
              <span className="material-symbols-outlined text-secondary">pie_chart</span>
              Capital Allocation
            </h3>

            <div className="space-y-3 font-body-sm text-body-sm">
              <div>
                <div className="flex justify-between items-center mb-1">
                  <span>Synthetix AI (47.1%)</span>
                  <span className="font-bold text-on-surface">$200,000</span>
                </div>
                <div className="w-full bg-surface-container h-2 rounded-full overflow-hidden">
                  <div className="bg-primary h-full rounded-full" style={{ width: '47.1%' }}></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between items-center mb-1">
                  <span>PolyMatrix AI (35.3%)</span>
                  <span className="font-bold text-on-surface">$150,000</span>
                </div>
                <div className="w-full bg-surface-container h-2 rounded-full overflow-hidden">
                  <div className="bg-secondary h-full rounded-full" style={{ width: '35.3%' }}></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between items-center mb-1">
                  <span>Kauri Health (17.6%)</span>
                  <span className="font-bold text-on-surface">$75,000</span>
                </div>
                <div className="w-full bg-surface-container h-2 rounded-full overflow-hidden">
                  <div className="bg-primary-container h-full rounded-full" style={{ width: '17.6%' }}></div>
                </div>
              </div>
            </div>

            <div className="pt-3 border-t border-surface-container flex justify-between items-center font-title-md text-body-md font-bold text-on-surface">
              <span>Total Deployed</span>
              <span className="text-secondary">$425,000</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

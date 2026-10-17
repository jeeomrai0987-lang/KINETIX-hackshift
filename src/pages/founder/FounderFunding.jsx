import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';

export const FounderFunding = () => {
  const { showToast } = useAuth();
  const [activeCategory, setActiveCategory] = useState('all');

  const opportunities = [
    {
      id: 'opp_1',
      name: 'Syndicate Alpha Angel Pool',
      category: 'syndicate',
      checkSize: '$250,000 – $500,000',
      structure: 'Post-Money SAFE ($10M Cap, 20% Discount)',
      matchFit: '98% Algorithmic Fit',
      tags: ['Enterprise AI', 'Distributed Systems', 'Lead Investor'],
      timeline: 'Terms Ready in 48 Hours',
    },
    {
      id: 'opp_2',
      name: 'Apex Horizon Capital',
      category: 'micro_vc',
      checkSize: '$400,000',
      structure: 'Priced Seed / SAFE Side Letter',
      matchFit: '95% Algorithmic Fit',
      tags: ['Fintech Infrastructure', 'High Throughput'],
      timeline: 'Partner Review Scheduled',
    },
    {
      id: 'opp_3',
      name: 'NSF SBIR Phase I AI Grant',
      category: 'grant',
      checkSize: '$275,000',
      structure: 'Non-Dilutive Federal Grant (0% Equity)',
      matchFit: '92% Algorithmic Fit',
      tags: ['Zero Dilution', 'Simulation Moat', 'Government'],
      timeline: 'Submission Window Open',
    },
    {
      id: 'opp_4',
      name: 'Fintech Velocity Syndicate',
      category: 'syndicate',
      checkSize: '$150,000 – $300,000',
      structure: 'SAFE Note with MFN & Pro-Rata',
      matchFit: '91% Algorithmic Fit',
      tags: ['Banking Tech', 'Agentic Workflows'],
      timeline: 'Attestation Room Verified',
    },
  ];

  const filteredOpps =
    activeCategory === 'all'
      ? opportunities
      : opportunities.filter((o) => o.category === activeCategory);

  const handleRequestTerms = (opp) => {
    showToast(`Dispatched confidential venture data pack to ${opp.name}`);
  };

  return (
    <div className="flex flex-col w-full gap-space-lg">
      {/* Hero & Breadcrumb */}
      <div className="flex flex-col gap-space-md">
        <div className="flex items-center gap-space-xs text-on-surface-variant font-label-sm text-label-sm uppercase tracking-wider">
          <span>Cohort Alpha ‘25</span>
          <span className="material-symbols-outlined text-[14px]">chevron_right</span>
          <span>Synthetix AI</span>
          <span className="material-symbols-outlined text-[14px]">chevron_right</span>
          <span className="text-secondary font-semibold">Syndicate &amp; Funding Discovery</span>
        </div>

        <div className="flex flex-col xl:flex-row xl:items-start justify-between gap-space-md">
          <div className="flex flex-col gap-space-xs max-w-3xl">
            <h1 className="font-headline-lg text-headline-lg text-on-surface tracking-tight font-bold">
              Syndicate &amp; Non-Dilutive Funding Discovery
            </h1>
            <p className="font-body-md text-body-md text-on-surface-variant leading-relaxed">
              AI-matched capital opportunities mapped to Synthetix AI’s verified telemetry, milestone deliverables, and
              enterprise fintech thesis.
            </p>
          </div>

          <div className="flex items-center gap-space-sm shrink-0">
            <button
              type="button"
              onClick={() => showToast('Cap table synced with funding allocations')}
              className="flex items-center gap-2 px-space-md h-10 rounded-lg bg-surface-container-low text-on-surface hover:bg-surface-container transition-colors font-label-md text-label-md font-semibold shadow-sm"
            >
              <span className="material-symbols-outlined text-[18px]">table_chart</span>
              <span>Sync Cap Table</span>
            </button>
            <button
              type="button"
              onClick={() => showToast('Matched brief exported with verified Merkle proof')}
              className="flex items-center gap-2 px-space-md h-10 rounded-lg bg-primary-container text-on-primary hover:bg-primary transition-colors font-label-md text-label-md font-semibold shadow-sm"
            >
              <span className="material-symbols-outlined text-[18px]">ios_share</span>
              <span>Export Matched Brief</span>
            </button>
          </div>
        </div>

        {/* Metric Status Pills */}
        <div className="flex flex-wrap items-center gap-space-sm pt-space-xs">
          <div className="flex items-center gap-2 px-space-md py-1.5 rounded-full bg-surface-container-lowest shadow-sm">
            <span className="w-2 h-2 rounded-full bg-secondary"></span>
            <span className="font-label-sm text-label-sm text-on-surface-variant font-medium">Active Match Pool:</span>
            <span className="font-label-sm text-label-sm text-on-surface font-bold">142 Opportunities</span>
          </div>
          <div className="flex items-center gap-2 px-space-md py-1.5 rounded-full bg-surface-container-lowest shadow-sm">
            <span className="material-symbols-outlined text-[16px] text-secondary">paid</span>
            <span className="font-label-sm text-label-sm text-on-surface-variant font-medium">Committed Syndicate Interest:</span>
            <span className="font-label-sm text-label-sm text-secondary font-bold">$1.2M Ready</span>
          </div>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-2 border-b border-surface-container pb-2">
        {[
          { id: 'all', label: 'All Opportunities (4)' },
          { id: 'syndicate', label: 'Angel Syndicates (2)' },
          { id: 'micro_vc', label: 'Micro-VCs (1)' },
          { id: 'grant', label: 'Non-Dilutive Grants (1)' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveCategory(tab.id)}
            className={`px-4 py-2 rounded-lg font-label-md text-label-md font-semibold transition-all ${
              activeCategory === tab.id
                ? 'bg-primary-container text-on-primary shadow-xs'
                : 'text-on-surface-variant hover:bg-surface-container'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Opportunities Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-space-md">
        {filteredOpps.map((opp) => (
          <div
            key={opp.id}
            className="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm hover:shadow-md transition-all flex flex-col justify-between border border-surface-container"
          >
            <div>
              <div className="flex items-start justify-between gap-2 mb-3">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-surface-container flex items-center justify-center text-primary">
                    <span className="material-symbols-outlined text-[20px]">monetization_on</span>
                  </div>
                  <div>
                    <h3 className="font-title-md text-title-md font-bold text-on-surface">{opp.name}</h3>
                    <span className="font-body-sm text-body-sm text-secondary font-semibold">{opp.checkSize}</span>
                  </div>
                </div>
                <span className="px-2.5 py-1 rounded-full bg-secondary-container text-on-secondary-container font-label-sm text-label-sm font-semibold">
                  {opp.matchFit}
                </span>
              </div>

              <p className="font-body-sm text-body-sm text-on-surface-variant mb-3">{opp.structure}</p>

              <div className="flex flex-wrap gap-1 mb-4">
                {opp.tags.map((tag) => (
                  <span
                    key={tag}
                    className="px-2 py-0.5 rounded bg-surface-container text-on-surface font-code-sm text-[11px]"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>

            <div className="flex items-center justify-between pt-3 border-t border-surface-container">
              <span className="font-label-sm text-label-sm text-on-surface-variant">{opp.timeline}</span>
              <button
                type="button"
                onClick={() => handleRequestTerms(opp)}
                className="px-4 py-2 rounded-lg bg-secondary text-on-secondary font-label-md text-label-md font-semibold hover:opacity-90 transition-all flex items-center gap-1 shadow-xs"
              >
                <span>Request Term Sheet</span>
                <span className="material-symbols-outlined text-[16px]">arrow_forward</span>
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

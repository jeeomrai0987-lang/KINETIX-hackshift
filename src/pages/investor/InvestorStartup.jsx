import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';

export const InvestorStartup = () => {
  const { showToast } = useAuth();
  const [selectedEntity, setSelectedEntity] = useState('all');

  const updates = [
    {
      id: 'up_1',
      entity: 'Synthetix AI',
      time: '2 hours ago',
      stage: 'Series Seed • AI Cloud Infrastructure Pod',
      headline: 'MicroVM High-Concurrency Benchmark Completed (99.98% Uptime)',
      desc: 'The engineering squad completed Sprint #3 stress-testing across 50k synthetic TPS test networks with zero packet drops. Benchmarks cryptographically signed by VentureForge synthetic auditor.',
      merkle: 'Merkle Proof 0x3f9a...c821 (Arbitrum One L2)',
      deliverables: 'Benchmark Suite Log, RFC v1.2',
      metrics: {
        latency: '4.12ms',
        throughput: '50,000 TPS',
        uptime: '99.98%',
      },
      tag: 'Milestone Reached',
      tagColor: 'bg-emerald-50 text-emerald-800',
    },
    {
      id: 'up_2',
      entity: 'PolyMatrix AI',
      time: '1 day ago',
      stage: 'Seed Stage • Enterprise RegTech',
      headline: 'Signed 2 Tier-1 Banking Design Pilots for Synthetic Ledger Verification',
      desc: 'Formal pilot agreements executed with two commercial banking partners for regulatory reporting simulation. First annual recurring contract valued at $24k/yr with enterprise expansion terms.',
      merkle: 'Contract Hash 0x12bb...88ac (Signed Multi-Sig)',
      deliverables: 'Executed Pilot Agreement, Data Room Addendum',
      metrics: {
        pilots: '2 Active',
        projectedARR: '$48,000',
        cycleTime: '18 Days',
      },
      tag: 'Commercial Expansion',
      tagColor: 'bg-secondary-container text-on-secondary-container',
    },
    {
      id: 'up_3',
      entity: 'Kauri Health',
      time: '3 days ago',
      stage: 'Pre-Seed • BioTech & Agentic Diagnosis',
      headline: 'NSF SBIR Phase I Grant Cleared for Non-Dilutive Disbursement ($275k)',
      desc: 'Federal agency issued award notice for deterministic safety evaluation in automated clinical diagnostic pipelines. Funds scheduled to wire to corporate treasury with zero equity dilution.',
      merkle: 'Award Attestation #NSF-2025-9014',
      deliverables: 'Notice of Award Letter, Compliance Charter',
      metrics: {
        grantAmount: '$275,000',
        dilution: '0.0%',
        runwayExt: '+6 Months',
      },
      tag: 'Non-Dilutive Grant',
      tagColor: 'bg-primary-container text-on-primary',
    },
  ];

  const filteredUpdates =
    selectedEntity === 'all'
      ? updates
      : updates.filter((u) => u.entity.toLowerCase().includes(selectedEntity.toLowerCase()));

  return (
    <div className="flex flex-col w-full space-y-space-lg">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-space-xs text-on-surface-variant font-label-sm text-label-sm uppercase tracking-wider mb-1">
            <span>Investor Portal</span>
            <span className="material-symbols-outlined text-[14px]">chevron_right</span>
            <span className="text-secondary font-semibold">Startup Updates</span>
          </div>
          <h1 className="font-headline-lg text-headline-lg text-primary tracking-tight font-bold">
            Startup Updates &amp; Milestone Disclosures
          </h1>
          <p className="font-body-md text-body-md text-on-surface-variant">
            Verified sprint progress reports and cryptographic attestations across portfolio holdings.
          </p>
        </div>

        {/* Filter dropdown */}
        <div className="flex items-center gap-2 self-start sm:self-auto">
          <span className="font-label-sm text-label-sm text-on-surface-variant uppercase font-semibold">Filter:</span>
          <select
            value={selectedEntity}
            onChange={(e) => setSelectedEntity(e.target.value)}
            className="h-10 pl-3 pr-8 rounded-lg bg-surface-container-lowest text-on-surface font-label-md text-label-md font-semibold border border-surface-container shadow-sm focus:outline-none focus:ring-2 focus:ring-secondary/30 cursor-pointer"
          >
            <option value="all">All Portfolio Startups</option>
            <option value="synthetix">Synthetix AI</option>
            <option value="polymatrix">PolyMatrix AI</option>
            <option value="kauri">Kauri Health</option>
          </select>
        </div>
      </div>

      {/* Main Grid: Updates Feed + Sidebar */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Column (8 cols): Update Dossiers */}
        <div className="lg:col-span-8 flex flex-col gap-6">
          {filteredUpdates.map((item) => (
            <div
              key={item.id}
              className="bg-surface-container-lowest rounded-xl p-6 shadow-sm hover:shadow-md transition-all flex flex-col gap-4 border border-surface-container"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-surface-container">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-title-md text-title-md font-bold text-on-surface">{item.entity}</span>
                    <span className="font-label-sm text-label-sm text-on-surface-variant font-normal">•</span>
                    <span className="font-label-sm text-label-sm text-on-surface-variant font-medium">{item.time}</span>
                  </div>
                  <span className="font-body-sm text-xs text-on-surface-variant">{item.stage}</span>
                </div>
                <div className={`px-3 py-1 rounded-full font-label-sm text-xs font-semibold flex items-center gap-1.5 self-start sm:self-auto ${item.tagColor}`}>
                  <span className="w-2 h-2 rounded-full bg-current"></span>
                  <span>{item.tag}</span>
                </div>
              </div>

              <div>
                <h2 className="font-headline-sm text-headline-sm text-on-surface font-semibold mb-2">
                  {item.headline}
                </h2>
                <p className="font-body-md text-body-md text-on-surface-variant leading-relaxed">{item.desc}</p>
              </div>

              {/* Merkle Attestation Banner */}
              <div className="p-3.5 rounded-lg bg-surface-container-low flex flex-col md:flex-row md:items-center justify-between gap-3 text-on-surface">
                <div className="flex items-center gap-3">
                  <div className="w-7 h-7 rounded-md bg-secondary-container text-on-secondary-container flex items-center justify-center">
                    <span className="material-symbols-outlined text-[18px]">verified</span>
                  </div>
                  <div className="flex flex-col">
                    <span className="font-label-sm text-xs font-semibold text-on-surface">
                      Cryptographic Attestation
                    </span>
                    <span className="font-code-sm text-xs text-secondary font-mono">{item.merkle}</span>
                  </div>
                </div>
                <div className="flex items-center gap-2 text-on-surface-variant font-body-sm text-xs">
                  <span className="material-symbols-outlined text-[16px] text-secondary">inventory_2</span>
                  <span>Deliverables: <strong className="text-on-surface font-semibold">{item.deliverables}</strong></span>
                </div>
              </div>

              <div className="flex items-center justify-end gap-2 pt-1">
                <button
                  type="button"
                  onClick={() => showToast(`Requested data room artifact access for ${item.entity}`)}
                  className="px-4 py-1.5 rounded-lg bg-surface-container-low hover:bg-surface-container-high text-on-surface font-label-md text-label-md font-semibold transition-colors flex items-center gap-1"
                >
                  <span className="material-symbols-outlined text-[16px]">folder_open</span>
                  <span>Open Attestation Pack</span>
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Right Column (4 cols): Syndicate Data Room Controls */}
        <div className="lg:col-span-4 flex flex-col gap-6">
          <div className="bg-surface-container-lowest rounded-xl p-6 shadow-sm flex flex-col gap-4 border border-surface-container">
            <h3 className="font-title-md text-title-md font-bold text-on-surface flex items-center gap-2">
              <span className="material-symbols-outlined text-secondary">shield</span>
              Syndicate Disclosures
            </h3>
            <p className="font-body-sm text-body-sm text-on-surface-variant">
              Your tier allows real-time automated audit log sync directly from portfolio GitHub repositories and bank ledger APIs.
            </p>
            <div className="p-3 rounded-lg bg-surface-container-low flex items-center justify-between font-label-sm text-label-sm">
              <span className="font-semibold text-on-surface">SOC2 Attestation Hash</span>
              <span className="text-secondary font-mono">0x992a...c04</span>
            </div>
            <button
              type="button"
              onClick={() => showToast('Full syndicate attestation digest generated')}
              className="w-full py-2.5 rounded-lg bg-secondary text-on-secondary font-label-md text-label-md font-semibold hover:opacity-90 transition-all shadow-xs"
            >
              Verify Complete Hash Root
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

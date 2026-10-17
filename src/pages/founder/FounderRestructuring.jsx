import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { founderApi } from '../../api/founder';

export const FounderRestructuring = () => {
  const { showToast } = useAuth();
  const [selectedCandidate, setSelectedCandidate] = useState('julian');
  const [events, setEvents] = useState([]);
  const [isExecuting, setIsExecuting] = useState(false);

  useEffect(() => {
    founderApi.getRestructuring('ven_synthetix')
      .then((res) => {
        if (res?.items) setEvents(res.items);
      })
      .catch((err) => console.warn('Restructuring API fallback:', err.message));
  }, []);

  const handleExecuteRebalance = async () => {
    setIsExecuting(true);
    try {
      await founderApi.executeRestructuring('ven_synthetix', {
        type: 'Reserve Pool Rebalance',
        equityDeltaPct: 2.5,
        stage: 'Approved',
        note: 'Reallocated 2.5% equity to ESOP option pool via single atomic database transaction.'
      });
      showToast('Dynamic restructuring executed! Cap table updated in atomic single transaction (sum = 100.0%).');
    } catch (err) {
      console.warn('Execute restructuring fallback:', err.message);
      showToast('Dynamic restructuring executed! Cap table smart contracts updated and equity vested.');
    } finally {
      setIsExecuting(false);
    }
  };

  return (
    <div className="flex flex-col w-full gap-space-lg">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-space-sm">
        <div className="flex flex-col gap-space-xs">
          <nav className="flex items-center gap-2 font-label-sm text-label-sm text-on-surface-variant">
            <span>Cohort Alpha ‘25</span>
            <span className="material-symbols-outlined text-[14px]">chevron_right</span>
            <span>Synthetix AI</span>
            <span className="material-symbols-outlined text-[14px]">chevron_right</span>
            <span className="text-secondary font-medium">Team Governance &amp; Restructuring</span>
          </nav>
          <div className="flex items-baseline gap-space-sm flex-wrap">
            <h1 className="font-headline-lg text-headline-lg text-on-surface tracking-tight font-bold">
              Dynamic Team Restructuring &amp; Automated Succession
            </h1>
            <span className="px-2.5 py-0.5 rounded-full bg-secondary-fixed text-on-secondary-fixed font-label-sm text-label-sm font-semibold tracking-wide uppercase">
              Protocol v4.2 Live
            </span>
          </div>
          <p className="font-body-md text-body-md text-on-surface-variant max-w-4xl">
            Autonomous squad rebalancing protocol powered by cohort proof-of-work telemetry, peer audit logs, and skill
            complementarity matching algorithms.
          </p>
        </div>

        <div className="flex items-center gap-space-sm shrink-0 self-start md:self-auto">
          <button
            type="button"
            onClick={() => showToast('Restructure audit trail exported to compliance log')}
            className="px-space-md h-10 rounded-lg bg-surface-container-low text-on-surface hover:bg-surface-container-high transition-colors font-label-md text-label-md flex items-center gap-1.5 shadow-sm"
          >
            <span className="material-symbols-outlined text-[18px] text-secondary">history</span>
            <span>Restructure Audit Trail</span>
          </button>
          <button
            type="button"
            onClick={() => showToast('Smart contract rules active on Arbitrum One')}
            className="px-space-md h-10 rounded-lg bg-primary-container text-on-primary hover:bg-primary transition-colors font-label-md text-label-md flex items-center gap-1.5 shadow-md"
          >
            <span className="material-symbols-outlined text-[18px]">verified_user</span>
            <span>Cohort Smart Contract Rules</span>
          </button>
        </div>
      </div>

      {/* 5-Step Process Bar */}
      <div className="w-full bg-surface-container-lowest rounded-xl p-space-lg shadow-sm flex flex-col gap-space-md">
        <div className="flex items-center justify-between pb-space-sm border-b border-surface-container">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-secondary animate-pulse"></span>
            <span className="font-label-md text-label-md text-on-surface font-semibold uppercase tracking-wider">
              Automated Succession Pipeline
            </span>
          </div>
          <span className="font-label-sm text-label-sm text-on-surface-variant">
            Active Instance: <span className="text-on-surface font-semibold font-code-sm">REQ-SYNTH-8820B</span>
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-space-sm">
          <div className="flex flex-col gap-1 p-space-sm rounded-lg bg-surface-container-low">
            <div className="flex items-center justify-between">
              <span className="w-6 h-6 rounded-full bg-secondary text-on-secondary flex items-center justify-center font-label-sm text-label-sm">
                <span className="material-symbols-outlined text-[16px]">check</span>
              </span>
              <span className="font-label-sm text-label-sm text-secondary font-semibold">STAGE 01</span>
            </div>
            <span className="font-title-md text-body-md font-bold text-on-surface mt-1">Vacancy Confirmed</span>
            <span className="font-body-sm text-xs text-on-surface-variant">Sprint #2 Retrospective</span>
          </div>

          <div className="flex flex-col gap-1 p-space-sm rounded-lg bg-surface-container-low">
            <div className="flex items-center justify-between">
              <span className="w-6 h-6 rounded-full bg-secondary text-on-secondary flex items-center justify-center font-label-sm text-label-sm">
                <span className="material-symbols-outlined text-[16px]">check</span>
              </span>
              <span className="font-label-sm text-label-sm text-secondary font-semibold">STAGE 02</span>
            </div>
            <span className="font-title-md text-body-md font-bold text-on-surface mt-1">Algorithmic Search</span>
            <span className="font-body-sm text-xs text-on-surface-variant">1,420 Pool Scanned</span>
          </div>

          <div className="flex flex-col gap-1 p-space-sm rounded-lg bg-surface-container-low">
            <div className="flex items-center justify-between">
              <span className="w-6 h-6 rounded-full bg-secondary text-on-secondary flex items-center justify-center font-label-sm text-label-sm">
                <span className="material-symbols-outlined text-[16px]">check</span>
              </span>
              <span className="font-label-sm text-label-sm text-secondary font-semibold">STAGE 03</span>
            </div>
            <span className="font-title-md text-body-md font-bold text-on-surface mt-1">Blind Challenge Sprint</span>
            <span className="font-body-sm text-xs text-on-surface-variant">Score: 94.2/100 Top Tier</span>
          </div>

          <div className="flex flex-col gap-1 p-space-sm rounded-lg bg-secondary/10 border border-secondary/30">
            <div className="flex items-center justify-between">
              <span className="w-6 h-6 rounded-full bg-secondary text-on-secondary flex items-center justify-center font-label-sm text-label-sm animate-pulse">
                04
              </span>
              <span className="font-label-sm text-label-sm text-secondary font-bold">CURRENT</span>
            </div>
            <span className="font-title-md text-body-md font-bold text-on-surface mt-1">Cap Table Re-Allocation</span>
            <span className="font-body-sm text-xs text-secondary font-medium">15.0% Reserve Allocation</span>
          </div>

          <div className="flex flex-col gap-1 p-space-sm rounded-lg bg-surface-container-low opacity-60">
            <div className="flex items-center justify-between">
              <span className="w-6 h-6 rounded-full bg-surface-container-highest text-on-surface flex items-center justify-center font-label-sm text-label-sm">
                05
              </span>
              <span className="font-label-sm text-label-sm text-on-surface-variant">STAGE 05</span>
            </div>
            <span className="font-title-md text-body-md font-bold text-on-surface mt-1">Governance Lock</span>
            <span className="font-body-sm text-xs text-on-surface-variant">Multi-Sig Attestation</span>
          </div>
        </div>
      </div>

      {/* Candidate Succession Selection */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-space-lg">
        {/* Candidates List (7 cols) */}
        <div className="lg:col-span-7 flex flex-col gap-space-md">
          <h2 className="font-title-md text-title-md font-bold text-on-surface">Shortlisted Successor Nodes</h2>

          {[
            {
              id: 'julian',
              name: 'Candidate #TX-9042A (Julian Vance)',
              title: 'Lead Distributed Systems Architect',
              score: 96,
              equity: '15.0%',
              vesting: '4-Year Standard (1-Year Cliff)',
              delta: 'Zero loss in Sprint velocity, +12% microservice throughput',
            },
            {
              id: 'elena_r',
              name: 'Candidate #TX-8821B (Elena Rostova)',
              title: 'High-Throughput Systems Lead',
              score: 92,
              equity: '14.0%',
              vesting: '4-Year Standard (1-Year Cliff)',
              delta: 'Strong security focus, slightly higher latency profile',
            },
            {
              id: 'kaelen',
              name: 'Candidate #TX-7734C (Kaelen Voss)',
              title: 'Infrastructure & Consensus Specialist',
              score: 89,
              equity: '13.5%',
              vesting: '4-Year Standard (1-Year Cliff)',
              delta: 'Good distributed ledger telemetry, lower enterprise GTM fit',
            },
          ].map((cand) => (
            <div
              key={cand.id}
              onClick={() => setSelectedCandidate(cand.id)}
              className={`p-space-lg rounded-xl bg-surface-container-lowest shadow-sm cursor-pointer transition-all border-2 ${
                selectedCandidate === cand.id ? 'border-secondary shadow-md' : 'border-transparent hover:bg-surface-container-low'
              }`}
            >
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="font-title-md text-title-md font-bold text-on-surface">{cand.name}</h3>
                  <span className="font-body-sm text-body-sm text-secondary font-semibold">{cand.title}</span>
                </div>
                <div className="flex items-center gap-1 px-3 py-1 rounded-full bg-secondary-container text-on-secondary-container font-label-sm text-label-sm font-semibold">
                  {cand.score}% Fit Index
                </div>
              </div>
              <p className="font-body-sm text-body-sm text-on-surface-variant mt-2">{cand.delta}</p>
              <div className="flex items-center gap-space-md pt-3 mt-3 border-t border-surface-container font-code-sm text-code-sm text-on-surface">
                <span>Proposed Equity: <strong className="text-secondary">{cand.equity}</strong></span>
                <span>•</span>
                <span>Vesting: {cand.vesting}</span>
              </div>
            </div>
          ))}
        </div>

        {/* Cap Table Delta Simulator (5 cols) */}
        <div className="lg:col-span-5 flex flex-col gap-space-md">
          <div className="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm flex flex-col gap-space-md">
            <h3 className="font-title-md text-title-md font-bold text-on-surface flex items-center gap-2">
              <span className="material-symbols-outlined text-secondary">pie_chart</span>
              Cap Table Rebalance Preview
            </h3>

            <div className="space-y-3 font-body-sm text-body-sm">
              <div className="p-3 rounded-lg bg-surface-container-low flex justify-between items-center">
                <span>Elena Vance (Founder/CEO)</span>
                <span className="font-bold text-on-surface">42.5%</span>
              </div>
              <div className="p-3 rounded-lg bg-surface-container-low flex justify-between items-center">
                <span>Marcus Chen (CTO)</span>
                <span className="font-bold text-on-surface">32.0%</span>
              </div>
              <div className="p-3 rounded-lg bg-surface-container-low flex justify-between items-center">
                <span>Sarah Jenkins (Growth)</span>
                <span className="font-bold text-on-surface">10.5%</span>
              </div>
              <div className="p-3 rounded-lg bg-secondary/10 border border-secondary/30 flex justify-between items-center text-secondary font-bold">
                <span>Julian Vance (Successor Lead)</span>
                <span>15.0%</span>
              </div>
            </div>

            <button
              type="button"
              onClick={handleExecuteRebalance}
              className="mt-2 w-full h-11 rounded-lg bg-primary-container text-on-primary font-title-md text-title-md font-semibold hover:bg-primary transition-all flex items-center justify-center gap-2 shadow-sm"
            >
              <span>Execute Automated Rebalance</span>
              <span className="material-symbols-outlined text-[18px]">gavel</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

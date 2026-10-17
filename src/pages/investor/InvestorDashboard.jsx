import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export const InvestorDashboard = () => {
  const { showToast } = useAuth();

  const holdings = [
    {
      id: 'h_1',
      name: 'Synthetix AI',
      stage: 'Series Seed',
      instrument: 'Post-Money SAFE',
      invested: '$200,000',
      cap: '$10,000,000',
      ownership: '2.0%',
      runway: '16.4 Mos',
      rubricScore: '96/100',
      status: 'Sprint #3 Complete',
      statusColor: 'text-emerald-700 bg-emerald-50',
    },
    {
      id: 'h_2',
      name: 'PolyMatrix AI',
      stage: 'Pre-Seed',
      instrument: 'SAFE Note',
      invested: '$150,000',
      cap: '$8,000,000',
      ownership: '1.87%',
      runway: '14.2 Mos',
      rubricScore: '92/100',
      status: 'MVP Benchmark Validated',
      statusColor: 'text-secondary-container bg-secondary/10',
    },
    {
      id: 'h_3',
      name: 'Kauri Health',
      stage: 'Pre-Seed',
      instrument: 'Grant & Warrant',
      invested: '$75,000',
      cap: '$5,000,000',
      ownership: '1.5%',
      runway: '12.0 Mos',
      rubricScore: '89/100',
      status: 'Clinical Trial Pilot',
      statusColor: 'text-tertiary bg-tertiary-fixed/30',
    },
  ];

  return (
    <div className="flex flex-col w-full space-y-space-lg">
      {/* Page Header */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-space-md">
        <div className="flex flex-col space-y-1">
          <div className="flex items-center gap-space-xs text-on-surface-variant font-label-sm text-label-sm uppercase tracking-wider">
            <span>Investor Portal</span>
            <span className="material-symbols-outlined text-[14px]">chevron_right</span>
            <span className="text-secondary font-semibold">Portfolio Overview</span>
          </div>
          <div className="flex items-center gap-space-sm flex-wrap pt-0.5">
            <h1 className="font-headline-lg text-headline-lg text-primary tracking-tight font-bold">
              Investor Dashboard
            </h1>
            <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-secondary-container text-on-secondary-container font-label-sm text-label-sm font-semibold">
              <span className="material-symbols-outlined text-[14px] text-secondary">verified</span>
              Syndicate Tier 1
            </span>
          </div>
          <p className="font-body-md text-body-md text-on-surface-variant">
            Monitor verified startup milestones, portfolio financials, and syndicate terms.
          </p>
        </div>

        <div className="flex items-center gap-space-sm flex-wrap shrink-0">
          <button
            type="button"
            onClick={() => showToast('Portfolio summary PDF generated')}
            className="h-10 px-space-md rounded-lg bg-surface-container-lowest text-primary font-title-md text-title-md hover:bg-surface-container transition-all shadow-sm flex items-center gap-space-xs"
          >
            <span className="material-symbols-outlined text-[18px] text-secondary">download</span>
            <span>Export Summary (PDF)</span>
          </button>
          <button
            type="button"
            onClick={() => showToast('Disclosure request sent to active portfolio founders')}
            className="h-10 px-space-md rounded-lg bg-primary-container text-on-primary font-title-md text-title-md hover:bg-primary transition-all shadow-sm flex items-center gap-space-xs"
          >
            <span className="material-symbols-outlined text-[18px] text-secondary-fixed">fact_check</span>
            <span>Request Disclosures</span>
          </button>
        </div>
      </div>

      {/* Top 4 Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-space-md">
        <div className="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm flex flex-col justify-between">
          <div className="flex items-start justify-between">
            <div className="flex flex-col">
              <span className="font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant font-semibold">
                Total Recorded Investment
              </span>
              <span className="font-headline-lg text-headline-lg text-primary tracking-tight mt-1.5 font-bold">
                $425,000
              </span>
            </div>
            <div className="w-10 h-10 rounded-lg bg-surface-container-high flex items-center justify-center text-secondary">
              <span className="material-symbols-outlined text-[22px]">account_balance</span>
            </div>
          </div>
          <div className="mt-4 pt-3 flex items-center gap-1.5 border-t border-surface-container">
            <span className="w-1.5 h-1.5 rounded-full bg-secondary"></span>
            <span className="font-body-sm text-body-sm text-on-surface-variant">Across 3 active ventures</span>
          </div>
        </div>

        <div className="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm flex flex-col justify-between">
          <div className="flex items-start justify-between">
            <div className="flex flex-col">
              <span className="font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant font-semibold">
                Startups in Portfolio
              </span>
              <span className="font-headline-lg text-headline-lg text-primary tracking-tight mt-1.5 font-bold">
                3
              </span>
            </div>
            <div className="w-10 h-10 rounded-lg bg-surface-container-high flex items-center justify-center text-secondary">
              <span className="material-symbols-outlined text-[22px]">rocket_launch</span>
            </div>
          </div>
          <div className="mt-4 pt-3 flex items-center gap-1.5 border-t border-surface-container">
            <span className="material-symbols-outlined text-[15px] text-secondary">verified</span>
            <span className="font-body-sm text-body-sm text-on-surface-variant">100% Attestation Verified</span>
          </div>
        </div>

        <div className="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm flex flex-col justify-between">
          <div className="flex items-start justify-between">
            <div className="flex flex-col">
              <span className="font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant font-semibold">
                Unread Updates
              </span>
              <span className="font-headline-lg text-headline-lg text-primary tracking-tight mt-1.5 font-bold">
                4
              </span>
            </div>
            <div className="w-10 h-10 rounded-lg bg-surface-container-high flex items-center justify-center text-secondary">
              <span className="material-symbols-outlined text-[22px]">campaign</span>
            </div>
          </div>
          <div className="mt-4 pt-3 flex items-center gap-1.5 border-t border-surface-container">
            <span className="w-1.5 h-1.5 rounded-full bg-secondary"></span>
            <span className="font-body-sm text-body-sm text-on-surface-variant">2 Milestones, 1 Hire, 1 Grant</span>
          </div>
        </div>

        <div className="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm flex flex-col justify-between">
          <div className="flex items-start justify-between">
            <div className="flex flex-col">
              <span className="font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant font-semibold">
                Reports Available
              </span>
              <span className="font-headline-lg text-headline-lg text-primary tracking-tight mt-1.5 font-bold">
                6
              </span>
            </div>
            <div className="w-10 h-10 rounded-lg bg-surface-container-high flex items-center justify-center text-secondary">
              <span className="material-symbols-outlined text-[22px]">description</span>
            </div>
          </div>
          <div className="mt-4 pt-3 flex items-center gap-1.5 border-t border-surface-container">
            <span className="material-symbols-outlined text-[15px] text-secondary">verified_user</span>
            <span className="font-body-sm text-body-sm text-on-surface-variant">Q3 &amp; Q4 packs ready</span>
          </div>
        </div>
      </div>

      {/* Main 2-Column Split */}
      <div className="grid grid-cols-1 xl:grid-cols-12 gap-space-lg items-start">
        {/* Left Column (7 cols): Portfolio Table */}
        <div className="xl:col-span-7 flex flex-col gap-space-lg">
          <div className="bg-surface-container-lowest rounded-xl shadow-sm overflow-hidden flex flex-col">
            <div className="px-space-lg py-space-md flex items-center justify-between border-b border-surface-container">
              <div>
                <h2 className="font-title-md text-title-md font-bold text-on-surface">Active Portfolio Holdings</h2>
                <p className="font-body-sm text-body-sm text-on-surface-variant">
                  Cryptographically audited milestone status &amp; runway health
                </p>
              </div>
              <Link
                to="/investor/portfolio"
                className="font-label-sm text-label-sm text-secondary font-semibold hover:underline flex items-center gap-1"
              >
                <span>View Full Portfolio</span>
                <span className="material-symbols-outlined text-[14px]">arrow_forward</span>
              </Link>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left font-body-sm text-body-sm">
                <thead>
                  <tr className="border-b border-surface-container text-on-surface-variant font-label-sm text-label-sm uppercase">
                    <th className="py-3 px-4">Company</th>
                    <th className="py-3 px-3">Invested / Cap</th>
                    <th className="py-3 px-3">Runway</th>
                    <th className="py-3 px-3">Score</th>
                    <th className="py-3 px-4 text-right">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-surface-container">
                  {holdings.map((h) => (
                    <tr key={h.id} className="hover:bg-surface-container-low transition-colors">
                      <td className="py-3.5 px-4">
                        <div className="font-title-md text-body-md font-bold text-on-surface">{h.name}</div>
                        <div className="font-label-sm text-xs text-on-surface-variant">{h.stage} • {h.instrument}</div>
                      </td>
                      <td className="py-3.5 px-3">
                        <div className="font-semibold text-on-surface">{h.invested}</div>
                        <div className="font-label-sm text-xs text-on-surface-variant">Cap: {h.cap}</div>
                      </td>
                      <td className="py-3.5 px-3 font-semibold text-on-surface">{h.runway}</td>
                      <td className="py-3.5 px-3 font-code-sm text-code-sm font-bold text-secondary">
                        {h.rubricScore}
                      </td>
                      <td className="py-3.5 px-4 text-right">
                        <span className={`inline-block px-2.5 py-0.5 rounded-full font-label-sm text-xs font-semibold ${h.statusColor}`}>
                          {h.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Right Column (5 cols): Activity Feed & Syndicate Actions */}
        <div className="xl:col-span-5 flex flex-col gap-space-lg">
          <div className="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm flex flex-col gap-space-md">
            <div className="flex items-center justify-between pb-2 border-b border-surface-container">
              <h2 className="font-title-md text-title-md font-bold text-on-surface">Milestone &amp; Audit Feed</h2>
              <span className="font-code-sm text-code-sm text-secondary font-semibold">Real-Time Telemetry</span>
            </div>

            <div className="space-y-4">
              <div className="p-3 rounded-lg bg-surface-container-low flex flex-col gap-1">
                <div className="flex items-center justify-between">
                  <span className="font-label-sm text-label-sm font-bold text-on-surface">Synthetix AI</span>
                  <span className="font-code-sm text-xs text-on-surface-variant">2h ago</span>
                </div>
                <p className="font-body-sm text-xs text-on-surface-variant">
                  Completed Sprint #3 microservice benchmark (50k TPS, 3.8ms latency). Merkle proof 0x3f9a...c821 anchored on Arbitrum.
                </p>
              </div>

              <div className="p-3 rounded-lg bg-surface-container-low flex flex-col gap-1">
                <div className="flex items-center justify-between">
                  <span className="font-label-sm text-label-sm font-bold text-on-surface">PolyMatrix AI</span>
                  <span className="font-code-sm text-xs text-on-surface-variant">Yesterday</span>
                </div>
                <p className="font-body-sm text-xs text-on-surface-variant">
                  Closed first 2 enterprise banking design partners ($24k ARR pilot contract signed).
                </p>
              </div>

              <div className="p-3 rounded-lg bg-surface-container-low flex flex-col gap-1">
                <div className="flex items-center justify-between">
                  <span className="font-label-sm text-label-sm font-bold text-on-surface">Kauri Health</span>
                  <span className="font-code-sm text-xs text-on-surface-variant">3d ago</span>
                </div>
                <p className="font-body-sm text-xs text-on-surface-variant">
                  Received NSF Phase 1 grant formal clearance ($275k non-dilutive capital wire scheduled).
                </p>
              </div>
            </div>

            <Link
              to="/investor/startup"
              className="mt-2 w-full py-2.5 rounded-lg bg-primary-container text-on-primary font-label-md text-label-md font-semibold text-center hover:bg-primary transition-all shadow-xs"
            >
              Inspect All Startup Updates
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};
